# AI Model Comparison Tool — Phase 1

Send one prompt to several local models side by side and capture cost, token usage,
latency, and human Good/Bad ratings for each response. See [Phase1.txt](Phase1.txt) for
the full spec this implements.

Compares three models served locally through [Ollama](https://ollama.com): `llama3.2`,
`mistral`, `gemma2`. Running locally means no API key and no per-token cost — the app
still reports "estimated cost" per the spec's data model, it's just always $0 here.

## Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL, talking to a local Ollama server
- **Frontend**: React + TypeScript + Vite
- **Infra**: Docker Compose (Postgres + backend); frontend runs locally via `npm run dev`

## Prerequisites

- Docker Desktop (for Postgres)
- Python 3.12+ (a venv is recommended)
- Node.js 18+
- [Ollama](https://ollama.com/download) installed and running natively (not in Docker)

### Install Ollama and pull the models

```
ollama pull llama3.2
ollama pull mistral
ollama pull gemma2
```

Ollama listens on `http://localhost:11434` by default — leave it running in the
background (the desktop app or `ollama serve`) while using this tool.

## Setup

### 1. Start Postgres

```
docker compose up -d postgres
```

### 2. Run the backend

```
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env          # defaults already point at localhost:11434 / Postgres
uvicorn app.main:app --reload --port 8000
```

The backend creates its tables automatically on startup. Check `http://localhost:8000/health`.

### 3. Run the frontend

```
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The dev server proxies `/api` requests to the backend on
port 8000, so the frontend never talks to Ollama directly.

## Running everything with Docker Compose

`docker compose up -d postgres` starts just the database, which is the fastest loop for
local development (backend/frontend run natively with hot reload). To also run the
backend in a container:

```
docker compose up -d
```

This builds `backend/Dockerfile` and connects it to the `postgres` service. Since Ollama
runs natively on your machine rather than in Compose, the backend container reaches it at
`http://host.docker.internal:11434` (Docker Desktop only — set `OLLAMA_BASE_URL` in a
root `.env` if your setup differs). The frontend is not containerized — keep running it
with `npm run dev`.

## Project layout

```
backend/app/
  main.py              FastAPI app, CORS, startup table creation
  config.py             Env vars + centralized model pricing table
  models.py              SQLAlchemy models: Prompt, ModelRun, Feedback
  providers/               Model abstraction (base.py) + Ollama implementation
  services/                 Cost calculation + comparison orchestration
  routers/                   /api/comparisons, /api/feedback, /api/dashboard

frontend/src/
  pages/                ComparePage, DashboardPage
  components/            PromptForm, ResultCard, ComparisonSummary, HistoryTable, ...
  api/client.ts            Typed fetch wrappers to the backend
```

## Notes

- **Pricing**: `backend/app/config.py` centralizes per-token pricing per the spec; all
  three Ollama models are set to $0 since they run locally. If you later add a paid cloud
  provider, its real rates go in the same table — no other code needs to change.
- **Error handling**: if a model call fails (e.g. Ollama isn't running, or a model hasn't
  been pulled), that model's run is saved with `status: "error"` and the comparison still
  returns results for the models that succeeded.
- Out of scope for Phase 1: authentication, semantic caching, model routing/recommendations,
  RAG, production deployment. See section 14 of [Phase1.txt](Phase1.txt).
