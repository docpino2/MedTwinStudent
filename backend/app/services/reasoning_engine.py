from app.schemas.reasoning import (
    CognitiveBiasRisk,
    KnowledgeGap,
    ReasoningAnalysisRequest,
    ReasoningAnalysisResponse,
)


CONCEPT_LABELS = {
    "cardiac_ischemia_pathophysiology": "Fisiopatología de la isquemia miocárdica",
    "chest_pain_red_flags": "Banderas rojas en dolor torácico",
    "ecg_initial_interpretation": "Interpretación inicial del ECG",
    "acs_risk_stratification": "Estratificación de riesgo de síndrome coronario agudo",
    "troponin_kinetics": "Cinética de troponinas",
    "initial_acs_management": "Manejo inicial del síndrome coronario agudo",
    "differential_diagnosis_chest_pain": "Diagnóstico diferencial del dolor torácico",
}


class ReasoningEngine:
    def analyze(self, request: ReasoningAnalysisRequest) -> ReasoningAnalysisResponse:
        student = request.student
        clinical_case = request.clinical_case

        mastery_by_concept = {item.concept_id: item.mastery for item in student.knowledge_state}
        gaps: list[KnowledgeGap] = []

        for concept_id in clinical_case.required_concepts:
            mastery = mastery_by_concept.get(concept_id, 0.0)
            if mastery < 0.7:
                severity = "high" if mastery < 0.4 else "moderate"
                gaps.append(
                    KnowledgeGap(
                        concept_id=concept_id,
                        concept_label=CONCEPT_LABELS.get(concept_id, concept_id.replace("_", " ").title()),
                        severity=severity,
                        rationale=f"La estimación de dominio es {mastery:.0%}, por debajo del umbral MVP de competencia de 70%.",
                    )
                )

        response_text = (request.student_response or "").lower()
        missed_red_flags = [
            flag
            for flag in clinical_case.red_flags
            if flag.lower() not in response_text
        ]
        bias = self._estimate_bias(student.cycle, response_text, missed_red_flags)

        if gaps:
            top_gap = gaps[0]
            next_activity = (
                f"Completar un caso adaptativo corto sobre {top_gap.concept_label.lower()}, "
                "responder una pregunta socrática de reflexión y luego repetir el triaje de dolor torácico."
            )
        else:
            next_activity = "Avanzar a un caso de dolor torácico de mayor complejidad con diagnósticos pulmonares y vasculares competidores."

        reasoning_analysis = self._build_reasoning_summary(request, gaps, missed_red_flags)
        feedback = self._build_feedback(gaps, missed_red_flags)
        tutor_prompt = self._build_tutor_prompt(request, gaps, bias)
        simulation_update = {
            concept_id: max(0.0, min(1.0, mastery_by_concept.get(concept_id, 0.0) + (0.04 if concept_id not in {gap.concept_id for gap in gaps} else -0.02)))
            for concept_id in clinical_case.required_concepts
        }

        return ReasoningAnalysisResponse(
            reasoning_analysis=reasoning_analysis,
            likely_knowledge_gaps=gaps,
            cognitive_bias_risk=bias,
            feedback=feedback,
            next_recommended_activity=next_activity,
            tutor_prompt=tutor_prompt,
            simulation_update=simulation_update,
        )

    def _estimate_bias(
        self,
        cycle: str,
        response_text: str,
        missed_red_flags: list[str],
    ) -> CognitiveBiasRisk:
        if "reflux" in response_text or "reflujo" in response_text or "anxiety" in response_text or "ansiedad" in response_text:
            return CognitiveBiasRisk(
                bias="cierre prematuro",
                risk_level="high",
                rationale="El estudiante parece aceptar un diagnóstico benigno antes de abordar causas cardíacas tiempo-dependientes.",
            )
        if missed_red_flags:
            return CognitiveBiasRisk(
                bias="anclaje",
                risk_level="moderate",
                rationale="Banderas rojas importantes no fueron incorporadas explícitamente en la representación del problema.",
            )
        if cycle == "basic_sciences":
            return CognitiveBiasRisk(
                bias="sesgo de disponibilidad",
                risk_level="moderate",
                rationale="Estudiantes tempranos pueden sobreponderar mecanismos recién estudiados sin conectarlos con riesgo clínico.",
            )
        return CognitiveBiasRisk(
            bias="riesgo bajo detectado",
            risk_level="low",
            rationale="El razonamiento entregado atiende los conceptos requeridos y las banderas rojas a este nivel MVP.",
        )

    def _build_reasoning_summary(
        self,
        request: ReasoningAnalysisRequest,
        gaps: list[KnowledgeGap],
        missed_red_flags: list[str],
    ) -> str:
        student = request.student
        clinical_case = request.clinical_case
        cycle_label = student.cycle.replace("_", " ")
        gap_clause = f"se detectan {len(gaps)} brecha(s) probable(s)" if gaps else "no se detectan brechas mayores"
        red_flag_clause = (
            f"Banderas rojas omitidas: {', '.join(missed_red_flags)}."
            if missed_red_flags
            else "Las banderas rojas clave fueron representadas."
        )
        return (
            f"{student.name} está en el ciclo {cycle_label} y analiza "
            f"'{clinical_case.title}'. La traza de razonamiento muestra que {gap_clause}. {red_flag_clause}"
        )

    def _build_feedback(self, gaps: list[KnowledgeGap], missed_red_flags: list[str]) -> str:
        if not gaps and not missed_red_flags:
            return "Buen razonamiento inicial. Mantén primero los diagnósticos potencialmente mortales y luego acota con ECG, cinética de troponinas y factores de riesgo."

        messages = []
        if missed_red_flags:
            messages.append("Empieza nombrando las banderas rojas y explicando por qué cambian la urgencia.")
        if gaps:
            messages.append(f"Revisa {gaps[0].concept_label.lower()} antes de intentar el siguiente caso.")
        return " ".join(messages)

    def _build_tutor_prompt(
        self,
        request: ReasoningAnalysisRequest,
        gaps: list[KnowledgeGap],
        bias: CognitiveBiasRisk,
    ) -> str:
        focus = gaps[0].concept_label if gaps else "estratificación de riesgo"
        return (
            f"Pregunta a {request.student.name} una cuestión socrática sobre {focus}. "
            f"Guíalo a comparar causas peligrosas y comunes de dolor torácico. "
            f"Vigila {bias.bias}."
        )
