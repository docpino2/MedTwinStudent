# Refinamiento del MVP: Gemelo Digital Educativo + Competencias IA/Salud Digital

Este documento traduce el marco de integración de IA en pregrado médico revisado en el artículo de Cheng et al. BMC Medical Education 2026, DOI `10.1186/s12909-026-08620-1`, a una hoja de ruta para MedTwin Student.

El hallazgo central útil para nuestro MVP es que la IA en medicina no debe agregarse como un curso periférico. Debe integrarse como una trayectoria longitudinal y cíclica que combine conocimiento fundacional, aplicación, colaboración humano-IA, ética, evaluación, investigación e interacción entre actores institucionales. Esto encaja bien con un gemelo digital porque permite observar cambios cognitivos, conductuales, éticos y pedagógicos a lo largo del tiempo.

## 1. Principio de Diseño

MedTwin Student debe evolucionar desde un “evaluador de caso” hacia un **sistema de diagnóstico y prescripción educativa de precisión**.

El gemelo no solo responde:

```text
¿Qué sabe el estudiante?
```

Debe responder:

```text
¿Cómo razona el estudiante, cómo usa IA, qué riesgos emergen, qué intervención requiere y cómo cambia después?
```

## 2. Flujo Refinado del Gemelo Digital del Estudiante

### Paso 1. Diagnóstico Cognitivo Integral del Estudiante

El diagnóstico inicial debe tener dos entradas complementarias.

#### 1.1. Análisis de Caso Clínico en Dominio Específico

Entrada:

- Perfil del estudiante.
- Ciclo formativo.
- Caso clínico.
- Respuesta inicial del estudiante.
- Dominio clínico, por ejemplo dolor torácico.

Evaluación:

- Representación del problema.
- Diagnóstico diferencial.
- Priorización de diagnósticos peligrosos.
- Interpretación de datos.
- Seguridad clínica.
- Metacognición.
- Sesgos cognitivos.

Salida:

- Brechas en competencias core.
- Riesgo educativo clínico.
- Sesgos probables.
- Nivel de dominio por concepto.

Backend actual relacionado:

```text
POST /api/v1/reasoning/analyze
POST /api/v1/tutor/turn
POST /api/v1/simulation/simulate
```

#### 1.2. Análisis de Uso de Modelos de IA Médica

Entrada:

- Prompt clínico del estudiante.
- Salida generada por IA.
- Crítica del estudiante a la salida.
- Declaración de incertidumbre.
- Indicadores de privacidad, fuentes y escalamiento.

Evaluación:

- Formulación de pregunta clínica.
- Prompting responsable.
- Crítica de salida IA.
- Verificación contra evidencia y guías.
- Detección de omisiones o alucinaciones.
- Privacidad y gobernanza.
- Sobredependencia IA.
- Colaboración humano-IA.

Salida:

- Brechas en competencias IA/Salud Digital.
- Riesgo de privacidad.
- Riesgo de aceptación acrítica.
- Riesgo de sobredependencia.
- Nivel de dominio IA/Digital.

Backend actual relacionado:

```text
GET /api/v1/ai-health/competencies
POST /api/v1/ai-health/evaluate
```

## 3. Diagnóstico Cognitivo Integral: Core + IA/Digital

El paso de razonamiento integral debe fusionar ambos diagnósticos.

### Matriz de Integración

| Dimensión | Pregunta | Fuente |
| --- | --- | --- |
| Competencias core | ¿Qué brecha clínica limita el razonamiento? | Reasoning Engine |
| Competencias IA/Digital | ¿Cómo usa IA para ampliar o distorsionar su razonamiento? | AI Health Engine |
| Seguridad | ¿Hay riesgo de acción insegura o alta prematura? | Reasoning + AI Health |
| Sesgos | ¿Qué sesgo humano o socio-técnico aparece? | Tutor + AI Health |
| Metacognición | ¿Reconoce incertidumbre y límites? | Tutor + AI Health |
| Trayectoria | ¿Qué cambió después de intervención? | Simulation Engine |

### Nuevos Indicadores Recomendados

- `clinical_gap_priority`: brecha clínica prioritaria.
- `ai_digital_gap_priority`: brecha IA/Digital prioritaria.
- `combined_risk_level`: riesgo integrado.
- `overreliance_risk`: riesgo de delegar juicio a IA.
- `verification_quality`: calidad de verificación de salida IA.
- `human_ai_collaboration_score`: capacidad de colaboración humano-IA.
- `ethical_governance_score`: privacidad, sesgo, transparencia y responsabilidad.
- `learning_change_signal`: evidencia de cambio cognitivo después de intervención.

