# Event Management System – API & Endpoint Documentation

## Base URL
```
http://<EMS_SERVER_IP>:5000
```
## 1. Authentication & Sessions

# Login
* **URL:** `/login`
* **Method:** `GET / POST`
* **Description:** Logs a user in (manager or customer).
* **Request Parameters (POST):**

  * `username` – Username (`ucp` or `customer`)
  * `password` – Password (`ucp123` or `cust123`)
* **Response:**

  * On success: redirects to `/` (event listing)
  * On failure: renders `login.html` with error message

# Logout
* **URL:** `/logout`
* **Method:** `GET`
* **Description:** Clears session and logs user out.

## 2. Event Management

# Event Listing

* **URL:** `/`
* **Method:** `GET`
* **Description:** Shows all events in the system (requires login).

# Event Details

* **URL:** `/event_details/<int:event_id>`
* **Method:** `GET`
* **Description:** Shows detailed info about a specific event, including tickets, attendees, sessions, venues, sponsors, and social media promotions.

# Add Event

* **URL:** `/add_event`
* **Method:** `GET / POST`
* **Access:** Manager only
* **POST Parameters:**

  * `EventName`, `EventDate`, `StartTime`, `EndTime`, `Description`, `Status`, `Budget`, `VenueID`, `OrganizerID`
* **Description:** Adds a new event. Triggers automatic Mastodon announcement if integration is enabled.

# Delete Event

* **URL:** `/delete_event/<int:event_id>`
* **Method:** `POST`
* **Access:** Manager only
* **Description:** Deletes a specific event.

# Complete Event

* **URL:** `/complete_event/<int:event_id>`
* **Method:** `POST`
* **Description:** Marks event as completed and triggers wrap-up Mastodon post.

## 3. Ticket Management

# Buy Ticket

* **URL:** `/event_details/<int:event_id>/buy_ticket`
* **Method:** `POST`
* **Parameters:**

  * `attendee_name`, `attendee_email`, `attendee_phone`
* **Description:** Adds a ticket purchase and attendee registration. Triggers “low tickets” Mastodon post if remaining tickets ≤ threshold.

# Get Tickets

* **URL:** `/events/<int:event_id>/tickets`
* **Method:** `GET`
* **Response:** JSON array of tickets for the event.

## 4. Mastodon Integration

# Manual Mastodon Feed Fetch

* **URL:** `/api/mastodon_feed/<event_id>`
* **Method:** `GET`
* **Description:** Returns JSON of Mastodon posts related to the event (uses hashtag based on event name).

# Manual Mastodon Post

* **URL:** `/post_to_mastodon/<int:event_id>`
* **Method:** `POST`
* **Parameters:**

  * `message` – Post content
* **Description:** Sends a manual post to Mastodon and flashes confirmation.

## 5. Error Handling

* **All Endpoints:** Uses Flask error handler to catch exceptions. Renders `error.html` with `error_message`.

## 6. Notes

* **Session-based Access Control:** Some endpoints (add/delete events, mark complete) are manager-only.
* **Social Media Automation:** Mastodon integration triggers posts automatically on certain events (new event, low tickets, event completion).
* **Database Relations:**

  * `Events` → `Tickets` → `Attendees` → `Registrations`
  * `Events` → `Sessions` → `Speakers`
  * `Events` → `Venues`, `Organizers`, `Sponsors`, `SocialMediaPromotions`