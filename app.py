from flask import Flask, request, jsonify
import requests
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Thread-safe access
lock = Lock()
urls = {}  # { url: {status: str, last_checked: str} }

def check_urls():
    with lock:
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                status = "up" if response.status_code == 200 else "down"
            except Exception as e:
                status = "down"
                logging.warning(f"Error checking {url}: {e}")
            urls[url]["status"] = status
            urls[url]["last_checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"Checked {url}: {status}")

@app.route("/add", methods=["POST"])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    with lock:
        urls[url] = {"status": "unknown", "last_checked": "never"}
    logging.info(f"Added {url} to monitoring list.")
    return jsonify({"message": f"Monitoring started for {url}"}), 201

@app.route("/status", methods=["GET"])
def status():
    with lock:
        return jsonify(urls)

@app.route("/_reset", methods=["POST"])
def reset():
    with lock:
        urls.clear()
    return jsonify({"message": "Reset complete"}), 200

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_urls, trigger="interval", seconds=30)
    scheduler.start()
    logging.info("Starting uptime monitor server on http://localhost:5000")
    app.run(debug=True, use_reloader=False, port= 5050)
