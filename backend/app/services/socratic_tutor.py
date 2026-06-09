from app.schemas.common import LearningCycle
from app.schemas.tutor import (
    RubricFeedback,
    TutorBiasSignal,
    TutorIntent,
    TutorKnowledgeGap,
    TutorToolCall,
    TutorTurnRequest,
    TutorTurnResponse,
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


class SocraticTutorAgent:
    """Deterministic MVP tutor that asks the next best clinical reasoning question."""

    def generate_turn(self, request: TutorTurnRequest) -> TutorTurnResponse:
        response_text = request.latest_student_response.lower()
        mastery = {item.concept_id: item.mastery for item in request.student.knowledge_state}
        gaps = self._detect_gaps(request, response_text, mastery)
        biases = self._detect_biases(request, response_text)
        intent = self._select_intent(request.student.cycle, response_text, gaps)
        question = self._build_question(request, intent, gaps, biases)

        return TutorTurnResponse(
            teaching_style=request.student.cycle,
            intent=intent,
            should_withhold_final_answer=True,
            tutor_question=question,
            rationale_for_question=self._question_rationale(request.student.cycle, intent),
            detected_knowledge_gaps=gaps,
            detected_biases=biases,
            rubric_feedback=self._rubric_feedback(request, response_text, gaps, biases),
            suggested_tool_calls=self._suggest_tools(request, gaps, biases),
            stop_condition=(
                "Entrega una explicación concisa solo después de que el estudiante haya formulado "
                "una representación del problema, nombrado alternativas peligrosas y justificado "
                "la siguiente acción."
            ),
        )

    def _detect_gaps(
        self,
        request: TutorTurnRequest,
        response_text: str,
        mastery: dict[str, float],
    ) -> list[TutorKnowledgeGap]:
        gaps: list[TutorKnowledgeGap] = []
        required = request.clinical_case.required_concepts
        mentioned_terms = {
            "ecg_initial_interpretation": ["ecg", "electro", "st elevation", "elevación del st", "stemi", "ischemic", "isquémic"],
            "troponin_kinetics": ["troponin", "troponina", "serial", "seriada", "repeat", "repetir"],
            "acs_risk_stratification": ["risk", "riesgo", "acs", "sca", "acute coronary", "coronario agudo", "unstable", "inestable"],
            "initial_acs_management": ["aspirin", "aspirina", "monitor", "cardiology", "cardiología", "management", "manejo", "treat", "tratar"],
            "differential_diagnosis_chest_pain": ["differential", "diferencial", "pe", "tep", "aortic", "aórtic", "pneumothorax", "neumotórax", "reflux", "reflujo"],
            "chest_pain_red_flags": ["exertional", "esfuerzo", "diaphoresis", "diaforesis", "radiation", "irradiación", "risk factors", "factores de riesgo"],
        }

        for concept_id in required:
            score = mastery.get(concept_id, 0.0)
            terms = mentioned_terms.get(concept_id, [])
            is_missing_from_response = terms and not any(term in response_text for term in terms)
            if score < 0.7 or is_missing_from_response:
                severity = "high" if score < 0.4 else "moderate"
                evidence = (
                    f"Estimación de dominio {score:.0%}; la respuesta del estudiante no mostró "
                    f"evidencia suficiente para {CONCEPT_LABELS.get(concept_id, concept_id)}."
                )
                gaps.append(
                    TutorKnowledgeGap(
                        concept_id=concept_id,
                        label=CONCEPT_LABELS.get(concept_id, concept_id.replace("_", " ").title()),
                        severity=severity,
                        evidence=evidence,
                    )
                )
        return gaps[:3]

    def _detect_biases(self, request: TutorTurnRequest, response_text: str) -> list[TutorBiasSignal]:
        biases: list[TutorBiasSignal] = []
        benign_terms = ["reflux", "reflujo", "anxiety", "ansiedad", "muscle strain", "contractura"]
        acs_terms = ["acs", "sca", "acute coronary", "coronario agudo"]
        if any(term in response_text for term in benign_terms) and not any(term in response_text for term in acs_terms):
            biases.append(
                TutorBiasSignal(
                    bias="premature_closure",
                    risk_level="high",
                    evidence="El estudiante pasó a una explicación benigna antes de abordar banderas rojas de SCA.",
                    debiasing_move="Pedirle que identifique primero el diagnóstico peligroso que no puede omitir.",
                )
            )
        if "first" not in response_text and request.student.cycle == LearningCycle.INTERNSHIP:
            biases.append(
                TutorBiasSignal(
                    bias="poor_prioritization",
                    risk_level="moderate",
                    evidence="La respuesta no secuencia con claridad las acciones inmediatas de seguridad.",
                    debiasing_move="Preguntar qué acción debe ocurrir en los primeros cinco minutos y por qué.",
                )
            )
        if any(
            term in response_text
            for term in [
                "normal troponin",
                "negative troponin",
                "troponin is negative",
                "troponina normal",
                "troponina negativa",
                "troponina es negativa",
            ]
        ):
            biases.append(
                TutorBiasSignal(
                    bias="overconfidence",
                    risk_level="moderate",
                    evidence="La respuesta puede estar sobrevalorando un biomarcador temprano aislado.",
                    debiasing_move="Preguntar cómo el tiempo de evolución cambia la interpretación de una troponina negativa.",
                )
            )
        return biases

    def _select_intent(
        self,
        cycle: LearningCycle,
        response_text: str,
        gaps: list[TutorKnowledgeGap],
    ) -> TutorIntent:
        if cycle == LearningCycle.BASIC_SCIENCES:
            return TutorIntent.PROBE_MECHANISM
        if cycle == LearningCycle.INTERNSHIP:
            if any(gap.concept_id == "initial_acs_management" for gap in gaps):
                return TutorIntent.PROBE_MANAGEMENT
            return TutorIntent.PROBE_SAFETY
        if "differential" not in response_text and "acs" not in response_text:
            return TutorIntent.PROBE_DIFFERENTIAL
        return TutorIntent.PROBE_DATA_INTERPRETATION

    def _build_question(
        self,
        request: TutorTurnRequest,
        intent: TutorIntent,
        gaps: list[TutorKnowledgeGap],
        biases: list[TutorBiasSignal],
    ) -> str:
        if request.student.cycle == LearningCycle.BASIC_SCIENCES:
            return (
                "Antes de nombrar el diagnóstico, ¿qué mecanismo podría explicar presión "
                "subesternal con el esfuerzo, irradiación al brazo izquierdo y diaforesis?"
            )
        if request.student.cycle == LearningCycle.CLINICAL_SCIENCES:
            if biases:
                return (
                    "¿Qué causas peligrosas de dolor torácico deben permanecer en tu diferencial "
                    "antes de aceptar una explicación benigna, y qué datos del caso apoyan cada una?"
                )
            return (
                "Construye una representación del problema en una frase; luego nombra tus tres "
                "diagnósticos principales y el dato que más cambiaría tu priorización."
            )
        if intent == TutorIntent.PROBE_MANAGEMENT:
            return (
                "En los primeros cinco minutos, ¿qué harías para mantener seguro a este paciente "
                "mientras el diagnóstico todavía es incierto?"
            )
        if any(gap.concept_id == "troponin_kinetics" for gap in gaps) or any(
            bias.bias == "overconfidence" for bias in biases
        ):
            return (
                "Si la primera troponina es negativa, ¿qué haría inseguro dar de alta a este "
                "paciente de inmediato?"
            )
        return (
            "¿Cuál es tu prioridad inmediata, qué incertidumbre persiste y cuándo escalarías "
            "a un superior o a cardiología?"
        )

    def _question_rationale(self, cycle: LearningCycle, intent: TutorIntent) -> str:
        rationales = {
            LearningCycle.BASIC_SCIENCES: "El estudiante necesita fortalecer mecanismos causales antes de etiquetar diagnósticos.",
            LearningCycle.CLINICAL_SCIENCES: "El estudiante necesita organizar los datos en diagnóstico diferencial y rasgos discriminantes.",
            LearningCycle.INTERNSHIP: "El estudiante necesita priorizar seguridad, escalamiento y acción bajo incertidumbre.",
        }
        return f"{rationales[cycle]} Intención pedagógica actual: {intent.value}."

    def _rubric_feedback(
        self,
        request: TutorTurnRequest,
        response_text: str,
        gaps: list[TutorKnowledgeGap],
        biases: list[TutorBiasSignal],
    ) -> list[RubricFeedback]:
        red_flags_named = sum(flag.lower() in response_text for flag in request.clinical_case.red_flags)
        reasoning_score = 3 if red_flags_named >= 2 and not biases else 2 if red_flags_named else 1
        safety_score = 3 if any(term in response_text for term in ["ecg", "monitor", "serial troponin", "troponina seriada"]) else 1
        metacognition_score = 3 if any(term in response_text for term in ["uncertain", "incierto", "incertidumbre", "rule out", "descartar", "differential", "diferencial"]) else 1

        if gaps:
            reasoning_score = min(reasoning_score, 2)

        return [
            RubricFeedback(
                criterion="clinical_reasoning",
                score=reasoning_score,
                rationale="Evalúa si el estudiante conecta los datos del caso con un razonamiento diagnóstico priorizado.",
                next_step="Formula la representación del problema y justifica el diagnóstico principal frente a alternativas.",
            ),
            RubricFeedback(
                criterion="patient_safety",
                score=safety_score,
                rationale="Evalúa si el estudiante identifica necesidades urgentes de evaluación y monitorización.",
                next_step="Nombra la acción inmediata que reduce riesgo mientras persiste la incertidumbre.",
            ),
            RubricFeedback(
                criterion="metacognition",
                score=metacognition_score,
                rationale="Evalúa conciencia de incertidumbre, calibración y monitoreo de sesgos.",
                next_step="Di qué evidencia cambiaría tu hipótesis y qué sesgo estás vigilando.",
            ),
        ]

    def _suggest_tools(
        self,
        request: TutorTurnRequest,
        gaps: list[TutorKnowledgeGap],
        biases: list[TutorBiasSignal],
    ) -> list[TutorToolCall]:
        tools = [
            TutorToolCall(
                tool_name="retrieve_curriculum_concepts",
                purpose="Buscar conceptos prerrequisito conectados con la brecha detectada.",
                inputs={"concept_ids": [gap.concept_id for gap in gaps]},
            )
        ]
        if biases:
            tools.append(
                TutorToolCall(
                    tool_name="select_cognitive_forcing_prompt",
                    purpose="Elegir una pregunta de desesgo para el patrón cognitivo detectado.",
                    inputs={"biases": [bias.bias for bias in biases]},
                )
            )
        if request.student.cycle == LearningCycle.INTERNSHIP:
            tools.append(
                TutorToolCall(
                    tool_name="generate_branching_simulation_step",
                    purpose="Crear el siguiente paso de simulación con presión de tiempo y foco en seguridad.",
                    inputs={"domain": request.clinical_case.domain, "setting": request.clinical_case.setting},
                )
            )
        return tools
