from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.reasoning import ReasoningAnalysisRequest
from app.schemas.session import (
    CoreAttemptRequest,
    CoreAttemptResponse,
    StartLearningSessionRequest,
    StartLearningSessionResponse,
)
from app.services.learning_repository import LearningRepository
from app.services.reasoning_engine import ReasoningEngine

router = APIRouter()
reasoning_engine = ReasoningEngine()


@router.post("/start", response_model=StartLearningSessionResponse)
def start_learning_session(
    request: StartLearningSessionRequest,
    db: Session = Depends(get_db),
) -> StartLearningSessionResponse:
    repository = LearningRepository(db)
    student = repository.get_student_profile(request.student_id)
    clinical_case = repository.get_case(request.case_version_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    if clinical_case is None:
        raise HTTPException(status_code=404, detail="Caso clínico no encontrado")

    session = repository.create_session(request.student_id, request.case_version_id)
    return StartLearningSessionResponse(
        session_id=session.id,
        student_id=session.student_id,
        case_version_id=session.case_version_id,
        status=session.status,
        current_phase=session.current_phase,
    )


@router.post("/attempts/core", response_model=CoreAttemptResponse)
def submit_core_attempt(
    request: CoreAttemptRequest,
    db: Session = Depends(get_db),
) -> CoreAttemptResponse:
    repository = LearningRepository(db)
    session = repository.get_session(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    if session.student_id != request.student_id or session.case_version_id != request.case_version_id:
        raise HTTPException(status_code=409, detail="La sesión no corresponde al estudiante o caso enviado")

    student = repository.get_student_profile(request.student_id)
    clinical_case = repository.get_case(request.case_version_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    if clinical_case is None:
        raise HTTPException(status_code=404, detail="Caso clínico no encontrado")

    reasoning = reasoning_engine.analyze(
        ReasoningAnalysisRequest(
            student=student,
            clinical_case=clinical_case,
            student_response=request.student_response,
        )
    )
    attempt, evidence_events, mastery_estimates = repository.persist_core_attempt(request, reasoning)
    return CoreAttemptResponse(
        attempt_id=attempt.id,
        session_id=request.session_id,
        reasoning=reasoning,
        mastery_estimates=mastery_estimates,
        evidence_event_ids=[event.id for event in evidence_events],
        message="Intento core persistido y estimaciones del gemelo actualizadas con incertidumbre.",
    )

