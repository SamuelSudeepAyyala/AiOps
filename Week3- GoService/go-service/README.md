# Go Service
**AIOps | Observability | Alerting | Incident Handling**

This repository documents a complete, hands-on journey of building a **production-style Go microservice** from scratch and incrementally evolving it into a **fully observable, alert-driven system**.

The focus is **not just learning Go**, but understanding how modern **DevOps / SRE / Platform Engineering teams** design services with:
- health checks
- metrics
- alerting
- incident generation
- containerized observability stacks

This project is part of the **AIOps – Intelligent Observability** learning path.

---

## Tech Stack

- **Go** – backend HTTP service
- **Prometheus** – metrics collection & alert evaluation
- **Alertmanager** – alert routing & notification handling
- **Docker & Docker Compose** – containerized runtime
- **Flask (Python)** – custom alert receiver
- **WSL / Remote Linux Server**

---

## High-Level Architecture

```
Go Service (:8080)
   ├── /healthz
   ├── /metrics
        ↓
Prometheus (:9090)
   ├── Scraping
   ├── Alert Rules
        ↓
Alertmanager (:9093)
   ├── Routing
   ├── Deduplication
        ↓
Alert Receiver (:5001)
   ├── Webhook Listener
   ├── Incident JSON Writer
```

---

## Repository Structure

```
go-service/
├── main.go
├── go.mod
├── go.sum
├── Dockerfile
├── docker-compose.yml
├── incidents/
│   └── incident-*.json
├── observability/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── rules/
│   │       └── go-service-alerts.yml
│   └── alertmanager/
│       └── alertmanager.yml
└── alert-receiver/
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```

---

## Environment & Go Setup

- Installed modern Go manually
- Fixed Go toolchain mismatch issues
- Configured GOPATH, GOROOT
- Initialized Go module
- Verified toolchain auto-upgrade behavior

### Commands Used
```bash
go version
go mod init go-service
go run .
```
#### Key Learnings

- Ubuntu package repositories ship outdated Go versions
- Go 1.21+ introduces automatic compiler toolchains
- All Go development should happen inside a module
- Tooling (gopls, Prometheus client) requires newer Go versions
---

## Basic Go HTTP Service

### Features Implemented
- Built HTTP server using net/http
- Implemented /healthz endpoint
- Added structured JSON responses
- Enabled logging
### Example Response
```bash
curl http://localhost:8080/healthz
```
```json
{
  "message": "ok",
  "time": "2026-01-05T18:30:00Z"
}
```
---

## Prometheus Metrics Integration

### Features Implemented

- `/metrics` endpoint using client_golang

- Custom metrics:

    - `http_requests_total`

    - `http_request_duration_seconds`

- HTTP middleware for instrumentation

- Labeling by path, method, and status

### Key Concepts Learned

- Prometheus does not auto-create metrics

- Metrics must be:
    - defined
    - registered
    - updated manually
- Middleware is the correct way to instrument HTTP services
- `/metrics` should not be self-instrumented

---

## Dockerization & Observability Stack

### Features Implemented

- Multi-stage Dockerfile for Go service
- Minimal runtime image
- Docker healthcheck using `/healthz`
- Docker Compose stack including:
    - Go service
    - Prometheus
    - Grafana

### Key Learnings

- Dockerfile syntax is strict (`CMD`, `HEALTHCHECK`)
- `CMD ["/binary"]` vs `CMD binary`
- Healthchecks must include required binaries (`curl`)
- Services communicate via Docker DNS names
- Prometheus scrapes by **service name**, not `localhost`

---

## Prometheus Alerting

### Features Implemented

- Custom alert rules for Go service
- GoServiceDown alert
- Rule evaluation tuning (for:)
- Fixed rule YAML structure issues
- Prometheus reload & validation

#### Example Alert Rule
```yaml
groups:
  - name: go-service-alerts
    rules:
      - alert: GoServiceDown
        expr: up{job="go-service"} == 0
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Go service is down"
          description: "The go-service has been unreachable for 30 seconds"
```

### Common Pitfalls Solved

- Incorrect YAML indentation
- Missing rule_files section
- Volume mount path mismatches
- Rule file parsing errors
---

## Alertmanager & Incident Receiver (AIOps Core)

### Features Implemented

- Alertmanager configuration and routing
- Webhook-based alert delivery
- Custom Flask-based alert receiver
- Incident JSON file creation
- Volume-mounted incident persistence
#### Alert Flow

```
Go Service stops
→ Prometheus alert fires
→ Alertmanager receives alert
→ Webhook POST to alert-receiver
→ Incident JSON file created
```
### Verified Behavior

- firing alerts generate incident files
- resolved alerts are delivered correctly
- Alertmanager successfully posts to receiver
- Incidents persist on host via volume mount
---

## How to Run

```bash
docker compose up -d --build
```

---
### Validate Services
```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/metrics
curl http://localhost:9090  # Prometheus
curl http://localhost:9093  # Alertmanager
curl http://localhost:5001  # Alert Receiver
```
---
### Planned Enhancements

- Alert deduplication & correlation
- Severity-based routing
- Grafana dashboards
- Kubernetes deployment
- Structured logging (Zap)
- OpenTelemetry tracing
- Incident enrichment & classification
---
### Author

**Samuel Sudeep Ayyala**
