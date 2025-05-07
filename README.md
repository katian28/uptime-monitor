# Uptime Monitor Server

A Python web server that monitors the uptime status of submitted URLs.

## Features
- Submit any URL via API
- Periodically checks URL availability every 30 seconds
- Returns current status and last-checked timestamp
- Lightweight and production-ready using Flask

## Endpoints
- `POST /add`: Add a new URL to monitor
- `GET /status`: Get current status of all monitored URLs
- `POST /_reset`: Clear all URLs (for testing)

## Setup
```bash
git clone https://github.com/your-username/uptime-monitor.git
cd uptime-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
