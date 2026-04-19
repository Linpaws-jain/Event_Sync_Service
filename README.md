# Event Sync Service – CRM & Calendar Reconciliation

## 📖 Overview
This project reconciles meeting data from two upstream systems:

- **CRM** → relationship and client context  
- **Calendar** → meeting execution details  

The service ingests both datasets, reconciles records that refer to the same real‑world meeting, and exposes a unified view via a FastAPI backend and a simple React frontend.  
Conflicts between sources are preserved and shown explicitly for transparency.

---

## ⚙️ How to Run with Docker

Navigate to your project root and Run both services with below one command

docker compose up --build

## Access services

Backend API → http://localhost:8000
Frontend UI → http://localhost:3000

Stop services  
Press Ctrl + C in the terminal, then clean up containers with below command:

docker compose down


## ⚙️ How to Run without Docker (seprately
)
### Backend (FastAPI)
1. Navigate to the backend folder:
   ```bash
   cd backend

2. Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install fastapi uvicorn

3. Start the backend:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

4. API will be available at:

Health check → http://localhost:8000/api/health

Meetings list → http://localhost:8000/api/meetings

Meeting detail → http://localhost:8000/api/meetings/{id}

### Frontend (React + Vite)

Navigate to the frontend folder:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

UI will be available at http://localhost:5173.

### Approach

Ingestion
1. JSON files loaded from /data.

2. CRM and Calendar records normalized into internal models.

3. Basic validation applied (missing time, malformed date, null fields).

### Normalization Rules

Calendar:

1. Parse start_time, end_time.

2. Lowercase title.

3. Keep attendees as list.

4. location as string.

CRM:

1. Combine meeting_date + meeting_time if time exists.

2. If meeting_time missing → set time_unknown = true.

3. Lowercase subject.

4. Keep client_name and client_company as‑is.

Timezone Assumption:  
"Z" suffix stripped, all times treated as naive/local.

### Reconciliation (Rule‑Based)
Records matched if:

Same date

CRM client/company name appears in calendar title

Meeting times within 60 minutes (or CRM time missing)

This deterministic approach ensures explainable results.

### Merge & Conflict Handling
Calendar is source of truth for:  
start/end time, attendees, virtual links

CRM is source of truth for:  
client company, relationship owner, meeting notes

When values differ, conflicts are explicitly shown.

API
GET /api/meetings → reconciled meeting list

GET /api/meetings/{id} → detailed view with conflicts and provenance

Frontend
Meeting list with conflict indicators

Detailed view showing which fields came from which system

### Data Quality Handling
CRM records with missing meeting time are matched (lower confidence).

Calendar events with missing location/description are preserved.

CRM records marked as cancelled are shown as conflicts if calendar shows confirmed.

Duplicate calendar events handled via best‑match selection.

### AI Assistance
AI was used for:

1. Designing reconciliation rules

2. Identifying data quality edge cases

3. Structuring implementation and documentation


### Time Spent
Approx. 4 hours:

Backend ingestion + reconciliation: ~1.5h

Frontend integration: ~1h

README + documentation: ~1h

### with more time
1. Add automated tests
2. Persist reconciled data to a database
3. Improve matching using fuzzy string scoring
4. Add pagination and filtering
