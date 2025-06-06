from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def alert():
    alert_data = request.json
    app.logger.info("🚨 Webhook Alert Received:")
    app.logger.info(alert_data)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
