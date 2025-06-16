from flask import Flask, json, request, jsonify
import logging
from datetime import datetime
import requests,os

app = Flask(__name__)
logging.basicConfig(filename="alerts_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route('/', methods=['POST'])
def alert():
    alert_data = request.json
    for alert in alert_data.get('alerts', []):
        
        status = alert.get("status")
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        start_time = alert.get("startsAt", "")
        time_fired = datetime.fromisoformat(start_time.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        #Default values
        summary = annotations.get("summary", "No summary")
        description = annotations.get("description", "No description")
        instance = labels.get("instance", "unknown")
        alertname = labels.get("alertname", "unnamed")
        severity = labels.get("severity", "unknown")
        
        message = (
            f"- *Alert*: {alertname}\n"
            f"- *Instance*: {instance}\n"
            f"- *Severity*: {severity}\n"
            f"- *Time Fired*: {time_fired}\n"
            f"- *Summary*: {summary}\n"
            f"- *Description*: {description}\n"
            f"- *Status*: {status}"
        )
        
        
        requests.post(TEAMS_WEBHOOK_URL, json=message)
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        app.logger.info(f"🚨 Webhook Alert Received:\n{message}")
        
    return jsonify({"status": "received"}), 2000

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
