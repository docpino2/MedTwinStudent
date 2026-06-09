from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas.curriculum import CurriculumConcept
from app.schemas.student import StudentProfile


class InterventionType(StrEnum):
    MECHANISM_MICRO_LESSON = "mechanism_micro_lesson"
    RETRIEVAL_PRACTICE = "retrieval_practice"
    CONCEPT_MAP_REPAIR = "concept_map_repair"
    ILLNESS_SCRIPT_COMPARISON = "illness_script_comparison"
    SOCRATIC_TUTORING = "socratic_tutoring"
    COGNITIVE_FORCING_CHECKLIST = "cognitive_forcing_checklist"
    CASE_CONTRAST_SET = "case_contrast_set"
    SIMULATION_RETRY = "simulation_retry"
    HANDOFF_REHEARSAL = "handoff_rehearsal"
    SUPERVISOR_REVIEW = "supervisor_review"


class SimulationWeights(BaseModel):
    performance: float = Field(default=0.28, ge=0, le=1)
    intervention: float = Field(default=0.22, ge=0, le=1)
    feedback_quality: float = Field(default=0.2, ge=0, le=1)
    time_spent: float = Field(default=0.15, ge=0, le=1)
    difficulty_alignment: float = Field(default=0.15, ge=0, le=1)
    max_positive_delta: float = Field(default=0.18, ge=0.01, le=0.5)
    max_negative_delta: float = Field(default=0.08, ge=0.01, le=0.5)
    gap_threshold: float = Field(default=0.7, ge=0, le=1)


class ClinicalCasePerformance(BaseModel):
    overall_score: float = Field(ge=0, le=1)
    concept_scores: dict[str, float] = Field(default_factory=dict)
    safety_score: float = Field(default=0.5, ge=0, le=1)
    reasoning_score: float = Field(default=0.5, ge=0, le=1)
    metacognition_score: float = Field(default=0.5, ge=0, le=1)


class SimulationRequest(BaseModel):
    student: StudentProfile
    competency_map: list[CurriculumConcept]
    baseline_mastery_scores: dict[str, float] = Field(default_factory=dict)
    clinical_case_performance: ClinicalCasePerformance
    intervention_type: InterventionType
    feedback_quality: float = Field(ge=0, le=1)
    time_spent_minutes: int = Field(ge=0, le=240)
    difficulty_level: int = Field(ge=1, le=5)
    weights: SimulationWeights = Field(default_factory=SimulationWeights)


class MasteryUpdate(BaseModel):
    concept_id: str
    concept_label: str
    baseline: float = Field(ge=0, le=1)
    updated: float = Field(ge=0, le=1)
    delta: float
    drivers: dict[str, float]


class RemainingGap(BaseModel):
    concept_id: str
    concept_label: str
    mastery: float = Field(ge=0, le=1)
    severity: str
    recommended_remediation: str


class LearningSimulationResponse(BaseModel):
    updated_mastery_scores: dict[str, float]
    mastery_updates: list[MasteryUpdate]
    predicted_risk_reduction: float = Field(ge=0, le=1)
    remaining_gaps: list[RemainingGap]
    recommended_next_activity: str
    learning_trajectory_summary: str
    model_config_used: SimulationWeights

