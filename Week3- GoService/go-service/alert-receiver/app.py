from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
import os
import subprocess
import requests
import requests_unixsocket

app = Flask(__name__)

INCIDENT_DIR = os.environ.get("INCIDENT_DIR", " ./incidents")
PROM_URL = os.environ.get("PROM_URL", "http://prometheus:9090")
TARGET_CONTAINER = os.environ.get("TARGET_CONTAINER", "go-service")

os.makedirs(INCIDENT_DIR, exist_ok=True)

def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def docker_logs_tail(container_name: str, lines: int=100) -> str:
    try:
        session = requests_unixsocket.Session()
        # Docker socket base URL must be URL-encoded:
        base = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
        url = f"{base}/containers/{container_name}/logs"
        params = {"stdout": 1, "stderr": 1, "tail": lines}
        r = session.get(url, params=params, timeout=3)
        r.raise_for_status()
        text = r.text.strip()
        return text if text else "[no_logs]"
    except Exception as e:
        return f"[log_error] {e}"


def prom_query(query:str):
    try:
        r = requests.get(f"{PROM_URL}/api/v1/query", params={"query": query}, timeout=3)
        r.raise_for_status()
        return r.json()
    except Exception as e :
        return {"error": str(e), "query": query}

def build_enrichment():
    snapshots = {
        "up_go_service" : prom_query('up{job="go-service"}'),
        "req_rate_by_path" : prom_query('sum by (path) (rate(http_requests_total[1m]))'),
        "p95_latency_by_path": prom_query('histogram_quantile(0.95, sum by (le, path) (rate(http_request_duration_seconds_bucket[5m])))'),
    }
    return snapshots

@app.post("/alert")
def alert():
    payload = request.get_json(force=True, silent=True) or {}
    ts = utc_stamp()
    
    path = os.path.join(INCIDENT_DIR, f"incident-{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    
    logs = docker_logs_tail(TARGET_CONTAINER, lines=120)
    prom = build_enrichment()
    
    enriched_log = {
        "timestamp_utc": ts,
        "alertmanager_status": payload.get("status"),
        "alerts": payload.get("alerts", []),
        "enrichment": {
            "target_container": TARGET_CONTAINER,
            "container_logs_tail": logs,
            "prometheus_snapshots": prom,
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