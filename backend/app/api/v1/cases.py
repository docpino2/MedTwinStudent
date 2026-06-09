from fastapi import APIRouter, HTTPException

from app.schemas.case import ClinicalCase
from app.services.seed_repository import get_seed_cases

router = APIRouter()


@router.get("", response_model=list[ClinicalCase])
def list_cases(domain: str | None = None) -> list[ClinicalCase]:
    cases = get_seed_cases()
    if domain:
        return [case for case in cases if case.domain == domain]
    return cases


@router.get("/{case_id}", response_model=ClinicalCase)
def get_case(case_id: str) -> ClinicalCase:
    for clinical_case in get_seed_cases():
        if clinical_case.id == case_id:
            return clinical_case
    raise HTTPException(status_code=404, detail="Clinical case not found")

