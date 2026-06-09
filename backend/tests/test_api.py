from fastapi.testclient import TestClient

from app.main import app
from app.services.seed_repository import get_seed_cases, get_seed_students


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_reasoning_endpoint() -> None:
    payload = {
        "student": get_seed_students()[1].model_dump(),
        "clinical_case": get_seed_cases()[0].model_dump(),
        "student_response": "I would get an ECG and consider ACS because of diaphoresis and exertional symptoms.",
    }

    response = client.post("/api/v1/reasoning/analyze", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert "reasoning_analysis" in body
    assert "likely_knowledge_gaps" in body
    assert "next_recommended_activity" in body

