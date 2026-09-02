from collections.abc import Generator
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models import ClinicalCase, CurriculumConcept, Student
from app.services.seed_repository import get_seed_cases, get_seed_concepts, get_seed_students


@contextmanager
def build_test_client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        for student in get_seed_students():
            session.add(
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
            session.add(
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
            session.add(
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

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_productive_core_attempt_uses_ids_and_persists_evidence() -> None:
    with build_test_client() as client:
        start_response = client.post(
            "/api/v1/sessions/start",
            json={"student_id": "stu_clinical_001", "case_version_id": "case_chest_pain_001"},
        )
        assert start_response.status_code == 200
        session_id = start_response.json()["session_id"]

        attempt_response = client.post(
            "/api/v1/sessions/attempts/core",
            json={
                "student_id": "stu_clinical_001",
                "case_version_id": "case_chest_pain_001",
                "session_id": session_id,
                "student_response": (
                    "Considero síndrome coronario agudo por dolor torácico de esfuerzo, "
                    "diaforesis y factores de riesgo. Solicito ECG y troponinas seriadas."
                ),
                "confidence_before": 0.45,
                "confidence_after": 0.68,
                "elapsed_seconds": 180,
                "hints_used": [],
            },
        )

        assert attempt_response.status_code == 200
        body = attempt_response.json()
        assert body["attempt_id"]
        assert len(body["evidence_event_ids"]) == 3
        assert body["mastery_estimates"]
        assert "incertidumbre" in body["mastery_estimates"][0]["explanation"]
        assert "persistido" in body["message"]


def test_productive_core_attempt_requires_confidence() -> None:
    with build_test_client() as client:
        start_response = client.post(
            "/api/v1/sessions/start",
            json={"student_id": "stu_basic_001", "case_version_id": "case_chest_pain_001"},
        )
        session_id = start_response.json()["session_id"]

        attempt_response = client.post(
            "/api/v1/sessions/attempts/core",
            json={
                "student_id": "stu_basic_001",
                "case_version_id": "case_chest_pain_001",
                "session_id": session_id,
                "student_response": "Puede haber un problema cardíaco.",
                "elapsed_seconds": 90,
                "hints_used": [],
            },
        )

        assert attempt_response.status_code == 422


def test_productive_core_attempt_rejects_session_mismatch() -> None:
    with build_test_client() as client:
        start_response = client.post(
            "/api/v1/sessions/start",
            json={"student_id": "stu_basic_001", "case_version_id": "case_chest_pain_001"},
        )
        session_id = start_response.json()["session_id"]

        attempt_response = client.post(
            "/api/v1/sessions/attempts/core",
            json={
                "student_id": "stu_clinical_001",
                "case_version_id": "case_chest_pain_001",
                "session_id": session_id,
                "student_response": "SCA posible.",
                "confidence_before": 0.5,
                "confidence_after": 0.6,
                "elapsed_seconds": 90,
                "hints_used": [],
            },
        )

        assert attempt_response.status_code == 409
