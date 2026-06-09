from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas.case import ClinicalCase
from app.schemas.common import LearningCycle
from app.schemas.student import StudentProfile


class TutorIntent(StrEnum):
    ELICIT_PROBLEM_REPRESENTATION = "elicit_problem_representation"
    PROBE_MECHANISM = "probe_mechanism"
    PROBE_DIFFERENTIAL = "probe_differential"
    PROBE_DATA_INTERPRETATION = "probe_data_interpretation"
    PROBE_MANAGEMENT = "probe_management"
    PROBE_SAFETY = "probe_safety"
    PROBE_REFLECTION = "probe_reflection"


class TutorMessage(BaseModel):
    role: str = Field(pattern="^(student|tutor)$")
    content: str


class TutorTurnRequest(BaseModel):
    student: StudentProfile
    clinical_case: ClinicalCase
    conversation: list[TutorMessage] = Field(default_factory=list)
    latest_student_response: str


class TutorKnowledgeGap(BaseModel):
    concept_id: str
    label: str
    severity: str = Field(pattern="^(low|moderate|high)$")
    evidence: str


class TutorBiasSignal(BaseModel):
    bias: str
    risk_level: str = Field(pattern="^(low|moderate|high)$")
    evidence: str
    debiasing_move: str


class RubricFeedback(BaseModel):
    criterion: str
    score: int = Field(ge=0, le=4)
    rationale: str
    next_step: str


class TutorToolCall(BaseModel):
    tool_name: str
    purpose: str
    inputs: dict[str, str | int | float | list[str]]


class TutorTurnResponse(BaseModel):
    teaching_style: LearningCycle
    intent: TutorIntent
    should_withhold_final_answer: bool
    tutor_question: str
    rationale_for_question: str
    detected_knowledge_gaps: list[TutorKnowledgeGap]
    detected_biases: list[TutorBiasSignal]
    rubric_feedback: list[RubricFeedback]
    suggested_tool_calls: list[TutorToolCall]
    stop_condition: str

