from pydantic import BaseModel, Field

from app.schemas.reasoning import ReasoningAnalysisResponse


class StartLearningSessionRequest(BaseModel):
    student_id: str
    case_version_id: str


class StartLearningSessionResponse(BaseModel):
    session_id: str
    student_id: str
    case_version_id: str
    status: str
    current_phase: str


class CoreAttemptRequest(BaseModel):
    student_id: str
    case_version_id: str
    session_id: str
    student_response: str = Field(min_length=1)
    confidence_before: float = Field(ge=0, le=1)
    confidence_after: float = Field(ge=0, le=1)
    elapsed_seconds: int = Field(ge=0, le=7200)
    hints_used: list[str] = Field(default_factory=list)


class MasteryEstimateView(BaseModel):
    competency_id: str
    estimated_mastery: float
    uncertainty: float
    evidence_count: int
    model_version: str
    explanation: str


class CoreAttemptResponse(BaseModel):
    attempt_id: str
    session_id: str
    reasoning: ReasoningAnalysisResponse
    mastery_estimates: list[MasteryEstimateView]
    evidence_event_ids: list[str]
    message: str

