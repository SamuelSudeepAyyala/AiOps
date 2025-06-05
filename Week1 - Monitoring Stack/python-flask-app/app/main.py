from flask import Flask, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
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

REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint'])

@app.before_request
def log_and_count():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    app.logger.info(f"Request: {request.method} {request.path}")
    
@app.route('/')
def home():
    return 'Hello Samuel! From AiOps homepage', 200
    
@app.route('/health')
def health():
    return 'OK', 200

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
