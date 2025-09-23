## Deployment – Event Management System + Mastodon

## 1. Clone Repository
```bash
git clone https://github.com/jayapath1/Event-Management-System
cd Event-Management-System
```

## 2. Build & Run with Docker
```bash
docker compose up --build
```
This will:
- Build backend (Flask/Python)
- Build frontend (HTML/JS)
- Start MySQL database

## 3. Mastodon Local Tunnel
```bash
ssh -i ~/.ssh/mastodon.pem -L 3000:localhost:3000 ubuntu@mastodon.uoa.cloud
```
- Opens Mastodon API on `http://localhost:3000/home `

## 5. Mastodon Integration Test
Run Python test script:
```bash
python mastodon_test.py
```
Expected output → event announcement posts to Mastodon.

## 6. EMS Web Frontend
```bash
ssh -i ~/.ssh/event-management-system.pem -L 5000:localhost:5000 ubuntu@event-management-system.uoa.cloud
```

## 7. Full Deployment Verification
1. Open frontend → `http://localhost:5000`
2. Create new event
3. Check Mastodon timeline for automatic post

---

✅ If all steps succeed → project is deployed & integrated!
