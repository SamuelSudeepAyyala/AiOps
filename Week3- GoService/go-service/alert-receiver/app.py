from flask import Flask, request, jsonify
from datetime import datetime, timezone, timedelta
import json
import os
import requests

app = Flask(__name__)

INCIDENT_DIR = os.environ.get("INCIDENT_DIR", "incidents")
PROM_URL = os.environ.get("PROM_URL", "http://prometheus:9090")
LOKI_URL = os.environ.get("LOKI_URL", "http://loki:3100")

LOKI_QUERY = os.environ.get("LOKI_QUERY", '{compose_service="go-service"}')

os.makedirs(INCIDENT_DIR, exist_ok=True)

def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def prom_query(query:str):
    try:
        r = requests.get(f"{PROM_URL}/api/v1/query", params={"query": query}, timeout=3)
        r.raise_for_status()
        return r.json()
    except Exception as e :
        return {"error": str(e), "query": query}

def build_metrics_snapshot():
    snapshots = {
        "up_go_service" : prom_query('up{job="go-service"}'),
        "req_rate_by_path" : prom_query('sum by (path) (rate(http_requests_total[1m]))'),
        "p95_latency_by_path": prom_query('histogram_quantile(0.95, sum by (le, path) (rate(http_request_duration_seconds_bucket[5m])))'),
    }
    return snapshots

def loki_logs_last_minutes(minutes: int = 5, limit: int = 200) -> str:
    try:
        end = datetime.now(timezone.utc)
        start = end - timedelta(minutes=minutes)

        params = {
            "query": LOKI_QUERY,
            "start": int(start.timestamp() * 1_000_000_000),  # ns
            "end": int(end.timestamp() * 1_000_000_000),      # ns
            "limit": limit,
            "direction": "forward",
        }
        r = requests.get(f"{LOKI_URL}/loki/api/v1/query_range", params=params, timeout=5)
        r.raise_for_status()
        data = r.json()

        result = data.get("data", {}).get("result", [])
        lines = []
        for stream in result:
            for ts, line in stream.get("values", []):
                lines.append(line)

        return "\n".join(lines[-limit:]) if lines else "[no_loki_logs]"
    except Exception as e:
        return f"[loki_error] {e}"

@app.post("/alert")
def alert():
    payload = request.get_json(force=True, silent=True) or {}
    ts = utc_stamp()
    
    path = os.path.join(INCIDENT_DIR, f"incident-{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    
    enriched_log = {
        "timestamp_utc": ts,
        "alertmanager_status": payload.get("status"),
        "alerts": payload.get("alerts", []),
        "enrichment": {
            "loki": {
                "url": LOKI_URL,
                "query": LOKI_QUERY,
                "logs_last_5m": loki_logs_last_minutes(minutes=5, limit=200),
            },
            "prometheus_snapshots": build_metrics_snapshot(),
        },
        "raw_alertmanager_payload": payload,
    }
    
    enriched_path = os.path.join(INCIDENT_DIR, f"enriched-{ts}.json")
    with open(enriched_path, "w", encoding="utf-8") as f:
        json.dump(enriched_log, f, indent=2)
        
    alerts = payload.get("alerts", [])
    names = [a.get("labels", {}).get("alertname", "unknown") for a in alerts]
    status = payload.get("status", "unknown")
    print(f"[ALERT RECEIVED] status={status} alerts={names} raw={path} enriched={enriched_path}", flush=True)
    
    return jsonify({"ok": True, "raw": path, "enriched": enriched_path})