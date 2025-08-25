from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# -----------------------
# MySQL Configuration
# -----------------------
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jayapath'
app.config['MYSQL_DB'] = 'EMS'
app.config['MYSQL_PORT'] = 3306

# -----------------------
# Helper: Create DB Connection
# -----------------------
def create_db_connection():
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            port=app.config["MYSQL_PORT"],
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise e

# -----------------------
# Login / Logout
# -----------------------
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -----------------------
# Index / Event List
# -----------------------
@app.route('/')
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Events")
                events = cursor.fetchall()
        return render_template('index.html', events=events)
    except pymysql.Error as e:
        return render_template('error.html', error_message=str(e))

# -----------------------
# Event Details & Tickets
# -----------------------
@app.route('/event/<int:event_id>')
def event_details(event_id):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                # Event info
                cursor.execute("SELECT * FROM Events WHERE EventID = %s", (event_id,))
                event = cursor.fetchone()
                
                if not event:
                    return render_template('event_details.html', event={}, venue={}, tickets=[])
                
                # Venue info
                cursor.execute("SELECT * FROM Venues WHERE VenueID = %s", (event['VenueID'],))
                venue = cursor.fetchone()
                
                # Tickets
                cursor.execute("SELECT * FROM Tickets WHERE EventID = %s", (event_id,))
                tickets = cursor.fetchall()

        return render_template('event_details.html', event=event, venue=venue, tickets=tickets)
    except pymysql.Error as e:
        return render_template('error.html', error_message=str(e))

# -----------------------
# Buy Ticket Endpoint
# -----------------------
@app.route('/event/<int:event_id>/buy_ticket', methods=['POST'])
def buy_ticket(event_id):
    attendee_name = request.form.get('attendee_name')
    if not attendee_name:
        return redirect(url_for('event_details', event_id=event_id))
    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Tickets (EventID, AttendeeName) VALUES (%s, %s)",
                    (event_id, attendee_name)
                )
                connection.commit()
        return redirect(url_for('event_details', event_id=event_id))
    except pymysql.Error as e:
        return render_template('error.html', error_message=str(e))

# -----------------------
# Add Event
# -----------------------
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VenueID, VenueName FROM Venues")
                venues = cursor.fetchall()
                cursor.execute("SELECT OrganizerID, OrganizerName FROM Organizers")
                organizers = cursor.fetchall()
    except pymysql.Error as e:
        return render_template('error.html', error_message=str(e))

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
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Events 
                        (EventName, EventDate, StartTime, EndTime, Description, Status, Budget, VenueID, OrganizerID)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (event_name, event_date, start_time, end_time, description, status, budget, venue_id, organizer_id))
                    connection.commit()
            return redirect(url_for('index'))
        except pymysql.Error as e:
            return render_template('error.html', error_message=str(e))

    return render_template('add_event.html', venues=venues, organizers=organizers)

# -----------------------
# JSON API for Event Details (for VR / Mastodon)
# -----------------------
@app.route('/event/<int:event_id>/json')
def event_details_json(event_id):
    try:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Events WHERE EventID = %s", (event_id,))
                event = cursor.fetchone()
                
                if not event:
                    return jsonify({})
                
                # Fetch tickets
                cursor.execute("SELECT * FROM Tickets WHERE EventID = %s", (event_id,))
                tickets = cursor.fetchall()
                
                return jsonify({
                    'EventDetails': event,
                    'Tickets': tickets
                })
    except pymysql.Error as e:
        return jsonify({'error': str(e)})

# -----------------------
# Global Error Handler
# -----------------------
@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html', error_message=str(e))

# -----------------------
# Run Flask App
# -----------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)