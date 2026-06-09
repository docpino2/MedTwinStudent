from app.schemas.tutor import TutorTurnRequest
from app.services.seed_repository import get_seed_cases, get_seed_students
from app.services.socratic_tutor import SocraticTutorAgent


def test_basic_sciences_tutor_probes_mechanism() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_basic_001")
    clinical_case = get_seed_cases()[0]

    result = SocraticTutorAgent().generate_turn(
        TutorTurnRequest(
            student=student,
            clinical_case=clinical_case,
            latest_student_response="Exercise makes the heart hurt.",
        )
    )

    assert result.should_withhold_final_answer is True
    assert result.intent == "probe_mechanism"
    assert "mecanismo" in result.tutor_question.lower()
    assert "estudiante" in result.rationale_for_question.lower()


def test_clinical_sciences_tutor_detects_premature_closure() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_clinical_001")
    clinical_case = get_seed_cases()[0]

    result = SocraticTutorAgent().generate_turn(
        TutorTurnRequest(
            student=student,
            clinical_case=clinical_case,
            latest_student_response="This is probably reflux because he has nausea.",
        )
    )

    assert result.detected_biases
    assert result.detected_biases[0].bias == "premature_closure"
    assert "causas peligrosas" in result.tutor_question.lower()
    assert "explicación benigna" in result.detected_biases[0].evidence


def test_tutor_endpoint_returns_structured_turn() -> None:
    from fastapi.testclient import TestClient

    from app.main import app

    student = next(item for item in get_seed_students() if item.id == "stu_intern_001")
    clinical_case = get_seed_cases()[0]
    client = TestClient(app)

    response = client.post(
        "/api/v1/tutor/turn",
        json={
            "student": student.model_dump(),
            "clinical_case": clinical_case.model_dump(),
            "conversation": [],
            "latest_student_response": "I would get labs. If troponin is negative he can probably go home.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["should_withhold_final_answer"] is True
    assert body["teaching_style"] == "internship"
    assert body["rubric_feedback"]
    assert "seguro" in body["tutor_question"].lower() or "inseguro" in body["tutor_question"].lower()
