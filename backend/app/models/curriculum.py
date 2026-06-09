from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CurriculumConcept(Base):
    __tablename__ = "curriculum_concepts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    label: Mapped[str] = mapped_column(String(180), nullable=False)
    domain: Mapped[str] = mapped_column(String(80), nullable=False)
    cycle: Mapped[str] = mapped_column(String(40), nullable=False)
    prerequisites: Mapped[list[str]] = mapped_column(JSON, default=list)
    learning_objectives: Mapped[list[str]] = mapped_column(JSON, default=list)

