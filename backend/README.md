# MedTwin Student Backend

FastAPI service for student profiles, curriculum concepts, clinical cases, and reasoning analysis.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Test

```bash
python -m pytest
```

## Initialize Database

```bash
python -m app.db_init
```

## Main Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/reasoning/analyze \
  -H "Content-Type: application/json" \
  --data @sample_request.json
```
