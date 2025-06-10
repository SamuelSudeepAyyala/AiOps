import time
from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/var/log/app.log")
    ]
)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint'])

REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Latency of HTTP requests', ['endpoint'])

@app.before_request
def log_and_count():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    app.logger.info(f"Request: {request.method} {request.path}")

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_latency(response):
    if hasattr(request, 'start_time'):
        resp_time = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.path).observe(resp_time)
    return response

@app.route('/')
def home():
    return 'Hello Samuel! From AiOps homepage', 200
    
@app.route('/health')
def health():
    return 'OK', 200

@app.route('/simulate-high-latency')
def high_latency():
    time.sleep(1)
    return jsonify({"status": "simulated high latency"}), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/login', methods=['POST'])
def login():
    app.logger.info("Login attempt received.")
    return "Login successful", 200

@app.route('/error')
def error():
    app.logger.error("An error occurred!")
    return "Simulated Error", 500

@app.route('/data')
def data():
    app.logger.info("Data requested")
    return {"data": [1, 2, 3]}, 200

@app.route('/log-error')
def log_error():
    app.logger.error("Simulated ERROR log for Loki alerting")
    return jsonify({"status": "logged error"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
