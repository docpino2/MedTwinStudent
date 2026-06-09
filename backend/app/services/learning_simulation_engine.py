from app.schemas.common import LearningCycle
from app.schemas.simulation import (
    InterventionType,
    LearningSimulationResponse,
    MasteryUpdate,
    RemainingGap,
    SimulationRequest,
)


INTERVENTION_EFFECTIVENESS = {
    InterventionType.MECHANISM_MICRO_LESSON: 0.64,
    InterventionType.RETRIEVAL_PRACTICE: 0.68,
    InterventionType.CONCEPT_MAP_REPAIR: 0.62,
    InterventionType.ILLNESS_SCRIPT_COMPARISON: 0.74,
    InterventionType.SOCRATIC_TUTORING: 0.72,
    InterventionType.COGNITIVE_FORCING_CHECKLIST: 0.7,
    InterventionType.CASE_CONTRAST_SET: 0.76,
    InterventionType.SIMULATION_RETRY: 0.78,
    InterventionType.HANDOFF_REHEARSAL: 0.66,
    InterventionType.SUPERVISOR_REVIEW: 0.7,
}


REMEDIATION_LABELS = {
    InterventionType.MECHANISM_MICRO_LESSON: "microlección de mecanismos",
    InterventionType.RETRIEVAL_PRACTICE: "práctica de recuperación espaciada",
    InterventionType.CONCEPT_MAP_REPAIR: "reparación de mapa conceptual",
    InterventionType.ILLNESS_SCRIPT_COMPARISON: "comparación de guiones de enfermedad",
    InterventionType.SOCRATIC_TUTORING: "tutoría socrática guiada",
    InterventionType.COGNITIVE_FORCING_CHECKLIST: "lista de verificación contra sesgos cognitivos",
    InterventionType.CASE_CONTRAST_SET: "set de casos contrastantes",
    InterventionType.SIMULATION_RETRY: "reintento de simulación con debrief",
    InterventionType.HANDOFF_REHEARSAL: "ensayo de entrega clínica",
    InterventionType.SUPERVISOR_REVIEW: "revisión con supervisor",
}


