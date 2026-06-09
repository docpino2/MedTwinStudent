# MedTwin Student

Digital twin MVP for simulating medical student learning trajectories across basic sciences, clinical sciences, and internship.

The prototype focuses on one initial clinical domain, chest pain, and is structured so each module can be expanded independently.

## Stack

- Backend: FastAPI
- Frontend: Next.js
- Database: PostgreSQL
- Optional vector layer: pgvector
- AI integration: OpenAI-compatible API
- Deployment targets: Render backend, Vercel frontend

## Core Modules

1. Student Profile Engine
2. Curriculum Knowledge Graph
3. Clinical Case Generator
4. Socratic Tutor Agent
5. Assessment Engine
6. Learning Simulation Engine
7. Teacher Dashboard

## Repository Layout

```text
MedTwinStudent/
  backend/
    app/
      api/v1/          FastAPI routers
      core/            Settings and database plumbing
      models/          SQLAlchemy persistence models
      schemas/         Pydantic request/response contracts
      services/        Domain services and AI adapters
    db/
      schema.sql       PostgreSQL schema with optional pgvector
      seeds/           MVP seed data
    tests/
  frontend/
    app/               Next.js App Router pages
    components/        UI components
    lib/               API client and types
  infra/               Local and deployment infrastructure
  docs/                Architecture notes
```

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:3000`

### Database

```bash
docker compose -f infra/docker-compose.yml up -d db
psql "$DATABASE_URL" -f backend/db/schema.sql
psql "$DATABASE_URL" -f backend/db/seeds/001_chest_pain.sql
```

## MVP Reasoning Endpoint

`POST /api/v1/reasoning/analyze`

Receives a student profile and clinical case, then returns:

- reasoning analysis
- likely knowledge gaps
- cognitive bias risk
- feedback
- next recommended activity

The first implementation is deterministic and transparent, with an OpenAI-compatible adapter ready for enrichment when `OPENAI_API_KEY` is configured.

