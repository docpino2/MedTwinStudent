from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ClinicalCase(Base):
    __tablename__ = "clinical_cases"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    domain: Mapped[str] = mapped_column(String(80), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    setting: Mapped[str] = mapped_column(String(120), nullable=False)
    stem: Mapped[str] = mapped_column(Text, nullable=False)
    patient_age: Mapped[int]
    patient_sex: Mapped[str] = mapped_column(String(40), nullable=False)
    vitals: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    findings: Mapped[list[str]] = mapped_column(JSON, default=list)
    required_concepts: Mapped[list[str]] = mapped_column(JSON, default=list)
    red_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    expected_reasoning_steps: Mapped[list[str]] = mapped_column(JSON, default=list)

