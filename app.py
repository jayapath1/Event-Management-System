from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from mastodon_integration.mastodon_service import post_event_announcement
import pymysql

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# -------------------- LOGIN / LOGOUT --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'ucp' and password == 'ucp123':
            session['logged_in'] = True
            session['username'] = username
            session['role'] = 'manager'
            return redirect(url_for('index'))

        elif username == 'customer' and password == 'cust123':
            session['logged_in'] = True
            session['username'] = username
            session['role'] = 'customer'
            return redirect(url_for('index'))

        else:
            error_message = 'Invalid credentials. Please try again.'

    return render_template('login.html', error_message=error_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------- DATABASE CONFIG --------------------
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'EMS'
app.config['MYSQL_PORT'] = 3306

def create_db_connection():
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            port=app.config["MYSQL_PORT"],
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise e

# -------------------- INDEX / EVENTS --------------------
@app.route('/')
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    try:
        with create_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Events")
                events = cursor.fetchall()
        return render_template('index.html', events=events)
    except pymysql.Error as e:
        print(f"Error fetching events: {e}")
        return render_template('error.html', error_message=str(e))

@app.route('/event_details/<int:event_id>')
def event_details(event_id):
    print("SESSION DATA:", session)
    try:
        with create_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Events WHERE EventID=%s", (event_id,))
                event = cursor.fetchone()

                if not event:
                    return render_template('event_details.html', events={})

                cursor.execute("SELECT * FROM Tickets WHERE EventID=%s", (event_id,))
                tickets = cursor.fetchall()

            venues = fetch_venue_details(connection)
            organizer = fetch_organizer_details(connection)
            attendees = fetch_attendees(connection, event_id)
            registrations = fetch_registrations(connection)
            sessions = fetch_sessions(connection, event_id)
            speakers = fetch_speakers(connection, event_id)
            feedbacks = fetch_feedbacks(connection)
            social_media_promotions = fetch_social_media_promotions(connection, event_id)
            sponsors = fetch_sponsors(connection, event_id)

        return render_template(
            'event_details.html',
            events=event,
            venues=venues,
            organizer=organizer,
            attendees=attendees,
            tickets=tickets,
            registrations=registrations,
            sessions=sessions,
            speakers=speakers,
            feedbacks=feedbacks,
            social_media_promotions=social_media_promotions,
            sponsors=sponsors
        )
    except pymysql.Error as e:
        print(f"Error fetching event details: {e}")
        return render_template('error.html', error_message=str(e))

# -------------------- FETCH HELPERS --------------------
def fetch_venue_details(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Venues LIMIT 1")
        return cursor.fetchone()

def fetch_organizer_details(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Organizers LIMIT 1")
        return cursor.fetchone()

def fetch_attendees(connection, event_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT a.FirstName, a.LastName
            FROM Attendees a
            JOIN Registrations r ON a.AttendeeID = r.AttendeeID
            WHERE r.EventID = %s
        """, (event_id,))
        return cursor.fetchall()

def fetch_registrations(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Registrations")
        return cursor.fetchall()

def fetch_sessions(connection, event_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT s.SessionID, s.Title, s.StartTime, s.EndTime, sp.SpeakerName
            FROM Sessions s
            JOIN Speakers sp ON s.SpeakerID = sp.SpeakerID
            WHERE s.EventID = %s
        """, (event_id,))
        return cursor.fetchall()

def fetch_speakers(connection, event_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT DISTINCT sp.SpeakerID, sp.SpeakerName, sp.Bio
            FROM Speakers sp
            JOIN Sessions s ON sp.SpeakerID = s.SpeakerID
            WHERE s.EventID = %s
        """, (event_id,))
        return cursor.fetchall()
    
def fetch_sponsors(connection, event_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT SponsorName, ContactPerson, ContactNumber
            FROM Sponsors
            WHERE SponsorID = %s
        """, (event_id,))
        return cursor.fetchall()

def fetch_feedbacks(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Feedback")
        return cursor.fetchall()

def fetch_social_media_promotions(connection, event_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("""
            SELECT Platform, Content, DatePosted
            FROM SocialMediaPromotion
            WHERE EventID = %s
        """, (event_id,))
        return cursor.fetchall()

# -------------------- ADD/DELETE EVENT --------------------
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if session.get('role') != 'manager':
        return render_template('error.html', error_message="Access denied: managers only.")
    try:
        with create_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT VenueID, VenueName FROM Venues")
                venues = cursor.fetchall()
                cursor.execute("SELECT OrganizerID, OrganizerName FROM Organizers")
                organizers = cursor.fetchall()
    except pymysql.Error as e:
        return render_template('error.html', error_message=f"Error fetching venues/organizers: {e}")

    if request.method == 'POST':
        event_name = request.form.get('EventName')
        event_date = request.form.get('EventDate')
        venue_id = request.form.get('VenueID')
        organizer_id = request.form.get('OrganizerID')
        start_time = request.form.get('StartTime') or None
        end_time = request.form.get('EndTime') or None
        description = request.form.get('Description') or None
        status = request.form.get('Status') or None
        budget = request.form.get('Budget') or None

        if not event_name or not event_date or not venue_id or not organizer_id:
            error_message = "Event name, date, venue, and organizer are required."
            return render_template('add_event.html', venues=venues, organizers=organizers, error_message=error_message)

        try:
            with create_db_connection() as connection:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(
                        """
                        INSERT INTO Events 
                        (EventName, EventDate, StartTime, EndTime, Description, Status, Budget, VenueID, OrganizerID)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (event_name, event_date, start_time, end_time, description, status, budget, venue_id, organizer_id)
                    )
                    connection.commit()
            return redirect(url_for('index'))
        except pymysql.Error as e:
            return render_template('error.html', error_message=f"Error inserting event: {e}")

    return render_template('add_event.html', venues=venues, organizers=organizers)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    if session.get("role") != "manager":
        flash("Unauthorized action", "danger")
        return redirect(url_for("index"))
    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Events WHERE EventID = %s", (event_id,))
                connection.commit()
        flash("Event deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting event: {str(e)}", "danger")

    return redirect(url_for("index"))

# -------------------- TICKET MANAGEMENT --------------------
@app.route('/event_details/<int:event_id>/buy_ticket', methods=['POST'])
def buy_ticket_form(event_id):
    attendee_name = request.form.get('attendee_name')
    attendee_email = request.form.get('attendee_email')
    attendee_phone = request.form.get('attendee_phone')
    if not attendee_name:
        return redirect(url_for('event_details', event_id=event_id))

    if " " in attendee_name:
        first_name, last_name = attendee_name.split(" ", 1)
    else:
        first_name = attendee_name
        last_name = ""

    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Attendees (FirstName, LastName, Email, ContactNumber) VALUES (%s, %s, %s, %s)",
                    (first_name, last_name, attendee_email, attendee_phone)
                )
                attendee_id = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO Tickets (EventID, AttendeeName) VALUES (%s, %s)",
                    (event_id, attendee_name)
                )

                cursor.execute(
                    "INSERT INTO Registrations (EventID, AttendeeID) VALUES (%s, %s)",
                    (event_id, attendee_id)
                )

                connection.commit()

        return redirect(url_for('event_details', event_id=event_id))

    except Exception as e:
        return render_template('error.html', error_message=f"Error purchasing ticket: {e}")

@app.route('/events/<int:event_id>/tickets', methods=['GET'])
def get_tickets(event_id):
    try:
        with create_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM tickets WHERE event_id = %s", (event_id,))
                tickets = cursor.fetchall()
        return jsonify(tickets)
    except pymysql.Error as e:
        return jsonify({"error": str(e)}), 500

# -------------------- ERROR HANDLER --------------------
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Unexpected error: {e}")
    return render_template('error.html', error_message=str(e))

# -------------------- MASTODON INTEGRATION --------------------
@app.route('/create_event', methods=['POST'])
def create_event():
    mastodon.toot(f"New event: {event_name} on {event_date}!")
    return "Event created!"

# -------------------- RUN APP --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)