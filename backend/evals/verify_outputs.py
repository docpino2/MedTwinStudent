from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.schemas.reasoning import ReasoningAnalysisRequest
from app.schemas.simulation import ClinicalCasePerformance, InterventionType, SimulationRequest
from app.schemas.tutor import TutorTurnRequest
from app.services.learning_simulation_engine import LearningSimulationEngine
from app.services.reasoning_engine import ReasoningEngine
from app.services.seed_repository import get_seed_cases, get_seed_concepts, get_seed_students
from app.services.socratic_tutor import SocraticTutorAgent

OUTPUT_PATH = ROOT / "evals" / "output" / "latest_outputs.json"

SPANISH_MARKERS = [
    "¿",
    "qué",
    "cómo",
    "estudiante",
    "riesgo",
    "brecha",
    "seguridad",
    "diagnóstico",
    "retroalimentación",
    "incertidumbre",
    "dolor torácico",
    "microlección",
    "recuperación",
    "caso",
    "simulación",
    "priorización",
    "escalamiento",
    "repetición",
    "restricción",
    "tiempo",
    "diferencial",
]

VISIBLE_OUTPUT_FIELDS = {
    "tutor": [
        "tutor_question",
        "rationale_for_question",
        "stop_condition",
    ],
    "reasoning": [
        "reasoning_analysis",
        "feedback",
        "next_recommended_activity",
        "tutor_prompt",
    ],
    "simulation": [
        "recommended_next_activity",
        "learning_trajectory_summary",
    ],
}


def main() -> int:
    students = {student.id: student for student in get_seed_students()}
    clinical_case = get_seed_cases()[0]
    concepts = get_seed_concepts()

    scenarios = [
        {
            "id": "basic_mechanism_gap",
            "student_id": "stu_basic_001",
            "student_response": "Exercise makes the heart hurt, but I am not sure why.",
            "intervention_type": InterventionType.MECHANISM_MICRO_LESSON,
            "performance": ClinicalCasePerformance(
                overall_score=0.42,
                concept_scores={
                    "cardiac_ischemia_pathophysiology": 0.48,
                    "chest_pain_red_flags": 0.28,
                },
                safety_score=0.35,
                reasoning_score=0.4,
                metacognition_score=0.55,
            ),
            "feedback_quality": 0.78,
            "time_spent_minutes": 18,
            "difficulty_level": 2,
        },
        {
            "id": "clinical_premature_closure",
            "student_id": "stu_clinical_001",
            "student_response": "This is probably reflux because he has chest discomfort and nausea.",
            "intervention_type": InterventionType.CASE_CONTRAST_SET,
            "performance": ClinicalCasePerformance(
                overall_score=0.52,
                concept_scores={
                    "differential_diagnosis_chest_pain": 0.48,
                    "acs_risk_stratification": 0.45,
                    "ecg_initial_interpretation": 0.5,
                },
                safety_score=0.42,
                reasoning_score=0.5,
                metacognition_score=0.38,
            ),
            "feedback_quality": 0.84,
            "time_spent_minutes": 30,
            "difficulty_level": 3,
        },
        {
            "id": "intern_troponin_overconfidence",
            "student_id": "stu_intern_001",
            "student_response": "I would get labs. If troponin is negative he can probably go home.",
            "intervention_type": InterventionType.SIMULATION_RETRY,
            "performance": ClinicalCasePerformance(
                overall_score=0.66,
                concept_scores={
                    "troponin_kinetics": 0.42,
                    "initial_acs_management": 0.72,
                    "acs_risk_stratification": 0.68,
                },
                safety_score=0.68,
                reasoning_score=0.64,
                metacognition_score=0.5,
            ),
            "feedback_quality": 0.88,
            "time_spent_minutes": 25,
            "difficulty_level": 4,
        },
    ]

    outputs = []
    failed_checks: list[str] = []

    for scenario in scenarios:
        student = students[scenario["student_id"]]
        tutor_output = SocraticTutorAgent().generate_turn(
            TutorTurnRequest(
                student=student,
                clinical_case=clinical_case,
                conversation=[],
                latest_student_response=scenario["student_response"],
            )
        )
        reasoning_output = ReasoningEngine().analyze(
            ReasoningAnalysisRequest(
                student=student,
                clinical_case=clinical_case,
                student_response=scenario["student_response"],
            )
        )
        simulation_output = LearningSimulationEngine().simulate(
            SimulationRequest(
                student=student,
                competency_map=concepts,
                baseline_mastery_scores={},
                clinical_case_performance=scenario["performance"],
                intervention_type=scenario["intervention_type"],
                feedback_quality=scenario["feedback_quality"],
                time_spent_minutes=scenario["time_spent_minutes"],
                difficulty_level=scenario["difficulty_level"],
            )
        )

        record = {
            "scenario_id": scenario["id"],
            "student_id": student.id,
            "student_cycle": student.cycle,
            "tutor": tutor_output.model_dump(mode="json"),
            "reasoning": reasoning_output.model_dump(mode="json"),
            "simulation": simulation_output.model_dump(mode="json"),
        }
        outputs.append(record)
        failed_checks.extend(validate_record(record))

    report = {
        "status": "failed" if failed_checks else "passed",
        "generated_at": datetime.now(UTC).isoformat(),
        "checks": {
            "total_scenarios": len(scenarios),
            "failed": failed_checks,
        },
        "outputs": outputs,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Estado: {report['status']}")
    print(f"Escenarios evaluados: {len(scenarios)}")
    print(f"Reporte: {OUTPUT_PATH}")
    if failed_checks:
        print("Fallos:")
        for failure in failed_checks:
            print(f"- {failure}")
        return 1

    print("Todas las validaciones pasaron.")
    return 0


def validate_record(record: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    scenario_id = record["scenario_id"]

    if record["tutor"]["should_withhold_final_answer"] is not True:
        failures.append(f"{scenario_id}: el tutor no está reteniendo la respuesta final.")

    if not record["tutor"]["rubric_feedback"]:
        failures.append(f"{scenario_id}: el tutor no devolvió feedback de rúbrica.")

    if not record["reasoning"]["likely_knowledge_gaps"]:
        failures.append(f"{scenario_id}: el motor de razonamiento no detectó brechas.")

    if not record["simulation"]["updated_mastery_scores"]:
        failures.append(f"{scenario_id}: la simulación no actualizó puntajes de dominio.")

    if record["simulation"]["predicted_risk_reduction"] < 0:
        failures.append(f"{scenario_id}: la reducción de riesgo predicha es inválida.")

    for section, fields in VISIBLE_OUTPUT_FIELDS.items():
        for field in fields:
            text = str(record[section].get(field, ""))
            if not looks_spanish(text):
                failures.append(f"{scenario_id}: {section}.{field} no parece estar en español.")

    for item in record["simulation"].get("remaining_gaps", []):
        if not looks_spanish(item.get("recommended_remediation", "")):
            failures.append(f"{scenario_id}: remediation de brecha no parece estar en español.")

    return failures


def looks_spanish(text: str) -> bool:
    normalized = text.lower()
    return any(marker in normalized for marker in SPANISH_MARKERS)


if __name__ == "__main__":
    raise SystemExit(main())
