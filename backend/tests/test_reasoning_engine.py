from app.schemas.reasoning import ReasoningAnalysisRequest
from app.services.reasoning_engine import ReasoningEngine
from app.services.seed_repository import get_seed_cases, get_seed_students


def test_reasoning_engine_detects_basic_science_gaps() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_basic_001")
    clinical_case = get_seed_cases()[0]
    request = ReasoningAnalysisRequest(
        student=student,
        clinical_case=clinical_case,
        student_response="This might be reflux because chest discomfort is common.",
    )

    result = ReasoningEngine().analyze(request)

    assert result.likely_knowledge_gaps
    assert result.cognitive_bias_risk.bias == "cierre prematuro"
    assert "caso adaptativo" in result.next_recommended_activity


def test_reasoning_engine_gives_intern_targeted_gap() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_intern_001")
    clinical_case = get_seed_cases()[0]
    request = ReasoningAnalysisRequest(
        student=student,
        clinical_case=clinical_case,
        student_response=(
            "Possible ACS with exertional chest pressure, radiation to left arm, "
            "diaphoresis, and cardiovascular risk factors. I need ECG and serial troponins."
        ),
    )

    result = ReasoningEngine().analyze(request)

    assert any(gap.concept_id == "troponin_kinetics" for gap in result.likely_knowledge_gaps)
    assert result.cognitive_bias_risk.risk_level == "low"


def test_reasoning_engine_recognizes_spanish_chest_pain_paraphrases() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_clinical_001")
    clinical_case = get_seed_cases()[0]
    request = ReasoningAnalysisRequest(
        student=student,
        clinical_case=clinical_case,
        student_response=(
            "Paciente con dolor torácico opresivo de esfuerzo, irradiado al brazo izquierdo y "
            "asociado con diaforesis. Priorizo síndrome coronario agudo y solicitaría ECG inmediato."
        ),
    )

    result = ReasoningEngine().analyze(request)

    evidence = {item.criterion: item for item in result.clinical_evidence}
    assert evidence["exertional chest pressure"].detected is True
    assert evidence["radiation to left arm"].detected is True
    assert evidence["diaphoresis"].detected is True
    assert evidence["cardiovascular risk factors"].detected is False
    assert result.red_flag_coverage == 0.75
    assert result.cognitive_bias_risk.risk_level == "low"
    assert "exertional chest pressure" not in result.reasoning_analysis
    assert "ciencias clínicas" in result.reasoning_analysis
    assert "Dolor torácico de esfuerzo en el servicio de urgencias" in result.reasoning_analysis
    assert "Reconociste la mayoría" in result.feedback


def test_reasoning_engine_does_not_credit_negated_red_flag() -> None:
    student = next(item for item in get_seed_students() if item.id == "stu_clinical_001")
    clinical_case = get_seed_cases()[0]
    request = ReasoningAnalysisRequest(
        student=student,
        clinical_case=clinical_case,
        student_response="Dolor torácico de esfuerzo, pero niega diaforesis.",
    )

    result = ReasoningEngine().analyze(request)

    evidence = {item.criterion: item for item in result.clinical_evidence}
    assert evidence["diaphoresis"].detected is False
