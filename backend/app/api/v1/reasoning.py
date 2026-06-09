from fastapi import APIRouter

from app.schemas.reasoning import ReasoningAnalysisRequest, ReasoningAnalysisResponse
from app.services.reasoning_engine import ReasoningEngine

router = APIRouter()
engine = ReasoningEngine()


@router.post("/analyze", response_model=ReasoningAnalysisResponse)
def analyze_reasoning(request: ReasoningAnalysisRequest) -> ReasoningAnalysisResponse:
    return engine.analyze(request)

