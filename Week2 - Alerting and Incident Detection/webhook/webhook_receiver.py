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
        enriched_log = {
            "Alert": alert.get("labels", {}).get("alertname"),
            "Instance": alert.get("labels", {}).get("instance"),
            "Severity": alert.get("labels", {}).get("severity"),
            "Summary": alert.get("annotations", {}).get("summary"),
            "Description": alert.get("annotations", {}).get("description"),
            "Time Fired": alert.get("startsAt")
        }
        
        teams_message = {
            "text": f"🚨 *{enriched_log['Alert']}* on *{enriched_log['Instance']}*:\n"
                    f"- Severity: {enriched_log['Severity']}\n"
                    f"- Summary: {enriched_log['Summary']}\n"
                    f"- Description: {enriched_log['Description']}\n"
                    f"- Time: {enriched_log['Time Fired']}"
        }
        
        discord_message = f"Discord Post Trigger: \n"\
                  f" -  Alert : {alert.get('labels', {}).get('alertname')}\n" \
                  f" - Instance : {alert.get('labels', {}).get('instance')}\n" \
                  f" - Severity : {alert.get('labels', {}).get('severity')}\n" \
                  f" - Summary : {alert.get('annotations', {}).get('summary')}\n" \
                  f" - Time : {alert.get('startsAt')}"
        
        app.logger.info(f"Discord made message: \n{json.dumps(discord_message)}")
        requests.post(TEAMS_WEBHOOK_URL, json=teams_message)
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": discord_message})
        app.logger.info(f"{response}")
        app.logger.info(f"🚨 Webhook Alert Received:\n{enriched_log}")
        
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
