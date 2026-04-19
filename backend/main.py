from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=[""],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_json(file_name):
    with open(os.path.join(DATA_DIR, file_name), "r") as f:
        return json.load(f)

def parse_datetime(date_str, time_str=None):
    try:
        if time_str:
            return datetime.fromisoformat(f"{date_str}T{time_str}".replace("Z", ""))
        return datetime.fromisoformat(date_str.replace("Z", ""))
    except Exception:
        return None

def reconcile(crm_events, calendar_events):
    unified = []
    used_calendar = set()

    for crm in crm_events:
        crm_dt = parse_datetime(crm["meeting_date"], crm.get("meeting_time"))
        crm_company = (crm.get("client_company") or "").lower()

        match = None

        for cal in calendar_events:
            if cal["event_id"] in used_calendar:
                continue

            cal_dt = datetime.fromisoformat(cal["start_time"].replace("Z", ""))
            same_date = crm["meeting_date"] in cal["start_time"]
            company_match = crm_company and crm_company in cal["title"].lower()

            time_ok = True
            if crm_dt:
                time_ok = abs((cal_dt - crm_dt).total_seconds()) <= 3600

            if same_date and company_match and time_ok:
                match = cal
                break

        meeting = {
            "title": match["title"] if match else crm["subject"],
            "start_time": match["start_time"] if match else crm_dt.isoformat() if crm_dt else None,
            "client_company": crm.get("client_company"),
            "location": {
                "value": match["location"] if match else crm.get("location"),
                "calendar": match["location"] if match else None,
                "crm": crm.get("location"),
                "conflict": bool(match and crm.get("location") and crm.get("location") != match["location"]),
                "source": "calendar" if match else "crm"
            },
            "sources": {
                "crm": crm["crm_id"],
                "calendar": match["event_id"] if match else None
            },
            "conflicts": [],
            "match_confidence": "high" if match else "low"
        }

        if meeting["location"]["conflict"]:
            meeting["conflicts"].append("location")

        unified.append(meeting)

        if match:
            used_calendar.add(match["event_id"])

    return unified

crm_data = load_json("crm_events.json")
calendar_data = load_json("calendar_events.json")
MEETINGS = reconcile(crm_data, calendar_data)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/meetings")
def get_meetings():
    return [
        {
            "id": i,
            "title": m["title"],
            "start_time": m["start_time"],
            "client_company": m["client_company"],
            "conflicts": m["conflicts"]
        }
        for i, m in enumerate(MEETINGS)
    ]

@app.get("/api/meetings/{meeting_id}")
def get_meeting(meeting_id: int):
    return MEETINGS[meeting_id]