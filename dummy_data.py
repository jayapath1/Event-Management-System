from faker import Faker
import pymysql
import random
import sys

# ---------------- Configuration ----------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jayapath',
    'db': 'EMS',
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor
}

# Default number of fake tickets
NUM_TICKETS_TO_GENERATE = int(sys.argv[1]) if len(sys.argv) > 1 else 50

# ---------------- Initialize ----------------
fake = Faker()
connection = pymysql.connect(**DB_CONFIG)
cursor = connection.cursor()

# ---------------- Fetch Events ----------------
cursor.execute("SELECT EventID FROM Events")
events = cursor.fetchall()
event_ids = [event['EventID'] for event in events]

if not event_ids:
    print("❌ No events found in the database. Please add events first.")
    exit(1)

print(f"✅ Found {len(event_ids)} events. Generating {NUM_TICKETS_TO_GENERATE} fake tickets...")

# ---------------- Generate Data ----------------
created_tickets = []

for _ in range(NUM_TICKETS_TO_GENERATE):
    # Pick a random event
    event_id = random.choice(event_ids)

    # Generate fake attendee
    attendee_name = fake.name()
    attendee_email = fake.email()
    attendee_phone = fake.phone_number()

    # Insert attendee
    cursor.execute(
        "INSERT INTO Attendees (Name, Email, Phone) VALUES (%s, %s, %s)",
        (attendee_name, attendee_email, attendee_phone)
    )
    attendee_id = cursor.lastrowid

    # Generate ticket with purchase date
    purchase_date = fake.date_between(start_date='-1y', end_date='today')
    cursor.execute(
        "INSERT INTO Tickets (EventID, AttendeeID, PurchaseDate) VALUES (%s, %s, %s)",
        (event_id, attendee_id, purchase_date)
    )

    created_tickets.append({
        "EventID": event_id,
        "AttendeeName": attendee_name,
        "Email": attendee_email,
        "Phone": attendee_phone,
        "PurchaseDate": purchase_date.strftime("%Y-%m-%d")
    })

# ---------------- Commit & Close ----------------
connection.commit()
cursor.close()
connection.close()

# ---------------- Preview Output ----------------
print(f"🎉 Successfully generated {NUM_TICKETS_TO_GENERATE} tickets!")
print("Here are the first 5 records inserted:")
for ticket in created_tickets[:5]:
    print(ticket)