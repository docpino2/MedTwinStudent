from app.schemas.ai_health import (
    AIHealthCompetency,
    AIHealthCriterionScore,
    AIHealthEvaluationRequest,
    AIHealthEvaluationResponse,
    AIHealthRiskSignal,
    AIHealthSkill,
)
from app.schemas.common import LearningCycle


def get_ai_health_competencies() -> list[AIHealthCompetency]:
    return [
        AIHealthCompetency(
            id=AIHealthSkill.CLINICAL_QUESTION_FORMULATION,
            title="Formulación de preguntas clínicas para IA",
            cycle=LearningCycle.BASIC_SCIENCES,
            description="Convierte dudas biomédicas o clínicas iniciales en preguntas claras, acotadas y verificables.",
            observable_behaviors=[
                "Explicita qué no entiende.",
                "Distingue pregunta conceptual, diagnóstica, terapéutica o de seguridad.",
                "Solicita explicación ajustada a su nivel formativo.",
            ],
            assessment_methods=["revisión de prompt", "diálogo con tutor IA", "reflexión metacognitiva"],
            common_failure_modes=["preguntas vagas", "delegación de juicio", "confundir explicación con validación clínica"],
            ai_supported_interventions=["plantillas de pregunta clínica", "tutoría socrática sobre incertidumbre"],
        ),
        AIHealthCompetency(
            id=AIHealthSkill.RESPONSIBLE_PROMPTING,
            title="Prompting clínico responsable",
            cycle=LearningCycle.CLINICAL_SCIENCES,
            description="Entrega contexto suficiente, declara incertidumbre y pide razonamiento diferencial sin exigir respuestas cerradas.",
            observable_behaviors=[
                "Incluye datos clínicos relevantes sin identificadores.",
                "Pide alternativas peligrosas y discriminadores.",
                "Solicita límites, supuestos y próximos datos necesarios.",
            ],
            assessment_methods=["rúbrica de prompt", "caso contrastante", "evaluación de seguridad"],
            common_failure_modes=["omitir red flags", "pedir solo diagnóstico final", "incluir datos identificables"],
            ai_supported_interventions=["checklist de prompt seguro", "comparación de prompts buenos y malos"],
        ),
        AIHealthCompetency(
            id=AIHealthSkill.AI_OUTPUT_CRITIQUE,
            title="Crítica de salidas generadas por IA",
            cycle=LearningCycle.CLINICAL_SCIENCES,
            description="Evalúa si la respuesta IA es completa, segura, verificable y coherente con los datos del caso.",
            observable_behaviors=[
                "Detecta omisiones peligrosas.",
                "Contrasta la salida con red flags y guías clínicas.",
                "Identifica alucinaciones o afirmaciones no justificadas.",
            ],
            assessment_methods=["crítica escrita", "detección de errores IA", "discusión docente"],
            common_failure_modes=["aceptación acrítica", "confirmación de hipótesis propia", "no verificar fuentes"],
            ai_supported_interventions=["salidas IA deliberadamente incompletas", "lista de verificación de verificación"],
        ),
        AIHealthCompetency(
            id=AIHealthSkill.DIFFERENTIAL_REASONING_WITH_AI,
            title="Razonamiento diferencial aumentado por IA",
            cycle=LearningCycle.CLINICAL_SCIENCES,
            description="Usa IA para ampliar hipótesis y buscar discriminadores sin reemplazar el juicio clínico.",
            observable_behaviors=[
                "Pide diagnósticos peligrosos y comunes.",
                "Solicita datos que cambien probabilidad.",
                "Reordena el diferencial con base en el caso, no en la autoridad del modelo.",
            ],
            assessment_methods=["think-aloud", "script concordance", "casos comparativos"],
            common_failure_modes=["sobredependencia", "anclaje en salida IA", "diferencial no priorizado"],
            ai_supported_interventions=["prompt de diagnóstico diferencial", "debiasing asistido"],
        ),
        AIHealthCompetency(
            id=AIHealthSkill.PRIVACY_AND_GOVERNANCE,
            title="Privacidad, gobernanza y responsabilidad profesional",
            cycle=LearningCycle.INTERNSHIP,
            description="Usa herramientas IA sin exponer datos sensibles y mantiene responsabilidad humana sobre decisiones.",
            observable_behaviors=[
                "No ingresa identificadores del paciente.",
                "Reconoce límites legales, institucionales y clínicos.",
                "Escala decisiones a supervisor cuando hay riesgo o incertidumbre.",
            ],
            assessment_methods=["auditoría de prompt", "simulación de caso real", "observación en práctica"],
            common_failure_modes=["PHI en prompt", "uso de IA fuera de política", "no escalar decisiones"],
            ai_supported_interventions=["checklist de privacidad", "simulación de gobernanza clínica"],
        ),
        AIHealthCompetency(
            id=AIHealthSkill.AGENT_ORCHESTRATION,
            title="Orquestación de agentes IA en aprendizaje clínico",
            cycle=LearningCycle.INTERNSHIP,
            description="Elige y coordina tutor, generador de casos, evaluador y simulador según la necesidad educativa o clínica.",
            observable_behaviors=[
                "Selecciona el agente adecuado para la tarea.",
                "Revisa outputs antes de usarlos.",
                "Integra retroalimentación en un plan de mejora.",
            ],
            assessment_methods=["flujo con agentes", "portafolio digital", "debrief docente"],
            common_failure_modes=["automatizar sin revisar", "usar agente incorrecto", "fragmentar el razonamiento"],
            ai_supported_interventions=["workflow guiado", "simulación con agentes encadenados"],
        ),
        AIHealthCompetency(
            id=AIHealthSkill.AI_AUGMENTED_METACOGNITION,
            title="Metacognición aumentada por IA",
            cycle=LearningCycle.BASIC_SCIENCES,
            description="Usa IA para identificar límites de conocimiento, calibrar confianza y planear estudio deliberado.",
            observable_behaviors=[
                "Declara nivel de confianza.",
                "Pide preguntas para revelar brechas.",
                "Compara su explicación con una alternativa generada.",
            ],
            assessment_methods=["diario de aprendizaje", "calibración confianza-desempeño", "tutor IA"],
            common_failure_modes=["sobreconfianza", "estudio pasivo", "no cerrar brechas detectadas"],
            ai_supported_interventions=["preguntas adaptativas", "plan de recuperación espaciada"],
        ),
    ]


