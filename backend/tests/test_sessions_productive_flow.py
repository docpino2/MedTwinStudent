from collections.abc import Generator
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app import db_init
from app.main import app
from app.models import ClinicalCase, CurriculumConcept, Student
from app.services.seed_repository import get_seed_cases, get_seed_concepts, get_seed_students


def test_postgraduate_bootstrap_is_idempotent_and_preserves_existing_profile(monkeypatch) -> None:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr(db_init, "engine", engine)

    db_init.ensure_postgraduate_profile()
    with Session(engine) as session:
        carlos = session.get(Student, db_init.POSTGRADUATE_STUDENT_ID)
        assert carlos is not None
        assert carlos.name == "Carlos Pérez"
        carlos.mastery_level = "competent"
        session.commit()

    db_init.ensure_postgraduate_profile()
    with Session(engine) as session:
        students = session.query(Student).all()
        assert len(students) == 1
        assert students[0].mastery_level == "competent"


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


def test_postgraduate_profile_can_start_session_and_submit_attempt() -> None:
    student_id = "stu_postgraduate_internal_medicine_001"
    with build_test_client() as client:
        students = client.get("/api/v1/students")
        assert students.status_code == 200
        carlos = next(item for item in students.json() if item["id"] == student_id)
        assert carlos["name"] == "Carlos Pérez"
        assert carlos["cycle"] == "postgraduate"
        assert carlos["current_rotation"] == "Medicina Interna"

        started = client.post(
            "/api/v1/sessions/start",
            json={"student_id": student_id, "case_version_id": "case_chest_pain_001"},
        )
        assert started.status_code == 200
        attempt = client.post(
            "/api/v1/sessions/attempts/core",
            json={
                "student_id": student_id,
                "case_version_id": "case_chest_pain_001",
                "session_id": started.json()["session_id"],
                "student_response": (
                    "Dolor torácico opresivo con esfuerzo, irradiación al brazo izquierdo, "
                    "diaforesis y factores de riesgo cardiovascular. Priorizo SCA, ECG inmediato "
                    "y troponinas seriadas; comunicaría la incertidumbre al equipo."
                ),
                "confidence_before": 0.62,
                "confidence_after": 0.78,
                "elapsed_seconds": 210,
                "hints_used": [],
            },
        )
        assert attempt.status_code == 200
        body = attempt.json()
        assert body["attempt_id"]
        assert body["mastery_estimates"]
        assert "postgrado en Medicina Interna" in body["reasoning"]["reasoning_analysis"]


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
