from pydantic import BaseModel, Field

from app.schemas.common import LearningCycle, MasteryLevel


class KnowledgeState(BaseModel):
    concept_id: str
    concept_label: str
    mastery: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    last_assessed_at: str | None = None


class StudentProfile(BaseModel):
    id: str
    name: str
    cycle: LearningCycle
    current_rotation: str | None = None
    mastery_level: MasteryLevel
    strengths: list[str] = Field(default_factory=list)
    vulnerabilities: list[str] = Field(default_factory=list)
    knowledge_state: list[KnowledgeState] = Field(default_factory=list)
    learning_preferences: list[str] = Field(default_factory=list)


class StudentProfileCreate(BaseModel):
    name: str
    cycle: LearningCycle
    current_rotation: str | None = None
    mastery_level: MasteryLevel = MasteryLevel.NOVICE

