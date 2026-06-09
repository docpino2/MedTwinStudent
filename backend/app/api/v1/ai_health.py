from fastapi import APIRouter

from app.schemas.ai_health import AIHealthCompetency, AIHealthEvaluationRequest, AIHealthEvaluationResponse
from app.services.ai_health_competency_engine import AIHealthCompetencyEngine

router = APIRouter()
engine = AIHealthCompetencyEngine()


@router.get("/competencies", response_model=list[AIHealthCompetency])
def list_ai_health_competencies() -> list[AIHealthCompetency]:
    return engine.list_competencies()


@router.post("/evaluate", response_model=AIHealthEvaluationResponse)
def evaluate_ai_health_competencies(request: AIHealthEvaluationRequest) -> AIHealthEvaluationResponse:
    return engine.evaluate(request)

