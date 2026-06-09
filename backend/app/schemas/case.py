from pydantic import BaseModel, Field


class ClinicalCase(BaseModel):
    id: str
    domain: str
    title: str
    setting: str
    stem: str
    patient_age: int
    patient_sex: str
    vitals: dict[str, str]
    findings: list[str]
    required_concepts: list[str]
    red_flags: list[str] = Field(default_factory=list)
    expected_reasoning_steps: list[str] = Field(default_factory=list)


class ClinicalCaseCreate(BaseModel):
    domain: str
    difficulty: str = "mvp"
    cycle: str | None = None

