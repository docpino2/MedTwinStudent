from pydantic import BaseModel, Field

from app.schemas.case import ClinicalCase
from app.schemas.student import StudentProfile


class ReasoningAnalysisRequest(BaseModel):
    student: StudentProfile
    clinical_case: ClinicalCase
    student_response: str | None = Field(
        default=None,
        description="Optional free-text reasoning written by the learner.",
    )


class KnowledgeGap(BaseModel):
    concept_id: str
    concept_label: str
    severity: str
    rationale: str


class CognitiveBiasRisk(BaseModel):
    bias: str
    risk_level: str
    rationale: str


class ReasoningAnalysisResponse(BaseModel):
    reasoning_analysis: str
    likely_knowledge_gaps: list[KnowledgeGap]
    cognitive_bias_risk: CognitiveBiasRisk
    feedback: str
    next_recommended_activity: str
    tutor_prompt: str
    simulation_update: dict[str, float]

