from app.schemas.reasoning import (
    ClinicalEvidenceObservation,
    CognitiveBiasRisk,
    KnowledgeGap,
    ReasoningAnalysisRequest,
    ReasoningAnalysisResponse,
)
from app.services.clinical_evidence import ClinicalEvidenceMatcher, normalize_clinical_text


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
    def __init__(self) -> None:
        self.evidence_matcher = ClinicalEvidenceMatcher()

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

        response_text = normalize_clinical_text(request.student_response or "")
        evidence_matches = self.evidence_matcher.match_red_flags(
            request.student_response or "",
            clinical_case.red_flags,
        )
        missed_red_flags = [match.label for match in evidence_matches if not match.detected]
        detected_count = sum(match.detected for match in evidence_matches)
        red_flag_coverage = detected_count / len(evidence_matches) if evidence_matches else 1.0
        bias = self._estimate_bias(student.cycle, response_text, missed_red_flags, red_flag_coverage)

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
            clinical_evidence=[
                ClinicalEvidenceObservation(
                    criterion=match.canonical_flag,
                    label=match.label,
                    detected=match.detected,
                    evidence=match.matched_text,
                )
                for match in evidence_matches
            ],
            red_flag_coverage=round(red_flag_coverage, 4),
        )

    def _estimate_bias(
        self,
        cycle: str,
        response_text: str,
        missed_red_flags: list[str],
        red_flag_coverage: float,
    ) -> CognitiveBiasRisk:
        if "reflux" in response_text or "reflujo" in response_text or "anxiety" in response_text or "ansiedad" in response_text:
            return CognitiveBiasRisk(
                bias="cierre prematuro",
                risk_level="high",
                rationale="El estudiante parece aceptar un diagnóstico benigno antes de abordar causas cardíacas tiempo-dependientes.",
            )
        if missed_red_flags and red_flag_coverage < 0.5:
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
            rationale=(
                "El razonamiento reconoce la mayoría de las banderas rojas y mantiene la prioridad clínica; "
                "las omisiones restantes requieren retroalimentación sin constituir por sí solas un sesgo relevante."
            ),
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
            f"Banderas rojas aún no representadas: {', '.join(missed_red_flags)}."
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
