from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'my_secret_key'
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'ucp' and password == 'ucp123':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error_message = 'Invalid credentials. Please try again.'

    return render_template('login.html', error_message=error_message)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jayapath'
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
    try:
        with create_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(f"SELECT * FROM Events where EventID = {event_id}")
                event = cursor.fetchone()

                if event:
                    venues = fetch_venue_details(connection)
                    organizer = fetch_organizer_details(connection)
                    attendees = fetch_attendees(connection)
                    registrations = fetch_registrations(connection)
                    sessions = fetch_sessions(connection)
                    speakers = fetch_speakers(connection)
                    feedbacks = fetch_feedbacks(connection)
                    social_media_promotions = fetch_social_media_promotions(connection)

                    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                        cursor.execute("SELECT * FROM Tickets WHERE EventID=%s", (event_id,))
                        tickets = cursor.fetchall()

                    return render_template('event_details.html', events=event, venues=venues, organizer=organizer,
                                           attendees=attendees, registrations=registrations,
                                           sessions=sessions,
                                           speakers=speakers, feedbacks=feedbacks,
                                           social_media_promotions=social_media_promotions, tickets=tickets)
                else:
                    return render_template('event_details.html', event={})
    except pymysql.Error as e:
        print(f"Error fetching event details: {e}")
        return render_template('error.html', error_message=str(e))

def fetch_venue_details(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Venues limit 1")
        return cursor.fetchone()
    
def fetch_organizer_details(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Organizers limit 1")
        return cursor.fetchone()

def fetch_attendees(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Attendees")
        return cursor.fetchall()

def fetch_registrations(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Registrations")
        return cursor.fetchall()

def fetch_sessions(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Sessions")
        return cursor.fetchall()

def fetch_speakers(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Speakers")
        return cursor.fetchall()

def fetch_feedbacks(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM Feedback")
        return cursor.fetchall()


def fetch_social_media_promotions(connection):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM SocialMediaPromotion")
        return cursor.fetchall()

@app.route('/event_details/<int:event_id>/json')
def event_details_json(event_id):
    try:
        with create_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Events limit 1")
                event = cursor.fetchone()

                if event:
                    venues = fetch_venue_details(connection)
                    organizer = fetch_organizer_details(connection)
                    attendees = fetch_attendees(connection)
                    registrations = fetch_registrations(connection)
                    sessions = fetch_sessions(connection)
                    speakers = fetch_speakers(connection)
                    feedbacks = fetch_feedbacks(connection)
                    social_media_promotions = fetch_social_media_promotions(connection)

                    event_dict = {
                        'EventDetails': event,
                        'VenueDetails':venues,
                        'OrganizerDetails': organizer,
                        'Attendees': attendees,
                        'Registrations': registrations,
                        'Sessions': sessions,
                        'Speakers': speakers,
                        'Feedbacks': feedbacks,
                        'SocialMediaPromotions': social_media_promotions,
                    }
                    return jsonify(event_dict)
                else:
                    return jsonify({})
    except pymysql.Error as e:
        print(f"Error fetching event details: {e}")
        return jsonify({'error': str(e)})

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
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

                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT * FROM Events WHERE EventName=%s ORDER BY EventID DESC LIMIT 1", (event_name,))
                    inserted_event = cursor.fetchone()
                    print("Inserted event:", inserted_event)

            return redirect(url_for('index'))

        except pymysql.Error as e:
            return render_template('error.html', error_message=f"Error inserting event: {e}")

    return render_template('add_event.html', venues=venues, organizers=organizers)

@app.route('/tickets', methods=['POST'])
def buy_ticket():
    data = request.json
    event_id = data.get('event_id')
    attendee_name = data.get('attendee_name')

    if not event_id or not attendee_name:
        return jsonify({'error': 'Event ID and attendee name are required'}), 400

    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Tickets (EventID, AttendeeName) VALUES (%s, %s)",
                    (event_id, attendee_name)
                )
            connection.commit()
        return jsonify({'message': 'Ticket purchased successfully'}), 201
    except pymysql.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/events/<int:event_id>/tickets', methods=['GET'])
def get_tickets(event_id):
    try:
        with create_db_connection() as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM Tickets WHERE EventID=%s", (event_id,))
                tickets = cursor.fetchall()
        return jsonify(tickets)
    except pymysql.Error as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Unexpected error: {e}")
    return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)