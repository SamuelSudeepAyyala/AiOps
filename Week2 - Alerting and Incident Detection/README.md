# Week2 - Alerting and Incident Detection

## Overview

This module builds on the AIOps stack with **real-time alerting and incident handling** using:

- **Prometheus Alertmanager** for rule-based alert generation  
- **Gmail SMTP**, **Discord**, and **Microsoft Teams** for multi-channel notifications  
- **Flask Webhook Receiver** to log and forward alerts  
- **Loki + Promtail** for log-based alerting  
- GitHub Actions-based config validation

---

## 📦 Components

| Directory/File                     | Description                                               |
|-----------------------------------|-----------------------------------------------------------|
| `alertmanager/config.yml`         | Alertmanager config for email, webhook, Discord, Teams   |
| `rules/alert_rules.yml`           | Prometheus alert rules                                    |
| `webhook/`                        | Flask receiver for webhook alerts                         |
| `grafana/provisioning/`           | Dashboards and data sources pre-config                    |
| `prometheus/prometheus.yml`       | Prometheus scrape targets and rule loading                |
| `docker-compose.yml`              | Spins up all services                                     |
| `assets/`                         | Alert screenshots and Grafana panels                      |
| `validation-logs/`                | Text logs exported from alerts                            |

---

## 🛠️ Setup Instructions

### 1. Clone and Navigate

```bash
git clone https://github.com/SamuelSudeepAyyala/AiOps.git
cd "AiOps/Week2 - Alerting and Incident Detection"
```

### 2. Create .env with Gmail credentials

```bash
EMAIL_USERNAME=********@gmail.com
EMAIL_PASSWORD=app_password
EMAIL_RECEIVER=recipient@gmail.com
```

#### For webhook integrations (used inside webhook_receiver.py):

```
DISCORD_WEBHOOK_URL=discord_url
TEAMS_WEBHOOK_URL=teams_url
```

### 3. Run the Stack
```
docker-compose up --build
```
## 🔍 Endpoints

| Service        | URL                                            |
| -------------- | ---------------------------------------------- |
| Flask App      | [http://localhost:5000](http://localhost:5000) |
| Prometheus     | [http://localhost:9090](http://localhost:9090) |
| Alertmanager   | [http://localhost:9093](http://localhost:9093) |
| Grafana        | [http://localhost:3000](http://localhost:3000) |
| Webhook Viewer | [http://localhost:9000](http://localhost:9000) |

## 🔔 Alerting Rules

#### We defined multiple groups of alerts:

1. flask-app-alerts
2. system-resource-alerts
3. prometheus-health-alerts
4. flask-app-metrics-alerts
5. loki-log-rules


## 📧 Multi-Channel Notifications

Alertmanager now sends alerts to:

 - Gmail ✅

 - Webhook Flask App ✅

 - Microsoft Teams ✅

 - Discord ✅

Webhook receiver enriches and logs alerts.

📂 alerts_log.txt, webhook_logs.txt, and flask_logs.txt are exported for audit purposes.

## 🧪 GitHub CI Validations (auto)
- ✅ Docker Compose syntax check

- ✅ YAML linting

- ✅ Prometheus rules validation (promtool)

- ✅ Python syntax check for Flask & Webhook

- ✅ Grafana provisioning config check

- ✅ Alertmanager config validation

## 🖼️ Visual Output & Dashboards
🔄 Simulated High Latency Endpoint

/simulate-high-latency triggers latency-based alerts.

#### 📊 Prometheus Alerts
#### Prometheus alert pending status
![Prometheus Rule Pending](assets/pending_status.png)

#### Prometheus alert firing status
![Prometheus Rule Firing](assets/Firing_status.png)



## 🧾 Webhook Logs

![Webhook_logs_png](./assets/webhook_logs.png)

## 📩 Email Evidence

#### Email Alert Received  
![Email_Alert](./assets/alert_email_image.png)

## 📥 Teams & Discord Alerts

#### Teams Alert
![Teams_Alert](./assets/teams_alert_evidence.png)

#### Discord Alert
![Discord_Alert](./assets/discord_alert_evidence.png)

## 📈 Dashboards

### Loki Logs Alerting Dashboard

![Loki-Logs-Alert](./assets/Loki-logs-prometheus-status.png)

## ✅ Status Summary
- 🔔 Real-time alerting via multiple channels

- 🌐 Webhook integration with alert enrichment

- 📄 Centralized log export for alerts

- 📊 Grafana dashboards for metrics & logs

- 🧪 CI Validations to prevent config issues

