## Deployment – Event Management System + Mastodon

## Machine Details
EMS Server
- Operating System - Ubuntu 22.04
- Instance type - 2 vCPUs, 4GB RAM
- Storage - 40GB 
- Ports - EMS (5000)
        - MySQL (3306 inside EMS VM)

Mastodon Server
- Operating System - Ubuntu 24.04 LTS
- Instance type - 2 vCPUs, 8GB RAM, 
- Storage - 60GB
- Ports - Mastodon (3000)

## Install Prerequisites on EMS Server
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y git docker.io docker-compose python3 python3-pip

# Verify installs
git --version
docker --version
docker-compose --version
python3 --version (Python 3.10+ recommended)
pip3 --version

## 1. Clone Repository
```bash
git clone https://github.com/jayapath1/Event-Management-System
cd Event-Management-System
```
## 2. Python setup
```bash
pip3 install -r requirements.txt
```

## 3. MySQL Setup Instructions
The MySQL connection details in `app.py` are:
```python
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'EMS'
```
# Running the SQL Script
To set up the database structure, follow these steps:
**Using MySQL command line**:
```bash
sudo service mysql start
mysql -u root -p
CREATE DATABASE EMS;
exit
mysql -u root -p EMS < ems.sql
```
This will create all the necessary tables like `Events`, `Attendees`, `Venues`, etc., based on the structure defined in the script.

## 4. Build & Run with Docker
```bash
docker compose up --build
```
This will:
- Build backend (Flask/Python)
- Build frontend (HTML/JS)
- Start MySQL database

Open frontend → `http://localhost:5000`

## 5. Mastodon Setup
1. Start the Mastodon Ronin VM.
2. Move the SSH key to your local machine:
```bash
mkdir -p ~/.ssh
mv mastodon.pem ~/.ssh/mastodon.pem
chmod 600 ~/.ssh/mastodon.pem
```

## 6. Mastodon Local Tunnel
```bash
ssh -i ~/.ssh/mastodon.pem -L 3000:localhost:3000 ubuntu@mastodon.uoa.cloud
```
- Open Mastodon API on `http://localhost:3000/home`

## 7. Configure Mastodon in EMS
Update config.json in the EMS project root:
{
  "MASTODON_BASE_URL": "http://localhost:3000",
  "MASTODON_ACCESS_TOKEN": "your_token_here"
}

## 8. Mastodon Integration Test
Run Python test script:
```bash
python mastodon_integration/mastodon_test.py
```
Expected output → event announcement posts to Mastodon.

## 9. Full Deployment Verification
1. Open frontend → `http://localhost:5000`
2. Create a new event
3. Check Mastodon timeline for automatic post
---
## 10. Login Credentials
# EMS 
- Default EMS credentials:
    - Username: ucp
    - Password: ucp123

- Customer Login:
    - Username: customer
    - Password: cust123

# Mastodon Instance
- Admin user:
    - Username: cyberlab
    - Email: cyberlab@localhost
    - Password: a4fa6df0281455cd916579b810d9387b
- Normal user:
    - Username: bob
    - Email: bob@localhost
    - Password: password
- Eventmanager (used by EMS to post automatically):
    - Username: eventmanager
    - Email: EventManager@localhost
    - Password: EventManager

## Important Files
- `mastodon_service.py`: Custom wrapper for Mastodon API (included in `mastodon_integration/`).
- `mastodon_test.py`: Script to manually test posting to Mastodon before enabling automatic posts. 
- `config.json`: Stores Mastodon base URL and access token.