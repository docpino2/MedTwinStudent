from fastapi import APIRouter, HTTPException

from app.schemas.student import StudentProfile
from app.services.seed_repository import get_seed_students

router = APIRouter()


@router.get("", response_model=list[StudentProfile])
def list_students() -> list[StudentProfile]:
    return get_seed_students()


@router.get("/{student_id}", response_model=StudentProfile)
def get_student(student_id: str) -> StudentProfile:
    for student in get_seed_students():
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

