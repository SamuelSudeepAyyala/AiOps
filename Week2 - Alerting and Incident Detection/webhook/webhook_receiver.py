from flask import Flask, request, jsonify
import logging 

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

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
        app.logger.info(f"🚨 Webhook Alert Received:\n{enriched_log}")
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
