from fastapi.testclient import TestClient

from app.main import app
from app.schemas.ai_health import AIHealthEvaluationRequest, AIUseIntent
from app.services.ai_health_competency_engine import AIHealthCompetencyEngine
from app.services.seed_repository import get_seed_cases, get_seed_students


def test_ai_health_competencies_are_cycle_aware() -> None:
    competencies = AIHealthCompetencyEngine().list_competencies()
    cycles = {competency.cycle for competency in competencies}

    assert "basic_sciences" in cycles
    assert "clinical_sciences" in cycles
    assert "internship" in cycles
    assert any("Privacidad" in competency.title for competency in competencies)


def test_ai_health_evaluation_detects_safe_clinical_prompt() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_clinical_001")
    clinical_case = get_seed_cases()[0]
    request = AIHealthEvaluationRequest(
        student=student,
        clinical_case=clinical_case,
        intent=AIUseIntent.DIFFERENTIAL_DIAGNOSIS,
        student_ai_prompt=(
            "Paciente de 58 años con dolor torácico de esfuerzo, irradiación al brazo izquierdo "
            "y diaforesis, sin datos identificables. Dame diagnóstico diferencial, causas "
            "peligrosas, red flags, discriminadores, límites e incertidumbre."
        ),
        ai_model_output="Podría ser SCA, reflujo o ansiedad.",
        student_critique=(
            "La salida puede omitir TEP o disección aórtica. Debo verificar con ECG, troponinas "
            "seriadas y guía clínica; no reemplaza mi juicio clínico."
        ),
        declared_uncertainty="Hay incertidumbre, pero el SCA debe priorizarse.",
        used_patient_identifiers=False,
        cited_sources_or_guidelines=True,
    )

    result = AIHealthCompetencyEngine().evaluate(request)

    assert result.overall_score >= 2.5
    assert "IA/Salud Digital" in result.digital_health_trajectory_note
    assert all(score.rationale for score in result.competency_scores)


def test_ai_health_evaluation_detects_privacy_and_overreliance_risk() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_intern_001")
    clinical_case = get_seed_cases()[0]
    request = AIHealthEvaluationRequest(
        student=student,
        clinical_case=clinical_case,
        intent=AIUseIntent.MANAGEMENT_PLANNING,
        student_ai_prompt="Dime el diagnóstico final de Juan Pérez con documento 123.",
        ai_model_output="El diagnóstico final es ansiedad.",
        student_critique="",
        used_patient_identifiers=True,
        escalated_to_human_supervisor=False,
    )

    result = AIHealthCompetencyEngine().evaluate(request)

    assert any(risk.risk == "riesgo de privacidad" for risk in result.detected_risks)
    assert any(risk.risk == "sobredependencia de IA" for risk in result.detected_risks)
    assert "checklist" in result.next_recommended_activity.lower()


def test_ai_health_endpoint_returns_spanish_outputs() -> None:
    client = TestClient(app)
    student = next(item for item in get_seed_students() if item.id == "stu_basic_001")

    response = client.post(
        "/api/v1/ai-health/evaluate",
        json={
            "student": student.model_dump(),
            "clinical_case": None,
            "intent": "learning_support",
            "student_ai_prompt": (
                "No estoy seguro del mecanismo. Sin datos identificables, explícame la isquemia "
                "miocárdica, pregúntame brechas y dame feedback."
            ),
            "ai_model_output": "La isquemia ocurre por desequilibrio entre demanda y aporte.",
            "student_critique": "Mi razonamiento debe verificar si entiendo el mecanismo y mi confianza.",
            "declared_uncertainty": "No estoy seguro del mecanismo celular.",
            "used_patient_identifiers": False,
            "cited_sources_or_guidelines": False,
            "escalated_to_human_supervisor": False,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "Fortalece" in body["feedback"] or "Uso sólido" in body["feedback"]
    assert "Competencias IA/Salud Digital" in body["digital_health_trajectory_note"]

