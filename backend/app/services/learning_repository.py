from datetime import datetime
from uuid import uuid4

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models import (
    AssessmentAttempt,
    ClinicalCase,
    EvidenceEvent,
    LearningSession,
    MasteryEstimate,
    Student,
)
from app.schemas.case import ClinicalCase as ClinicalCaseSchema
from app.schemas.common import LearningCycle, MasteryLevel
from app.schemas.reasoning import ReasoningAnalysisResponse
from app.schemas.session import CoreAttemptRequest, MasteryEstimateView
from app.schemas.student import StudentProfile


class LearningRepository:
    _runtime_schema_checked = False

    def __init__(self, db: Session) -> None:
        self.db = db
        self._ensure_runtime_schema()

    def _ensure_runtime_schema(self) -> None:
        if LearningRepository._runtime_schema_checked:
            return

        bind = self.db.get_bind()
        Base.metadata.create_all(
            bind=bind,
            tables=[
                LearningSession.__table__,
                EvidenceEvent.__table__,
                MasteryEstimate.__table__,
            ],
        )
        if bind.dialect.name == "postgresql":
            statements = [
                "ALTER TABLE assessment_attempts ADD COLUMN IF NOT EXISTS session_id TEXT REFERENCES learning_sessions(id)",
                "ALTER TABLE assessment_attempts ADD COLUMN IF NOT EXISTS confidence_before DOUBLE PRECISION",
                "ALTER TABLE assessment_attempts ADD COLUMN IF NOT EXISTS confidence_after DOUBLE PRECISION",
                "ALTER TABLE assessment_attempts ADD COLUMN IF NOT EXISTS elapsed_seconds INTEGER",
                "ALTER TABLE assessment_attempts ADD COLUMN IF NOT EXISTS hints_used JSON DEFAULT '[]'",
            ]
            for statement in statements:
                self.db.execute(text(statement))
            self.db.commit()

        LearningRepository._runtime_schema_checked = True

    def get_student_profile(self, student_id: str) -> StudentProfile | None:
        student = self.db.get(Student, student_id)
        if student is None:
            return None
        return StudentProfile(
            id=student.id,
            name=student.name,
            cycle=LearningCycle(student.cycle),
            current_rotation=student.current_rotation,
            mastery_level=MasteryLevel(student.mastery_level),
            strengths=student.strengths,
            vulnerabilities=student.vulnerabilities,
            knowledge_state=student.knowledge_state,
            learning_preferences=student.learning_preferences,
        )

    def get_case(self, case_version_id: str) -> ClinicalCaseSchema | None:
        clinical_case = self.db.get(ClinicalCase, case_version_id)
        if clinical_case is None:
            return None
        return ClinicalCaseSchema(
            id=clinical_case.id,
            domain=clinical_case.domain,
            title=clinical_case.title,
            setting=clinical_case.setting,
            stem=clinical_case.stem,
            patient_age=clinical_case.patient_age,
            patient_sex=clinical_case.patient_sex,
            vitals=clinical_case.vitals,
            findings=clinical_case.findings,
            required_concepts=clinical_case.required_concepts,
            red_flags=clinical_case.red_flags,
            expected_reasoning_steps=clinical_case.expected_reasoning_steps,
        )

    def create_session(self, student_id: str, case_version_id: str) -> LearningSession:
        session = LearningSession(student_id=student_id, case_version_id=case_version_id)
        self.db.add(session)
        self.db.flush()
        event = EvidenceEvent(
            student_id=student_id,
            session_id=session.id,
            event_type="learning_session_started",
            payload={"case_version_id": case_version_id, "status": session.status},
            model_version="session-v1",
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: str) -> LearningSession | None:
        return self.db.get(LearningSession, session_id)

    def persist_core_attempt(
        self,
        request: CoreAttemptRequest,
        reasoning: ReasoningAnalysisResponse,
    ) -> tuple[AssessmentAttempt, list[EvidenceEvent], list[MasteryEstimateView]]:
        attempt = AssessmentAttempt(
            id=str(uuid4()),
            student_id=request.student_id,
            session_id=request.session_id,
            clinical_case_id=request.case_version_id,
            student_response=request.student_response,
            confidence_before=request.confidence_before,
            confidence_after=request.confidence_after,
            elapsed_seconds=request.elapsed_seconds,
            hints_used=request.hints_used,
            score=self._score_from_reasoning(reasoning),
            reasoning_analysis=reasoning.model_dump(mode="json"),
        )
        self.db.add(attempt)

        events = [
            EvidenceEvent(
                student_id=request.student_id,
                session_id=request.session_id,
                event_type="core_attempt_submitted",
                payload={
                    "attempt_id": attempt.id,
                    "case_version_id": request.case_version_id,
                    "elapsed_seconds": request.elapsed_seconds,
                    "hints_used": request.hints_used,
                },
                model_version="attempt-v1",
            ),
            EvidenceEvent(
                student_id=request.student_id,
                session_id=request.session_id,
                event_type="confidence_reported",
                payload={
                    "attempt_id": attempt.id,
                    "confidence_before": request.confidence_before,
                    "confidence_after": request.confidence_after,
                },
                model_version="confidence-v1",
            ),
            EvidenceEvent(
                student_id=request.student_id,
                session_id=request.session_id,
                event_type="core_reasoning_observed",
                payload={
                    "attempt_id": attempt.id,
                    "gap_count": len(reasoning.likely_knowledge_gaps),
                    "bias": reasoning.cognitive_bias_risk.bias,
                    "risk_level": reasoning.cognitive_bias_risk.risk_level,
                },
                model_version="deterministic-core-v1",
            ),
        ]
        self.db.add_all(events)
        estimates = self._update_mastery_estimates(request, reasoning)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt, events, estimates

    def _update_mastery_estimates(
        self,
        request: CoreAttemptRequest,
        reasoning: ReasoningAnalysisResponse,
    ) -> list[MasteryEstimateView]:
        gap_ids = {gap.concept_id for gap in reasoning.likely_knowledge_gaps}
        observed_ids = set(reasoning.simulation_update)
        estimates: list[MasteryEstimateView] = []

        for concept_id in observed_ids:
            existing = self.db.scalar(
                select(MasteryEstimate).where(
                    MasteryEstimate.student_id == request.student_id,
                    MasteryEstimate.competency_id == concept_id,
                )
            )
            prior = existing.estimated_mastery if existing else reasoning.simulation_update.get(concept_id, 0.5)
            evidence_count = (existing.evidence_count if existing else 0) + 1
            observed_signal = 0.35 if concept_id in gap_ids else 0.75
            learning_rate = min(0.35, 1 / (evidence_count + 2))
            updated_mastery = self._clamp(prior * (1 - learning_rate) + observed_signal * learning_rate)
            uncertainty = self._clamp(max(0.08, 0.5 / (evidence_count + 1)))
            explanation = (
                f"Estado previo {prior:.0%}; evidencia del intento indica "
                f"{'brecha observada' if concept_id in gap_ids else 'desempeño suficiente'}; "
                f"modelo deterministic-mastery-v1 actualiza a {updated_mastery:.0%} "
                f"con incertidumbre {uncertainty:.0%}."
            )

            if existing:
                existing.estimated_mastery = updated_mastery
                existing.uncertainty = uncertainty
                existing.evidence_count = evidence_count
                existing.explanation = explanation
                existing.last_observed_at = datetime.utcnow()
                existing.updated_at = datetime.utcnow()
                row = existing
            else:
                row = MasteryEstimate(
                    student_id=request.student_id,
                    competency_id=concept_id,
                    estimated_mastery=updated_mastery,
                    uncertainty=uncertainty,
                    evidence_count=evidence_count,
                    model_version="deterministic-mastery-v1",
                    explanation=explanation,
                    last_observed_at=datetime.utcnow(),
                )
                self.db.add(row)

            estimates.append(
                MasteryEstimateView(
                    competency_id=concept_id,
                    estimated_mastery=updated_mastery,
                    uncertainty=uncertainty,
                    evidence_count=evidence_count,
                    model_version=row.model_version,
                    explanation=explanation,
                )
            )

        return sorted(estimates, key=lambda item: item.competency_id)

    def _score_from_reasoning(self, reasoning: ReasoningAnalysisResponse) -> float:
        penalty = len(reasoning.likely_knowledge_gaps) * 0.12
        risk_penalty = 0.12 if reasoning.cognitive_bias_risk.risk_level == "high" else 0.06
        return self._clamp(0.82 - penalty - risk_penalty)

    def _clamp(self, value: float) -> float:
        return round(max(0.0, min(1.0, value)), 4)
