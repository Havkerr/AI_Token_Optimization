# AI Model Comparison Tool — Phase 1

Send one prompt to several Gemini models side by side and capture cost, token usage,
latency, and human Good/Bad ratings for each response. See [Phase1.txt](Phase1.txt) for
the full spec this implements.

Compares three models on a cheap/mid/premium price spread via the
[Gemini API](https://ai.google.dev): `gemini-2.5-flash-lite`, `gemini-2.5-flash`,
`gemini-2.5-pro`. Unlike a free local model, these have real per-token pricing, so the
cost comparison the app reports is actually meaningful.

## Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL, talking to the Gemini API
- **Frontend**: React + TypeScript + Vite
- **Infra**: Docker Compose (Postgres + backend); frontend runs locally via `npm run dev`

## Prerequisites

- Docker Desktop (for Postgres)
- Python 3.12+ (a venv is recommended)
- Node.js 18+
- A [Gemini API key](https://aistudio.google.com/apikey) (Google AI Studio)

## Setup

### 1. Configure your API key

```
cp .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY=...`. This file is used by Docker Compose and is
gitignored — never commit it.

### 2. Start Postgres

```
docker compose up -d postgres
```

### 3. Run the backend

```
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env          # then fill in GEMINI_API_KEY
uvicorn app.main:app --reload --port 8000
```

The backend creates its tables automatically on startup. Check `http://localhost:8000/health`.

### 4. Run the frontend

```
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The dev server proxies `/api` requests to the backend on
port 8000, so the frontend never sees the API key.

## Running everything with Docker Compose

`docker compose up -d postgres` starts just the database, which is the fastest loop for
local development (backend/frontend run natively with hot reload). To also run the
backend in a container:

```
docker compose up -d
```

This builds `backend/Dockerfile` and connects it to the `postgres` service using the
`GEMINI_API_KEY` from your shell/`.env`. The frontend is not containerized — keep
running it with `npm run dev`.

## Project layout

```
backend/app/
  main.py              FastAPI app, CORS, startup table creation
  config.py             Env vars + centralized model pricing table
  models.py              SQLAlchemy models: Prompt, ModelRun, Feedback
  providers/               Model abstraction (base.py) + Gemini implementation
  services/                 Cost calculation + comparison orchestration
  routers/                   /api/comparisons, /api/feedback, /api/dashboard

frontend/src/
  pages/                ComparePage, DashboardPage
  components/            PromptForm, ResultCard, ComparisonSummary, HistoryTable, ...
  api/client.ts            Typed fetch wrappers to the backend
```

## Notes

- **Pricing**: `backend/app/config.py` has per-token prices checked against
  [Gemini's pricing page](https://ai.google.dev/gemini-api/docs/pricing) in September
  2026. Confirm current rates there before trusting cost figures, since providers change
  pricing over time — `gemini-2.5-pro`'s rate also step up for prompts over 200k tokens,
  which isn't modeled here.
- **Error handling**: if a model call fails (e.g. missing/invalid API key, rate limit),
  that model's run is saved with `status: "error"` and the comparison still returns
  results for the models that succeeded.
- Out of scope for Phase 1: authentication, semantic caching, model routing/recommendations,
  RAG, production deployment. See section 14 of [Phase1.txt](Phase1.txt).