class AIHealthCompetencyEngine:
    def list_competencies(self) -> list[AIHealthCompetency]:
        return get_ai_health_competencies()

    def evaluate(self, request: AIHealthEvaluationRequest) -> AIHealthEvaluationResponse:
        prompt = request.student_ai_prompt.lower()
        output = (request.ai_model_output or "").lower()
        critique = (request.student_critique or "").lower()
        cycle = request.student.cycle

        scores = [
            self._score_prompt_context(request, prompt),
            self._score_safety_and_privacy(request, prompt),
            self._score_critical_appraisal(request, output, critique),
            self._score_clinical_reasoning_with_ai(request, prompt, critique),
            self._score_metacognition(request, prompt, critique),
        ]
        if cycle == LearningCycle.INTERNSHIP:
            scores.append(self._score_escalation_and_systems(request, prompt, critique))

        risks = self._detect_risks(request, prompt, output, critique)
        overall = round(sum(score.score for score in scores) / len(scores), 2)
        gaps = [f"{score.criterion}: {score.next_step}" for score in scores if score.score < 3]

        return AIHealthEvaluationResponse(
            cycle=cycle,
            overall_score=overall,
            mastery_level=self._mastery_level(overall),
            competency_scores=scores,
            detected_risks=risks,
            emerging_competency_gaps=gaps,
            feedback=self._feedback(cycle, overall, risks),
            recommended_remediation=self._remediation(cycle, gaps, risks),
            next_recommended_activity=self._next_activity(cycle, risks, gaps),
            digital_health_trajectory_note=self._trajectory_note(request, overall, gaps),
        )

    def _score_prompt_context(self, request: AIHealthEvaluationRequest, prompt: str) -> AIHealthCriterionScore:
        evidence = []
        score = 0
        if len(prompt.split()) >= 18:
            score += 1
            evidence.append("Incluye una cantidad mínima de contexto.")
        if any(term in prompt for term in ["edad", "age", "síntoma", "symptom", "signos", "vitals", "antecedente"]):
            score += 1
            evidence.append("Incluye datos clínicos del caso.")
        if any(term in prompt for term in ["diferencial", "differential", "alternativas", "causas peligrosas", "red flags"]):
            score += 1
            evidence.append("Pide razonamiento diferencial o causas peligrosas.")
        if any(term in prompt for term in ["incertidumbre", "uncertain", "supuestos", "límites", "limitations"]):
            score += 1
            evidence.append("Reconoce incertidumbre o límites.")
        return AIHealthCriterionScore(
            criterion="contexto_y_formulacion_del_prompt",
            score=min(score, 4),
            rationale="Evalúa si el estudiante formula una pregunta clínica útil, contextualizada y no reducida a pedir la respuesta final.",
            evidence=evidence,
            next_step="Incluir contexto clínico, objetivo de uso, diferencial esperado, límites e incertidumbre.",
        )

    def _score_safety_and_privacy(self, request: AIHealthEvaluationRequest, prompt: str) -> AIHealthCriterionScore:
        score = 4
        evidence = ["No se reporta uso de identificadores directos."]
        if request.used_patient_identifiers:
            score -= 3
            evidence = ["Se reporta uso de identificadores del paciente."]
        if any(term in prompt for term in ["nombre", "documento", "teléfono", "address", "phone", "id patient"]):
            score -= 2
            evidence.append("El prompt parece contener datos potencialmente identificables.")
        if "no incluyas datos identificables" in prompt or "sin datos identificables" in prompt:
            score = min(4, score + 1)
            evidence.append("Explicita restricción de privacidad.")
        return AIHealthCriterionScore(
            criterion="privacidad_y_seguridad_digital",
            score=max(0, min(score, 4)),
            rationale="Evalúa si el estudiante usa IA sin exponer información sensible y con responsabilidad profesional.",
            evidence=evidence,
            next_step="Anonimizar el caso y declarar explícitamente que no se deben incluir datos identificables.",
        )

    def _score_critical_appraisal(
        self,
        request: AIHealthEvaluationRequest,
        output: str,
        critique: str,
    ) -> AIHealthCriterionScore:
        evidence = []
        score = 0
        if critique:
            score += 1
            evidence.append("El estudiante entregó una crítica de la salida IA.")
        if any(term in critique for term in ["omite", "falt", "red flag", "bandera roja", "peligros", "unsafe", "insegur"]):
            score += 1
            evidence.append("Busca omisiones o riesgos de seguridad.")
        if any(term in critique for term in ["fuente", "guía", "evidencia", "verificar", "confirmar", "guideline"]):
            score += 1
            evidence.append("Solicita verificación externa o contraste con guía.")
        if output and any(term in critique for term in ["no basta", "no reemplaza", "supervisor", "juicio clínico", "responsabilidad"]):
            score += 1
            evidence.append("Mantiene responsabilidad humana sobre la decisión.")
        return AIHealthCriterionScore(
            criterion="critica_de_salida_ia",
            score=min(score, 4),
            rationale="Evalúa si el estudiante revisa la salida generada antes de incorporarla a su razonamiento.",
            evidence=evidence,
            next_step="Comparar la salida IA contra datos del caso, banderas rojas, guías y límites del modelo.",
        )

    def _score_clinical_reasoning_with_ai(
        self,
        request: AIHealthEvaluationRequest,
        prompt: str,
        critique: str,
    ) -> AIHealthCriterionScore:
        evidence = []
        score = 0
        if any(term in prompt for term in ["diagnóstico diferencial", "differential", "diferencial"]):
            score += 1
            evidence.append("Usa IA para ampliar hipótesis.")
        if any(term in prompt for term in ["discriminadores", "datos que cambian", "support/refute", "apoyan o refutan"]):
            score += 1
            evidence.append("Pide rasgos discriminantes.")
        if any(term in prompt + critique for term in ["sca", "acs", "síndrome coronario", "disección", "tep", "embolia", "neumotórax"]):
            score += 1
            evidence.append("Considera diagnósticos peligrosos.")
        if any(term in critique for term in ["priorizar", "probabilidad", "riesgo", "urgencia"]):
            score += 1
            evidence.append("Reordena la salida IA según riesgo y probabilidad.")
        return AIHealthCriterionScore(
            criterion="razonamiento_clinico_aumentado_por_ia",
            score=min(score, 4),
            rationale="Evalúa si la IA se usa para fortalecer el razonamiento clínico, no para sustituirlo.",
            evidence=evidence,
            next_step="Pedir diagnósticos peligrosos y comunes, discriminadores, y justificar la priorización propia.",
        )

    def _score_metacognition(
        self,
        request: AIHealthEvaluationRequest,
        prompt: str,
        critique: str,
    ) -> AIHealthCriterionScore:
        evidence = []
        score = 0
        uncertainty_text = (request.declared_uncertainty or "").lower()
        if uncertainty_text or any(term in prompt for term in ["no estoy seguro", "incertidumbre", "uncertain"]):
            score += 1
            evidence.append("Declara incertidumbre.")
        if any(term in prompt + critique for term in ["sesgo", "bias", "anclaje", "cierre prematuro", "sobreconfianza"]):
            score += 1
            evidence.append("Vigila sesgos cognitivos.")
        if any(term in prompt for term in ["pregúntame", "evalúame", "brechas", "feedback", "retroalimentación"]):
            score += 1
            evidence.append("Usa IA para aprendizaje autorregulado.")
        if any(term in critique for term in ["mi razonamiento", "cambiaría", "confianza", "calibr"]):
            score += 1
            evidence.append("Reflexiona sobre su propio razonamiento.")
        return AIHealthCriterionScore(
            criterion="metacognicion_aumentada_por_ia",
            score=min(score, 4),
            rationale="Evalúa si el estudiante usa IA para calibrar incertidumbre, sesgos y brechas.",
            evidence=evidence,
            next_step="Declarar confianza, sesgo probable y qué evidencia cambiaría la hipótesis.",
        )

    def _score_escalation_and_systems(
        self,
        request: AIHealthEvaluationRequest,
        prompt: str,
        critique: str,
    ) -> AIHealthCriterionScore:
        evidence = []
        score = 0
        if any(term in prompt + critique for term in ["supervisor", "cardiología", "escalar", "senior", "equipo"]):
            score += 2
            evidence.append("Reconoce necesidad de escalamiento humano.")
        if any(term in prompt + critique for term in ["protocolo", "institucional", "sistema", "disponibilidad", "recursos"]):
            score += 1
            evidence.append("Considera restricciones del sistema.")
        if request.escalated_to_human_supervisor:
            score += 1
            evidence.append("Reporta escalamiento a supervisor humano.")
        return AIHealthCriterionScore(
            criterion="escalamiento_y_restricciones_del_sistema",
            score=min(score, 4),
            rationale="Evalúa si el interno usa IA sin perder supervisión, flujo de atención y límites institucionales.",
            evidence=evidence,
            next_step="Explicitar cuándo escalar, a quién y qué restricciones del sistema modifican la conducta.",
        )

    def _detect_risks(
        self,
        request: AIHealthEvaluationRequest,
        prompt: str,
        output: str,
        critique: str,
    ) -> list[AIHealthRiskSignal]:
        risks: list[AIHealthRiskSignal] = []
        if request.used_patient_identifiers:
            risks.append(
                AIHealthRiskSignal(
                    risk="riesgo de privacidad",
                    level="crítico",
                    rationale="Se reporta inclusión de identificadores del paciente en el uso de IA.",
                    mitigation="Anonimizar el caso y usar solo datos clínicos necesarios.",
                )
            )
        if any(term in prompt for term in ["dime el diagnóstico", "final diagnosis", "respuesta final"]) and "diferencial" not in prompt:
            risks.append(
                AIHealthRiskSignal(
                    risk="sobredependencia de IA",
                    level="alto",
                    rationale="El prompt pide una respuesta final sin solicitar razonamiento, límites o alternativas.",
                    mitigation="Reformular el prompt para pedir diferencial, discriminadores y supuestos.",
                )
            )
        if output and not critique:
            risks.append(
                AIHealthRiskSignal(
                    risk="aceptación acrítica de salida IA",
                    level="moderado",
                    rationale="Existe salida IA pero no hay crítica del estudiante.",
                    mitigation="Exigir verificación contra datos del caso y guías antes de aceptar la salida.",
                )
            )
        if request.student.cycle == LearningCycle.INTERNSHIP and not request.escalated_to_human_supervisor:
            risks.append(
                AIHealthRiskSignal(
                    risk="falta de escalamiento supervisado",
                    level="moderado",
                    rationale="En internado, el uso de IA en un caso potencialmente riesgoso debe integrarse con supervisión humana.",
                    mitigation="Definir umbral de escalamiento y comunicar incertidumbre al supervisor.",
                )
            )
        return risks

    def _mastery_level(self, score: float) -> str:
        if score < 1:
            return "no observado"
        if score < 2:
            return "novato"
        if score < 3:
            return "en desarrollo"
        if score < 3.6:
            return "competente"
        return "adaptativo"

    def _feedback(
        self,
        cycle: LearningCycle,
        overall: float,
        risks: list[AIHealthRiskSignal],
    ) -> str:
        if overall >= 3 and not risks:
            return "Uso sólido de IA/Salud Digital: el estudiante mantiene juicio clínico, seguridad y verificación crítica."
        if cycle == LearningCycle.BASIC_SCIENCES:
            return "Fortalece la pregunta conceptual, declara incertidumbre y usa IA para revelar brechas, no para memorizar respuestas."
        if cycle == LearningCycle.CLINICAL_SCIENCES:
            return "Usa IA para ampliar el diferencial, pedir discriminadores y criticar omisiones peligrosas antes de aceptar una salida."
        return "Integra IA con seguridad clínica: prioriza, verifica, protege datos y escala decisiones bajo incertidumbre."

    def _remediation(
        self,
        cycle: LearningCycle,
        gaps: list[str],
        risks: list[AIHealthRiskSignal],
    ) -> list[str]:
        remediation = []
        if risks:
            remediation.append("Revisar checklist de IA clínica segura: privacidad, límites, verificación y responsabilidad humana.")
        if cycle == LearningCycle.BASIC_SCIENCES:
            remediation.append("Practicar prompts de explicación mecanística con declaración de incertidumbre y preguntas de autoevaluación.")
        elif cycle == LearningCycle.CLINICAL_SCIENCES:
            remediation.append("Comparar dos prompts: uno que pide diagnóstico final y otro que pide diferencial, discriminadores y red flags.")
        else:
            remediation.append("Realizar simulación con IA bajo presión: decidir, verificar, escalar y documentar límites del modelo.")
        if gaps:
            remediation.append("Repetir la actividad enfocándose en los criterios con puntaje menor a 3.")
        return remediation

    def _next_activity(
        self,
        cycle: LearningCycle,
        risks: list[AIHealthRiskSignal],
        gaps: list[str],
    ) -> str:
        if any(risk.level in {"alto", "crítico"} for risk in risks):
            return "Rehacer el prompt con checklist de privacidad y seguridad antes de consultar nuevamente el modelo."
        if gaps:
            return "Completar una estación breve de IA clínica segura con crítica obligatoria de la salida generada."
        if cycle == LearningCycle.INTERNSHIP:
            return "Avanzar a un flujo con agentes: tutor, evaluador, simulador y debrief docente."
        return "Avanzar a un caso contrastante donde la IA omite una bandera roja y el estudiante debe detectarla."

    def _trajectory_note(
        self,
        request: AIHealthEvaluationRequest,
        overall: float,
        gaps: list[str],
    ) -> str:
        return (
            f"{request.student.name} obtiene {overall:.1f}/4 en Competencias IA/Salud Digital "
            f"para el ciclo {request.student.cycle.replace('_', ' ')}. "
            f"Persisten {len(gaps)} brecha(s) emergentes que deben integrarse al gemelo digital educativo."
        )

