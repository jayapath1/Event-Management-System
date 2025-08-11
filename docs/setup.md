# Setup Guide for Event Management System (EMS)

## 1. Prerequistes

Before you begin, ensure you have the following installed on your machine:
- **Python 3.x**
- **Flask**: `pip install Flask`
- **MySQL Server**: Community Edition is fine. Ensure you have MySQL server installed and running.
- **pymysql**: `pip install pymysql`

## 2. Clone the Repository

Open your terminal/command prompt and run:
git clone https://github.com/your-username/Event-Management-System.git
cd Event-Management-System

## 3. Configuring MySQL Database

Ensure your MySQL server is running locally You can verify by running:
**mysql -u root -p**

Create the EMS database:
**CREATE DATABASE EMS;**

Exit MySQL:
**exit;**

Run the provided SQL script to set up tables and inital data:
**mysql -u root -p EMS < path/to/event_management.sql**: replace the path/to/ with the actual path to the sql file

## 4. Configure Database Connection

Check and update the database credential in app.py to match your MySQL setup:

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'EMS'

## 5. Run the flask application
**python app.py** 

By default, the app will run on:
http://127.0.0.1:5000

## 6. Login and Use the Application

Using the default credential to log in:
Username: 'ucp'
Password: 'ucp123'

View the list of events, and click on any event for detailed information.

Logout using the button in the header.

## Troubleshooting
MySQL Connection Issues:
- Ensure MySQL service is running
- Verify your credential in app.py
- Make sure the EMS database and tables exist
Python Package Error:
- Run **pip install -r requirements.txt**.