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
