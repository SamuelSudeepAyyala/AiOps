# 🚀 AIOps Engineering Lab

This repository documents my journey building a **modular, real-time AIOps platform** integrating **DevOps, observability, and AI**.

## 📚 Overview

This lab-based project is divided into weekly modules to cover core concepts of AIOps:
- Monitoring Stack (logs, metrics, dashboards)
- Log anomaly detection & classification
- AI-enhanced CI/CD workflows
- Kubernetes-based deployment automation
- Auto-remediation via ML/NLP models

---

## 📆 Weekly Modules

| Week | Module | Description |
|------|--------|-------------|
| 1️⃣ | [Week1 - Monitoring Stack](./Week1 - Monitoring Stack) | Prometheus + Grafana + Loki + Flask app |
| 2️⃣ | (Coming soon) Log Analyzer | Train and deploy AI models for log classification |
| 3️⃣ | (Planned) CI/CD Automation | GitHub Actions with AI-triggered decision points |
| 4️⃣ | (Planned) Kubernetes Infra | Helm-based K8s deployment of AIOps pipeline |

---

## 🧠 Stack Highlights

- **Python Flask** microservices
- **Prometheus, Grafana, Loki** for observability
- **Docker Compose** orchestration
- **scikit-learn**, **Hugging Face**, **OpenAI** for AI
- Optional: **Kubernetes**, **Azure DevOps**, **Slack Bots**

---

## 🛠️ How to Run (Week 1)

```bash
cd week1-observability/docker
docker-compose up --build
