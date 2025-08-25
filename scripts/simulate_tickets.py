# scripts/simulate_tickets.py

from faker import Faker
import pymysql
import random

# -----------------------
# Configuration
# -----------------------
DB_CONFIG = {
    'host': 'localhost',    # or 'db' if using Docker
    'user': 'root',
    'password': 'jayapath',
    'db': 'EMS',
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor
}

NUM_TICKETS_TO_GENERATE = 50  # total fake tickets

# -----------------------
# Initialize Faker
# -----------------------
fake = Faker()

# -----------------------
# Connect to Database
# -----------------------
connection = pymysql.connect(**DB_CONFIG)
cursor = connection.cursor()

# -----------------------
# Fetch existing event IDs
# -----------------------
cursor.execute("SELECT EventID FROM Events")
events = cursor.fetchall()
event_ids = [event['EventID'] for event in events]

if not event_ids:
    print("No events found in the database. Please add events first.")
    exit(1)

# -----------------------
# Generate Dummy Tickets
# -----------------------
for _ in range(NUM_TICKETS_TO_GENERATE):
    event_id = random.choice(event_ids)
    attendee_name = fake.name()
    
    cursor.execute(
        "INSERT INTO Tickets (EventID, AttendeeName) VALUES (%s, %s)",
        (event_id, attendee_name)
    )

connection.commit()
cursor.close()
connection.close()

print(f"{NUM_TICKETS_TO_GENERATE} dummy tickets generated successfully for events: {event_ids}")