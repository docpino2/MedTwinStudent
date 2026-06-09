from pydantic import BaseModel, Field

from app.schemas.common import LearningCycle


class CurriculumConcept(BaseModel):
    id: str
    label: str
    domain: str
    cycle: LearningCycle
    prerequisites: list[str] = Field(default_factory=list)
    learning_objectives: list[str] = Field(default_factory=list)


class CurriculumGraph(BaseModel):
    concepts: list[CurriculumConcept]
    edges: list[tuple[str, str, str]]

