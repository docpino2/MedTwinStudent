from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.models import AssessmentAttempt, ClinicalCase, CurriculumConcept, Student
from app.services.seed_repository import get_seed_cases, get_seed_concepts, get_seed_students


def create_extensions() -> None:
    with engine.begin() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def seed_data() -> None:
    with Session(engine) as session:
        for student in get_seed_students():
            session.merge(
                Student(
                    id=student.id,
                    name=student.name,
                    cycle=student.cycle,
                    current_rotation=student.current_rotation,
                    mastery_level=student.mastery_level,
                    strengths=student.strengths,
                    vulnerabilities=student.vulnerabilities,
                    knowledge_state=[item.model_dump(mode="json") for item in student.knowledge_state],
                    learning_preferences=student.learning_preferences,
                )
            )

        for concept in get_seed_concepts():
            session.merge(
                CurriculumConcept(
                    id=concept.id,
                    label=concept.label,
                    domain=concept.domain,
                    cycle=concept.cycle,
                    prerequisites=concept.prerequisites,
                    learning_objectives=concept.learning_objectives,
                )
            )

        for clinical_case in get_seed_cases():
            session.merge(
                ClinicalCase(
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
            )

        session.commit()


def main() -> None:
    create_extensions()
    create_tables()
    seed_data()
    print("Base de datos inicializada con tablas y datos seed.")


if __name__ == "__main__":
    main()