class LearningSimulationEngine:
    """Transparent weighted-update model for MVP learning trajectory simulation."""

    def simulate(self, request: SimulationRequest) -> LearningSimulationResponse:
        concept_labels = {concept.id: concept.label for concept in request.competency_map}
        baseline_scores = self._baseline_scores(request)
        performance = request.clinical_case_performance
        weights = request.weights

        time_factor = min(request.time_spent_minutes / 45, 1.0)
        difficulty_alignment = self._difficulty_alignment(request.difficulty_level, performance.overall_score)
        intervention_effect = INTERVENTION_EFFECTIVENESS[request.intervention_type]

        updates: list[MasteryUpdate] = []
        updated_scores: dict[str, float] = {}

        for concept_id, baseline in baseline_scores.items():
            concept_performance = performance.concept_scores.get(concept_id, performance.overall_score)
            driver_score = (
                weights.performance * concept_performance
                + weights.intervention * intervention_effect
                + weights.feedback_quality * request.feedback_quality
                + weights.time_spent * time_factor
                + weights.difficulty_alignment * difficulty_alignment
            )
            learning_readiness = 1 - baseline
            raw_delta = (driver_score - 0.5) * weights.max_positive_delta * (0.6 + learning_readiness)

            if concept_performance < 0.35:
                raw_delta -= (0.35 - concept_performance) * weights.max_negative_delta

            delta = round(raw_delta, 4)
            updated = self._clamp(baseline + delta)
            drivers = {
                "desempeno_caso": round(concept_performance, 3),
                "efecto_intervencion": round(intervention_effect, 3),
                "calidad_feedback": round(request.feedback_quality, 3),
                "tiempo": round(time_factor, 3),
                "alineacion_dificultad": round(difficulty_alignment, 3),
            }
            updates.append(
                MasteryUpdate(
                    concept_id=concept_id,
                    concept_label=concept_labels.get(concept_id, concept_id),
                    baseline=round(baseline, 4),
                    updated=updated,
                    delta=round(updated - baseline, 4),
                    drivers=drivers,
                )
            )
            updated_scores[concept_id] = updated

        remaining_gaps = self._remaining_gaps(request, updates)
        risk_reduction = self._risk_reduction(request, baseline_scores, updated_scores)
        next_activity = self._next_activity(request, remaining_gaps, risk_reduction)
        summary = self._trajectory_summary(request, updates, remaining_gaps, risk_reduction)

        return LearningSimulationResponse(
            updated_mastery_scores=updated_scores,
            mastery_updates=updates,
            predicted_risk_reduction=risk_reduction,
            remaining_gaps=remaining_gaps,
            recommended_next_activity=next_activity,
            learning_trajectory_summary=summary,
            model_config_used=weights,
        )

    def _baseline_scores(self, request: SimulationRequest) -> dict[str, float]:
        scores = {item.concept_id: item.mastery for item in request.student.knowledge_state}
        scores.update(request.baseline_mastery_scores)

        for concept in request.competency_map:
            scores.setdefault(concept.id, 0.0)

        return {concept_id: self._clamp(score) for concept_id, score in scores.items()}

    def _difficulty_alignment(self, difficulty_level: int, performance_score: float) -> float:
        normalized_difficulty = difficulty_level / 5
        challenge_gap = abs(normalized_difficulty - performance_score)
        return self._clamp(1 - challenge_gap)

    def _remaining_gaps(self, request: SimulationRequest, updates: list[MasteryUpdate]) -> list[RemainingGap]:
        concept_cycle = {concept.id: concept.cycle for concept in request.competency_map}
        gaps: list[RemainingGap] = []

        for update in updates:
            if update.updated >= request.weights.gap_threshold:
                continue

            severity = "alta" if update.updated < 0.4 else "moderada"
            remediation = self._remediation_for_gap(
                student_cycle=request.student.cycle,
                concept_cycle=concept_cycle.get(update.concept_id),
                intervention=request.intervention_type,
            )
            gaps.append(
                RemainingGap(
                    concept_id=update.concept_id,
                    concept_label=update.concept_label,
                    mastery=update.updated,
                    severity=severity,
                    recommended_remediation=remediation,
                )
            )

        return sorted(gaps, key=lambda gap: gap.mastery)[:5]

    def _remediation_for_gap(
        self,
        student_cycle: LearningCycle,
        concept_cycle: LearningCycle | None,
        intervention: InterventionType,
    ) -> str:
        if student_cycle == LearningCycle.BASIC_SCIENCES or concept_cycle == LearningCycle.BASIC_SCIENCES:
            return "microlección de mecanismo seguida de recuperación activa"
        if student_cycle == LearningCycle.CLINICAL_SCIENCES:
            return "caso contrastante con tutoría socrática sobre diagnóstico diferencial"
        if intervention == InterventionType.SIMULATION_RETRY:
            return "debrief focalizado y repetición con mayor restricción de tiempo"
        return "simulación corta con foco en priorización, seguridad y escalamiento"

    def _risk_reduction(
        self,
        request: SimulationRequest,
        baseline_scores: dict[str, float],
        updated_scores: dict[str, float],
    ) -> float:
        if not updated_scores:
            return 0.0

        baseline_mean = sum(baseline_scores[concept_id] for concept_id in updated_scores) / len(updated_scores)
        updated_mean = sum(updated_scores.values()) / len(updated_scores)
        mastery_gain = max(0.0, updated_mean - baseline_mean)
        safety_factor = request.clinical_case_performance.safety_score
        feedback_factor = request.feedback_quality
        risk_reduction = mastery_gain * 0.55 + safety_factor * 0.25 + feedback_factor * 0.2
        return round(self._clamp(risk_reduction), 4)

    def _next_activity(
        self,
        request: SimulationRequest,
        gaps: list[RemainingGap],
        risk_reduction: float,
    ) -> str:
        if gaps:
            top_gap = gaps[0]
            return (
                f"Realizar {top_gap.recommended_remediation} sobre {top_gap.concept_label.lower()} "
                "y repetir un caso breve de dolor torácico con retroalimentación inmediata."
            )
        if risk_reduction < 0.35:
            return "Repetir el caso con una intervención más guiada y feedback específico por criterio de rúbrica."
        return "Avanzar a un caso de dolor torácico más complejo con diagnósticos competidores y restricciones de sistema."

    def _trajectory_summary(
        self,
        request: SimulationRequest,
        updates: list[MasteryUpdate],
        gaps: list[RemainingGap],
        risk_reduction: float,
    ) -> str:
        positive_updates = [update for update in updates if update.delta > 0]
        average_delta = sum(update.delta for update in updates) / len(updates) if updates else 0
        intervention = REMEDIATION_LABELS[request.intervention_type]
        return (
            f"Tras {request.time_spent_minutes} minutos de {intervention}, "
            f"{request.student.name} muestra cambio promedio de dominio de {average_delta:+.1%}. "
            f"Conceptos con mejora: {len(positive_updates)}/{len(updates)}. "
            f"Reducción de riesgo predicha: {risk_reduction:.0%}. "
            f"Persisten {len(gaps)} brechas bajo el umbral configurado."
        )

    def _clamp(self, value: float) -> float:
        return round(max(0.0, min(1.0, value)), 4)

