# Week1 - Monitoring Stack

## Overview

This module contains the initial observability stack setup using a Flask application, Prometheus for metrics, and Docker Compose for orchestration.

## Components

- `flask-app/` : Python Flask application exposing a `/metrics` endpoint and request logging.
- `prometheus/` : Prometheus configuration to scrape the Flask app.
- `docker-compose.yml` : Brings up Flask app and Prometheus in containers.

## Setup Instructions

### 1. Clone the Repository
 
```bash
git clone https://github.com/<your-username>/AiOps.git
cd "AiOps/Week1 - Monitoring Stack"
```

### 2. Build and Run

```bash
docker-compose up --build
```

### 3. Access Endpoints

 - Flask App Health: http://localhost:5000/health

 - Flask App Metrics: http://localhost:5000/metrics

 - Prometheus UI: http://localhost:9090

 ### 4. Verify Prometheus Scraping

 - Navigate to Status > Targets in Prometheus UI

 - Ensure flask-app:5000 target shows as UP


## Status

✅ Completed setup of Flask app with Prometheus metrics\
✅ Configured Prometheus to scrape metrics from Flask app\
✅ Dockerized both services\
✅ Verified metrics in Prometheus UI