## 4. Plan Especializado de Enseñanza de Precisión

El plan no debe ser genérico. Debe derivarse de:

```text
competencias core + competencias emergentes + ciclo formativo + riesgo + respuesta a intervención
```

### Componentes del Plan

- Objetivo clínico principal.
- Objetivo IA/Salud Digital principal.
- Estrategia docente.
- Actividad con OxTutor.
- Actividad con tutor humano.
- Evidencia esperada de mejora.
- Criterio de reevaluación.
- Plazo de seguimiento.

### Ejemplo

```text
Brecha core:
No integra cinética de troponinas con disposición segura.

Brecha IA/Digital:
Acepta salida IA sin verificar omisión de diagnósticos peligrosos.

Plan:
1. Caso contrastante de dolor torácico con primera troponina negativa.
2. Prompt controlado para pedir diferencial y límites de IA.
3. Crítica obligatoria de salida IA.
4. Tutor socrático enfocado en alta insegura.
5. Reevaluación con caso nuevo en 7 días.
```

## 5. Adaptación del OxTutor IA y del Tutor Humano

El tutor IA y el tutor humano deben tener roles complementarios.

### OxTutor IA

Debe encargarse de:

- Preguntas socráticas progresivas.
- Práctica deliberada.
- Detección temprana de brechas.
- Feedback inmediato.
- Simulaciones repetibles.
- Crítica de prompts y salidas IA.
- Preparación para sesión humana.

### Tutor Humano

Debe encargarse de:

- Juicio educativo complejo.
- Profesionalismo.
- Priorización de alto impacto.
- Contexto institucional.
- Acompañamiento emocional y ético.
- Decisión de escalamiento.
- Validación final de progreso.

### Regla de Orquestación

```text
OxTutor entrena y evidencia.
Tutor humano interpreta, prioriza y decide.
```

## 6. Estrategias Discriminadas por Ciclo

### Ciencias Básicas

Foco core:

- Mecanismos.
- Conceptos.
- Causalidad.
- Integración básico-clínica.

Foco IA/Digital:

- Vocabulario IA/ML/GenAI.
- Métricas básicas.
- Hallucinations.
- Incertidumbre.
- Uso de IA para estudiar, no para copiar.

Intervenciones:

- Microlección mecanística.
- Mapa conceptual.
- Prompt de explicación fisiopatológica.
- Autoevaluación generada por IA.

### Ciencias Clínicas

Foco core:

- Diagnóstico diferencial.
- Discriminadores.
- Interpretación de pruebas.
- Sesgos cognitivos.

Foco IA/Digital:

- Prompting clínico responsable.
- Verificación de salida IA.
- Detección de omisiones peligrosas.
- Evaluación crítica.

Intervenciones:

- Caso contrastante.
- Crítica de respuesta IA incompleta.
- Checklist de red flags.
- Tutor socrático sobre cierre prematuro.

### Internado

Foco core:

- Priorización.
- Seguridad.
- Disposición.
- Escalamiento.
- Restricciones del sistema.

Foco IA/Digital:

- Privacidad.
- Gobernanza.
- Documentación de uso IA.
- Colaboración humano-IA en equipo.
- Uso de agentes bajo supervisión.

Intervenciones:

- Simulación con presión de tiempo.
- Debrief de near-miss.
- Handoff con mención de incertidumbre.
- Escalamiento a tutor humano.

## 7. Nueva Evaluación Secuencial

El artículo enfatiza que la evaluación debe ser continua, no un punto final. En MedTwin eso se traduce en un módulo de reevaluación secuencial.

### Secuencia Recomendada

```text
Diagnóstico inicial
→ intervención OxTutor
→ intervención tutor humano
→ práctica o simulación
→ nueva evaluación
→ detección de cambio cognitivo
→ actualización del gemelo
→ nuevo plan
```

### Detección de Cambios Cognitivos

Variables:

- Cambio en representación del problema.
- Cambio en priorización de diagnósticos peligrosos.
- Cambio en calidad del prompt IA.
- Cambio en crítica de salida IA.
- Cambio en calibración de confianza.
- Persistencia o resolución de sesgo.
- Transferencia a caso nuevo.

### Salidas del Módulo de Reevaluación

