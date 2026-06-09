from fastapi.testclient import TestClient

from app.main import app
from app.schemas.simulation import ClinicalCasePerformance, InterventionType, SimulationRequest
from app.services.learning_simulation_engine import LearningSimulationEngine
from app.services.seed_repository import get_seed_concepts, get_seed_students


def test_learning_simulation_updates_mastery_and_reports_gaps() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_intern_001")
    concepts = get_seed_concepts()
    request = SimulationRequest(
        student=student,
        competency_map=concepts,
        baseline_mastery_scores={"troponin_kinetics": 0.58},
        clinical_case_performance=ClinicalCasePerformance(
            overall_score=0.64,
            concept_scores={"troponin_kinetics": 0.42, "acs_risk_stratification": 0.72},
            safety_score=0.72,
            reasoning_score=0.68,
            metacognition_score=0.55,
        ),
        intervention_type=InterventionType.SOCRATIC_TUTORING,
        feedback_quality=0.86,
        time_spent_minutes=25,
        difficulty_level=3,
    )

    result = LearningSimulationEngine().simulate(request)

    assert "troponin_kinetics" in result.updated_mastery_scores
    assert result.updated_mastery_scores["troponin_kinetics"] >= 0.58
    assert result.predicted_risk_reduction > 0
    assert "Reducción de riesgo predicha" in result.learning_trajectory_summary
    assert result.recommended_next_activity


def test_learning_simulation_endpoint_returns_spanish_outputs() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_clinical_001")
    concepts = get_seed_concepts()
    client = TestClient(app)

    payload = {
        "student": student.model_dump(),
        "competency_map": [concept.model_dump() for concept in concepts],
        "baseline_mastery_scores": {
            "ecg_initial_interpretation": 0.45,
            "troponin_kinetics": 0.3,
        },
        "clinical_case_performance": {
            "overall_score": 0.52,
            "concept_scores": {
                "ecg_initial_interpretation": 0.48,
                "troponin_kinetics": 0.25,
            },
            "safety_score": 0.45,
            "reasoning_score": 0.5,
            "metacognition_score": 0.4,
        },
        "intervention_type": "case_contrast_set",
        "feedback_quality": 0.8,
        "time_spent_minutes": 30,
        "difficulty_level": 3,
    }

    response = client.post("/api/v1/simulation/simulate", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["remaining_gaps"]
    assert "Realizar" in body["recommended_next_activity"]
    assert "brechas" in body["learning_trajectory_summary"]

