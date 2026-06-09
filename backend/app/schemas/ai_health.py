from enum import StrEnum

from pydantic import BaseModel, Field

from app.schemas.case import ClinicalCase
from app.schemas.common import LearningCycle
from app.schemas.student import StudentProfile


class AIHealthSkill(StrEnum):
    CLINICAL_QUESTION_FORMULATION = "clinical_question_formulation"
    RESPONSIBLE_PROMPTING = "responsible_prompting"
    AI_OUTPUT_CRITIQUE = "ai_output_critique"
    DIFFERENTIAL_REASONING_WITH_AI = "differential_reasoning_with_ai"
    SELF_REGULATED_AI_LEARNING = "self_regulated_ai_learning"
    PRIVACY_AND_GOVERNANCE = "privacy_and_governance"
    AGENT_ORCHESTRATION = "agent_orchestration"
    AI_AUGMENTED_METACOGNITION = "ai_augmented_metacognition"


class AIUseIntent(StrEnum):
    LEARNING_SUPPORT = "learning_support"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    MANAGEMENT_PLANNING = "management_planning"
    PATIENT_EDUCATION = "patient_education"
    SELF_ASSESSMENT = "self_assessment"
    AGENT_WORKFLOW = "agent_workflow"


class AIHealthCompetency(BaseModel):
    id: AIHealthSkill
    title: str
    cycle: LearningCycle
    description: str
    observable_behaviors: list[str]
    assessment_methods: list[str]
    common_failure_modes: list[str]
    ai_supported_interventions: list[str]


class AIHealthEvaluationRequest(BaseModel):
    student: StudentProfile
    clinical_case: ClinicalCase | None = None
    intent: AIUseIntent
    student_ai_prompt: str
    ai_model_output: str | None = None
    student_critique: str | None = None
    declared_uncertainty: str | None = None
    used_patient_identifiers: bool = False
    cited_sources_or_guidelines: bool = False
    escalated_to_human_supervisor: bool = False


class AIHealthCriterionScore(BaseModel):
    criterion: str
    score: int = Field(ge=0, le=4)
    rationale: str
    evidence: list[str] = Field(default_factory=list)
    next_step: str


class AIHealthRiskSignal(BaseModel):
    risk: str
    level: str = Field(pattern="^(bajo|moderado|alto|crítico)$")
    rationale: str
    mitigation: str


class AIHealthEvaluationResponse(BaseModel):
    cycle: LearningCycle
    overall_score: float = Field(ge=0, le=4)
    mastery_level: str
    competency_scores: list[AIHealthCriterionScore]
    detected_risks: list[AIHealthRiskSignal]
    emerging_competency_gaps: list[str]
    feedback: str
    recommended_remediation: list[str]
    next_recommended_activity: str
    digital_health_trajectory_note: str

