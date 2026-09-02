from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: new_id("session"))
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), nullable=False)
    case_version_id: Mapped[str] = mapped_column(ForeignKey("clinical_cases.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="iniciada", nullable=False)
    current_phase: Mapped[str] = mapped_column(String(80), default="diagnostico_integral", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class EvidenceEvent(Base):
    __tablename__ = "evidence_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: new_id("evidence"))
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), nullable=False)
    session_id: Mapped[str] = mapped_column(ForeignKey("learning_sessions.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    model_version: Mapped[str] = mapped_column(String(80), default="deterministic-core-v1", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class MasteryEstimate(Base):
    __tablename__ = "mastery_estimates"
    __table_args__ = (UniqueConstraint("student_id", "competency_id", name="uq_mastery_student_competency"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: new_id("mastery"))
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), nullable=False)
    competency_id: Mapped[str] = mapped_column(String, nullable=False)
    estimated_mastery: Mapped[float] = mapped_column(Float, nullable=False)
    uncertainty: Mapped[float] = mapped_column(Float, nullable=False)
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    model_version: Mapped[str] = mapped_column(String(80), default="deterministic-mastery-v1", nullable=False)
    explanation: Mapped[str] = mapped_column(Text, default="", nullable=False)
    last_observed_at: Mapped[datetime | None] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
