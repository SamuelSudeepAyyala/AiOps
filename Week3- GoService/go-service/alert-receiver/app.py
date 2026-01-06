from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
import os

app = Flask(__name__)

INCIDENT_DIR = os.environ.get("INCIDENT_DIR", " /incidents")
os.makedirs(INCIDENT_DIR, exist_ok=True)

@app.post("/alert")
def alert():
    payload = request.get_json(force=True, silent=True) or {}
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(INCIDENT_DIR, f"incident-{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    
    alerts = payload.get("alerts", [])
    names = [a.get("labels", {}).get("alertname", "unknown") for a in alerts]
    status = payload.get("status", "unknown")
    print(f"[ALERT RECEIVED] status={status} alerts={names} saved={path}", flush=True)
    
    return jsonify({"ok": True, "saved": path})