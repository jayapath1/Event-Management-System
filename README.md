# Event Management System (EMS) 

## Overview
The **Event Management System (EMS)** is a web application built using **Flask** and **MySQL** to manage and display event details. It supports user authentication, viewing event details, and comprehensive information about each event such as attendees, venues, tasks, and more.

## Features
- User authentication (login/logout functionality).
- Dashboard to view upcoming events.
- Detailed event pages, including information on:
  - Venues
  - Attendees
  - Payments
  - Tickets
  - Live Event Announcements, and more!

## Project Structure
```
Event-Management-System/
│
├── app.py                 # Main Flask application
├── requirements.txt
├── static/
│   ├── style.css          # Main CSS file
│   └── styles.css         # Additional CSS file
├── templates/
│   ├── index.html         # Dashboard
│   ├── login.html         # Login page
│   ├── error.html         # Error page
│   └── event_details.html # Detailed event page
├── ems.sql                # SQL script to set up MySQL database
├── architecture_before.png
├── architecture_after.png
├── Dockerfile
├── docker-compose.yml
```

## Prerequisites
Make sure you have the following installed:
- **Docker**
- **Docker Compose**

## MySQL Setup Instructions

Before running the application, you need to set up the MySQL database.

### 1. MySQL Configuration in `app.py`

The MySQL connection details in `app.py` are:
```python
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'EMS'
```
**Ensure that your MySQL configuration matches these values**. If your credentials differ:
- Update the `app.config` section in `app.py` with your own MySQL host, username, password, and database name.

### 2. Running the SQL Script

To set up the database structure, follow these steps:
1. **Open MySQL Workbench** or use the **MySQL command line**.
2. **Run the provided SQL script** (`ems.sql`) to create the necessary tables for the system.

**Using MySQL command line**:
```bash
mysql -u root -p EMS < path_to_event_management.sql
```
This will create all the necessary tables like `Events`, `Attendees`, `Venues`, etc., based on the structure defined in the script.

## Running the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/jayapath1/Event-Management-System
   cd Event-Management-System
   ```
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Build and Run the container in Docker:
   ```bash
   docker-compose up --build
   ```
4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## ⚙️ Usage
1. **Login** using the credentials:
   - Username: `ucp`
   - Password: `ucp123`
2. View the list of events, and click on any event for detailed information.
3. Logout using the button in the header.
