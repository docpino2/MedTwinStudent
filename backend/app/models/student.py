from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    cycle: Mapped[str] = mapped_column(String(40), nullable=False)
    current_rotation: Mapped[str | None] = mapped_column(String(120))
    mastery_level: Mapped[str] = mapped_column(String(40), nullable=False)
    strengths: Mapped[list[str]] = mapped_column(JSON, default=list)
    vulnerabilities: Mapped[list[str]] = mapped_column(JSON, default=list)
    knowledge_state: Mapped[list[dict]] = mapped_column(JSON, default=list)
    learning_preferences: Mapped[list[str]] = mapped_column(JSON, default=list)

