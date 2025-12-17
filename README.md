# Realtime AI Backend Project

This is a simple real-time AI backend project created for assignment submission.

The project demonstrates:
- Real-time communication using WebSockets
- Handling user and AI messages
- Storing data in Supabase
- Generating a session summary after the chat ends

UI is kept minimal as the focus is on backend functionality.

---

## Technology Used

- Python
- FastAPI
- WebSockets
- Supabase (PostgreSQL)
- HTML and JavaScript

---

## Project Structure

realtime-ai-backend/
- app/
  - main.py
  - database.py
  - llm.py
  - tasks.py
- frontend/
  - index.html
- requirements.txt
- .env
- README.md

---

## How to Run the Project

### Step 1: Create virtual environment
python -m venv venv

Activate the environment: venv\Scripts\activate

### Step 2: Install dependencies
pip install -r requirements.txt

### Step 3: Setup Supabase

Create a `.env` file in the root folder and add:
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

### Step 4: Run the backend
python -m uvicorn app.main:app --reload

Backend will start at:
http://127.0.0.1:8000

## WebSocket Endpoint

ws://127.0.0.1:8000/ws/session/{session_id}

- User sends a message
- AI sends a response
- All messages are saved in Supabase

---

## Supabase Database Tables

create table sessions (
session_id text primary key,
start_time timestamp,
end_time timestamp,
summary text
);

create table session_events (
id uuid primary key default gen_random_uuid(),
session_id text,
role text,
message text,
created_at timestamp default now()
);