- `cognitive_change_detected`: sí/no.
- `change_type`: conceptual, razonamiento, seguridad, IA/Digital, metacognición.
- `evidence_of_transfer`: baja/moderada/alta.
- `persistent_gap`: brecha persistente.
- `next_teaching_decision`: continuar, intensificar, cambiar estrategia, tutor humano.

## 8. Gemelo Digital de Profesores

El mismo enfoque debe aplicarse a docentes, pero el objeto no es “dominio clínico del caso”, sino **capacidad pedagógica adaptativa en entornos con IA**.

### Objetivo del Gemelo Docente

Responder:

```text
¿Cómo enseña este profesor, cómo usa IA en su docencia, qué brechas pedagógicas tiene y cómo mejora su capacidad de guiar estudiantes?
```

### Dimensiones del Gemelo Docente

#### 1. Perfil Pedagógico

- Rol.
- Departamento.
- Experiencia docente.
- Ciclos que enseña.
- Dominios clínicos.
- Estilo de enseñanza.
- Preferencias de feedback.

#### 2. Competencias Docentes Core

- Diseño de objetivos.
- Enseñanza basada en casos.
- Feedback efectivo.
- Evaluación por rúbrica.
- Tutoría socrática.
- Supervisión clínica.
- Alineación constructiva.

#### 3. Competencias IA/Salud Digital Docentes

- Diseño de actividades con IA.
- Evaluación de prompts estudiantiles.
- Curación de casos con IA.
- Detección de sobredependencia IA.
- Evaluación de outputs IA.
- Gobernanza y privacidad.
- Orquestación de agentes educativos.
- Diseño de evaluación longitudinal.

#### 4. Diagnóstico de Enseñanza

Entradas:

- Plan de clase.
- Caso diseñado.
- Rúbrica usada.
- Feedback emitido.
- Uso de IA en la actividad.
- Resultados de estudiantes.
- Auto-reflexión docente.

Salidas:

- Fortalezas docentes.
- Brechas pedagógicas.
- Riesgo de mala alineación evaluación-objetivo.
- Riesgo de uso superficial de IA.
- Recomendación de desarrollo docente.

#### 5. Plan de Desarrollo Docente

- Microcurso recomendado.
- Co-diseño con IA.
- Observación de clase.
- Revisión de rúbrica.
- Entrenamiento en feedback.
- Entrenamiento en privacidad/gobernanza IA.
- Seguimiento de impacto en estudiantes.

## 9. Arquitectura Recomendada

### Nuevos Módulos Backend

```text
Integrated Cognitive Diagnosis Engine
Teaching Precision Plan Engine
Sequential Reassessment Engine
Professor Twin Engine
Faculty AI/Digital Health Competency Engine
```

### Nuevos Endpoints Propuestos

```text
POST /api/v1/integrated-diagnosis/student
POST /api/v1/teaching-plan/generate
POST /api/v1/reassessment/sequential

GET  /api/v1/professors
POST /api/v1/professor-twin/diagnose
POST /api/v1/professor-twin/teaching-plan
POST /api/v1/professor-twin/reassess
```

## 10. Ajuste del Frontend

El flujo visual debería evolucionar a:

```text
Alumno
→ Caso
→ Diagnóstico Core
→ Diagnóstico IA/Salud Digital
→ Diagnóstico Integrado
→ Plan de Enseñanza
→ OxTutor + Tutor Humano
→ Reevaluación
→ Trayectoria
```

Para docentes:

```text
Profesor
→ Actividad docente
→ Diagnóstico pedagógico
→ Diagnóstico IA/Salud Digital docente
→ Plan de desarrollo docente
→ Seguimiento de impacto
```

## 11. Prioridades de Implementación

### Fase 1

- Añadir pantalla de Diagnóstico Integrado.
- Unificar salida de Reasoning Engine + AI Health Engine.
- Generar Plan de Enseñanza de precisión.

### Fase 2

- Crear módulo de Reevaluación Secuencial.
- Comparar caso inicial vs caso posterior.
- Detectar cambio cognitivo.

### Fase 3

- Crear Gemelo Digital Docente.
- Evaluar calidad de diseño pedagógico y uso docente de IA.
- Relacionar desempeño docente con evolución de estudiantes.

### Fase 4

- Analítica longitudinal por cohorte.
- Recomendaciones curriculares.
- Detección de brechas institucionales en IA/Salud Digital.

