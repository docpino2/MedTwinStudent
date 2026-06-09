import json
from functools import lru_cache
from pathlib import Path

from app.schemas.case import ClinicalCase
from app.schemas.curriculum import CurriculumConcept
from app.schemas.student import StudentProfile

SEED_DIR = Path(__file__).resolve().parents[2] / "db" / "seeds"


def _load_json(filename: str) -> list[dict]:
    with (SEED_DIR / filename).open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache
def get_seed_students() -> list[StudentProfile]:
    return [StudentProfile.model_validate(item) for item in _load_json("students.json")]


@lru_cache
def get_seed_cases() -> list[ClinicalCase]:
    return [ClinicalCase.model_validate(item) for item in _load_json("clinical_cases.json")]


@lru_cache
def get_seed_concepts() -> list[CurriculumConcept]:
    return [CurriculumConcept.model_validate(item) for item in _load_json("curriculum_concepts.json")]

