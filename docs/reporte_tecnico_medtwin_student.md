# Reporte Técnico de MedTwin Student

## 1. Resumen Ejecutivo

**MedTwin Student** es un MVP de gemelo digital educativo para estudiantes de medicina. Su propósito es modelar, evaluar y acompañar la trayectoria de aprendizaje del estudiante a través de competencias clínicas core y competencias emergentes en IA/Salud Digital.

El sistema permite:

- Evaluar razonamiento clínico en casos específicos.
- Identificar brechas cognitivas y sesgos.
- Evaluar el uso de modelos de IA médica como competencia emergente.
- Activar un tutor socrático adaptado al ciclo formativo.
- Simular cambios en dominio y riesgo educativo tras intervenciones.
- Generar la base conceptual para planes de enseñanza de precisión.
- Proyectar una arquitectura paralela para gemelos digitales de profesores.

El MVP está organizado como una aplicación full-stack:

```text
Backend: FastAPI
Frontend: Vite/Lovable o Next.js
Base de datos: PostgreSQL
IA generativa: API OpenAI-compatible vía OpenRouter
Despliegue backend: Render
Repositorio: GitHub
```

Repositorio:

```text
https://github.com/docpino2/MedTwinStudent
```

## 2. Objetivo del Sistema

El objetivo de MedTwin Student es responder de manera longitudinal a cinco preguntas educativas:

1. ¿Cómo razona clínicamente el estudiante?
2. ¿Qué brechas tiene en competencias médicas core?
3. ¿Cómo usa modelos de IA médica y agentes educativos?
4. ¿Qué riesgos cognitivos, éticos o digitales emergen?
5. ¿Qué intervención educativa personalizada debe recibir y cómo cambia después?

La visión no es solo construir un chatbot o un dashboard, sino un sistema de **diagnóstico cognitivo integral y enseñanza de precisión**.

## 3. Secuencia Pedagógica del Gemelo Digital del Estudiante

El flujo refinado del gemelo digital se estructura en cinco fases principales:

```text
1. Diagnóstico cognitivo integral
   1.1 Análisis de caso clínico en dominio específico
   1.2 Análisis de uso de modelos de IA médica

2. Generación de plan especializado de enseñanza
   basado en brechas core y emergentes

3. Adaptación del OxTutor IA y tutor humano
   para desarrollar el plan

4. Estrategias discriminadas y plan de seguimiento

5. Nueva evaluación secuencial
   con detección de cambios cognitivos y de aprendizaje
```

Este flujo permite observar al estudiante como un sistema dinámico: sus conocimientos, sesgos, estrategias de razonamiento, uso de IA, metacognición y respuesta a intervenciones evolucionan con el tiempo.

## 4. Fundamento Conceptual

El MVP incorpora cuatro fundamentos:

### 4.1 Medicina y Razonamiento Clínico

- Representación del problema.
- Diagnóstico diferencial.
- Priorización de diagnósticos peligrosos.
- Interpretación de datos clínicos.
- Seguridad del paciente.
- Disposición y escalamiento.

### 4.2 Ciencia Cognitiva

- Formación de esquemas.
- Recuperación activa.
- Transferencia.
- Calibración de confianza.
- Carga cognitiva.
- Detección de sesgos.
- Metacognición.

### 4.3 Pensamiento Complejo

- Trayectorias no lineales.
- Interacción entre contexto, conocimiento y desempeño.
- Evaluación longitudinal.
- Emergencia de competencias.
- Adaptación dinámica de intervenciones.

### 4.4 IA en Educación Médica de Pregrado

El refinamiento incorpora el marco de Cheng et al. en BMC Medical Education 2026, que plantea siete dominios para integrar IA en pregrado médico:

```text
1. Conocimiento fundacional de IA
2. Aplicación de IA
3. Colaboración humano-IA
4. Implicaciones éticas y sociales
5. Evaluación y assessment
6. Investigación e innovación con IA
7. Colaboración interorganizacional
```

Estos dominios se entienden como un ciclo longitudinal, no como una jerarquía fija.

## 5. Arquitectura General del Repositorio

```text
MedTwinStudent/
  backend/
    app/
      api/v1/
      core/
      models/
      schemas/
      services/
      db_init.py
    db/
      schema.sql
      seeds/
    evals/
    tests/
  frontend/
    app/
    components/
    lib/
  docs/
  schemas/
  infra/
  render.yaml
```

## 6. Backend

El backend está construido en FastAPI y organizado por responsabilidad funcional.

### 6.1 Capas

```text
api/v1      → routers HTTP
schemas     → contratos Pydantic
services    → lógica de dominio
models      → modelos SQLAlchemy
core        → configuración y base de datos
db          → schema SQL y seeds
evals       → entorno de evaluación de salidas
tests       → pruebas automatizadas
```

### 6.2 Endpoints Principales

```text
GET  /health

GET  /api/v1/students
GET  /api/v1/cases?domain=chest_pain
GET  /api/v1/curriculum/concepts
GET  /api/v1/curriculum/graph

POST /api/v1/reasoning/analyze
POST /api/v1/tutor/turn
POST /api/v1/simulation/simulate

GET  /api/v1/ai-health/competencies
POST /api/v1/ai-health/evaluate
```

## 7. Módulo de Competencias Core

Las competencias core representan el desempeño médico tradicional del estudiante.

### 7.1 Ciclos Formativos

```text
Ciencias básicas
Ciencias clínicas
Internado
```

### 7.2 Competencias Evaluadas

```text
fisiopatología
banderas rojas
diagnóstico diferencial
interpretación inicial del ECG
estratificación de riesgo
cinética de troponinas
manejo inicial
seguridad clínica
metacognición
comunicación clínica
```

### 7.3 Servicio Principal

```text
backend/app/services/reasoning_engine.py
```

### 7.4 Schema

```text
backend/app/schemas/reasoning.py
```

### 7.5 Endpoint

```text
POST /api/v1/reasoning/analyze
```

### 7.6 Entrada

```json
{
  "student": {},
  "clinical_case": {},
  "student_response": "..."
}
```

### 7.7 Salida

```json
{
  "reasoning_analysis": "...",
  "likely_knowledge_gaps": [],
  "cognitive_bias_risk": {},
  "feedback": "...",
  "next_recommended_activity": "...",
  "tutor_prompt": "...",
  "simulation_update": {}
}
```

### 7.8 Lógica Actual

El motor:

- Lee el perfil del estudiante.
- Compara dominio por concepto contra conceptos requeridos por el caso.
- Detecta brechas bajo umbral de competencia.
- Detecta banderas rojas omitidas.
- Estima riesgo de sesgo cognitivo.
- Genera retroalimentación y actividad recomendada.

La salida está en español.

## 8. Dominio Clínico Inicial

El dominio clínico semilla es:

```text
dolor torácico
```

Caso inicial:

```text
Paciente masculino de 58 años con presión torácica subesternal de esfuerzo,
irradiación al brazo izquierdo, náusea, diaforesis, hipertensión y tabaquismo.
```

Conceptos asociados:

```text
fisiopatología de isquemia miocárdica
banderas rojas en dolor torácico
interpretación inicial de ECG
estratificación de riesgo de SCA
cinética de troponinas
manejo inicial de SCA
diagnóstico diferencial de dolor torácico
```

## 9. Tutor Socrático OxTutor

El tutor socrático es una intervención formativa.

### 9.1 Servicio

```text
backend/app/services/socratic_tutor.py
```

### 9.2 Schema

```text
backend/app/schemas/tutor.py
```

### 9.3 Endpoint

```text
POST /api/v1/tutor/turn
```

### 9.4 Funciones

El tutor:

- Evita entregar respuesta final de inmediato.
- Formula una pregunta progresiva.
- Detecta brechas de conocimiento.
- Detecta sesgos cognitivos.
- Devuelve feedback con rúbrica 0-4.
- Adapta estilo al ciclo formativo.

### 9.5 Adaptación por Ciclo

```text
Ciencias básicas:
  mecanismos, conceptos, causalidad

Ciencias clínicas:
  diagnóstico diferencial, discriminadores, razonamiento clínico

Internado:
  priorización, seguridad, incertidumbre, escalamiento y restricciones del sistema
```

## 10. Módulo de Competencias Emergentes IA/Salud Digital

Este módulo evalúa el uso de modelos de IA médica como competencia explícita del estudiante.

### 10.1 Servicio

```text
backend/app/services/ai_health_competency_engine.py
```

### 10.2 Schema

```text
backend/app/schemas/ai_health.py
```

### 10.3 Endpoints

```text
GET  /api/v1/ai-health/competencies
POST /api/v1/ai-health/evaluate
```

### 10.4 Competencias Emergentes

```text
formulación de preguntas clínicas para IA
prompting clínico responsable
crítica de salidas IA
razonamiento diferencial aumentado por IA
aprendizaje autorregulado con IA
privacidad y gobernanza
orquestación de agentes
metacognición aumentada por IA
```

### 10.5 Entrada de Evaluación

```json
{
  "student": {},
  "clinical_case": {},
  "intent": "differential_diagnosis",
  "student_ai_prompt": "...",
  "ai_model_output": "...",
  "student_critique": "...",
  "declared_uncertainty": "...",
  "used_patient_identifiers": false,
  "cited_sources_or_guidelines": true,
  "escalated_to_human_supervisor": false
}
```

### 10.6 Salida

```json
{
  "cycle": "...",
  "overall_score": 0,
  "mastery_level": "...",
  "competency_scores": [],
  "detected_risks": [],
  "emerging_competency_gaps": [],
  "feedback": "...",
  "recommended_remediation": [],
  "next_recommended_activity": "...",
  "digital_health_trajectory_note": "..."
}
```

### 10.7 Criterios Evaluados

El motor evalúa:

- Calidad y contexto del prompt.
- Seguridad y privacidad.
- Crítica de la salida IA.
- Verificación contra guías, fuentes o datos del caso.
- Razonamiento diferencial aumentado por IA.
- Metacognición.
- Riesgo de sobredependencia.
- Riesgo de aceptación acrítica.
- Escalamiento humano.

### 10.8 Riesgos Detectados

```text
riesgo de privacidad
sobredependencia de IA
aceptación acrítica de salida IA
falta de escalamiento supervisado
```

## 11. Schema Global de Competencias

Archivo:

```text
schemas/competency_model.schema.json
```

Se extendió con:

```text
core_competency_family:
  ai_digital_health

assessment_methods:
  ai_prompt_review
  ai_output_critique
  agent_workflow_review

failure_modes:
  ai_overreliance
  privacy_violation
  uncritical_ai_acceptance
  unsafe_ai_workflow

remediation_strategies:
  safe_ai_prompting_practice
  ai_output_verification
  agent_workflow_simulation
  privacy_governance_checklist
```

## 12. Learning Simulation Engine

El motor de simulación estima cambios en el gemelo digital tras una intervención.

### 12.1 Servicio

```text
backend/app/services/learning_simulation_engine.py
```

### 12.2 Endpoint

```text
POST /api/v1/simulation/simulate
```

### 12.3 Entrada

```text
perfil del estudiante
mapa de competencias
puntajes basales
desempeño en caso clínico
tipo de intervención
calidad del feedback
tiempo invertido
nivel de dificultad
pesos configurables
```

### 12.4 Salida

```text
puntajes actualizados
reducción de riesgo predicha
brechas remanentes
actividad recomendada
resumen de trayectoria
configuración usada
```

### 12.5 Modelo Matemático

```text
driver =
  w_performance * desempeño
  + w_intervention * efecto_intervención
  + w_feedback * calidad_feedback
  + w_time * tiempo
  + w_difficulty * alineación_dificultad
```

Luego:

```text
updated_mastery = baseline_mastery + delta
```

El modelo es transparente y configurable.

## 13. Diagnóstico Cognitivo Integral

El diagnóstico cognitivo integral debe fusionar:

```text
diagnóstico core
diagnóstico IA/Salud Digital
sesgos humanos
riesgos digitales
metacognición
seguridad
trayectoria
```

Actualmente puede componerse en frontend usando:

```text
POST /api/v1/reasoning/analyze
POST /api/v1/ai-health/evaluate
```

Próximo módulo recomendado:

```text
Integrated Cognitive Diagnosis Engine
```

Endpoint propuesto:

```text
POST /api/v1/integrated-diagnosis/student
```

## 14. Plan de Enseñanza de Precisión

El plan debe derivarse de:

```text
brechas core
brechas IA/Digital
ciclo formativo
riesgos detectados
respuesta a intervención
```

Debe producir:

```text
objetivo clínico
objetivo IA/Digital
estrategia con OxTutor
estrategia con tutor humano
actividad recomendada
criterio de éxito
intervalo de seguimiento
criterio de reevaluación
```

Próximo módulo recomendado:

```text
Teaching Precision Plan Engine
```

Endpoint propuesto:

```text
POST /api/v1/teaching-plan/generate
```

## 15. Reevaluación Secuencial

La reevaluación secuencial debe detectar cambio cognitivo y de aprendizaje.

Variables sugeridas:

```text
cambio en representación del problema
cambio en priorización de diagnósticos peligrosos
cambio en calidad del prompt IA
cambio en crítica de salida IA
cambio en calibración de confianza
persistencia o resolución de sesgo
transferencia a caso nuevo
```

Salidas sugeridas:

```text
cognitive_change_detected
change_type
evidence_of_transfer
persistent_gap
next_teaching_decision
```

Próximo módulo recomendado:

```text
Sequential Reassessment Engine
```

Endpoint propuesto:

```text
POST /api/v1/reassessment/sequential
```

## 16. Gemelo Digital de Profesores

Se creó una estructura inicial para modelar profesores.

Archivo:

```text
schemas/professor_twin.schema.json
```

### 16.1 Objetivo

El gemelo docente busca responder:

```text
¿Cómo enseña este profesor, cómo usa IA en docencia,
qué brechas pedagógicas tiene y cómo mejora su capacidad de guiar estudiantes?
```

### 16.2 Dimensiones

```text
perfil pedagógico
competencias docentes core
competencias IA/Salud Digital docentes
evidencias de enseñanza
riesgos pedagógicos
plan de desarrollo docente
```

### 16.3 Competencias Docentes Core

```text
diseño de objetivos
enseñanza basada en casos
feedback efectivo
evaluación por rúbrica
tutoría socrática
supervisión clínica
alineación constructiva
seguimiento longitudinal
```

### 16.4 Competencias Docentes IA/Salud Digital

```text
diseño de actividades con IA
evaluación de prompts estudiantiles
curación de casos con IA
detección de sobredependencia IA
evaluación de salidas IA
gobernanza y privacidad
orquestación de agentes educativos
diseño de evaluación longitudinal
```

### 16.5 Riesgos Pedagógicos

```text
evaluación mal alineada
feedback genérico
actividad IA insegura
brecha de privacidad
sobredependencia en outputs IA
supervisión humana insuficiente
seguimiento longitudinal débil
```

## 17. Infraestructura

### 17.1 GitHub

```text
https://github.com/docpino2/MedTwinStudent
```

### 17.2 Render

Backend desplegado como Web Service.

Variables relevantes:

```env
PYTHON_VERSION=3.11.11
DATABASE_URL=postgresql+psycopg://...
BACKEND_CORS_ORIGINS=...
BACKEND_CORS_ORIGIN_REGEX=https://.*\.lovable\.app
OPENAI_API_KEY=sk-or-...
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4o-mini
INIT_DB_ON_STARTUP=true
```

### 17.3 Inicialización de Base de Datos

Archivo:

```text
backend/app/db_init.py
```

Comando:

```bash
python -m app.db_init
```

También puede ejecutarse automáticamente al arranque si:

```env
INIT_DB_ON_STARTUP=true
```

## 18. Frontend

El frontend debe organizarse como flujo secuencial, no como dashboard saturado.

Secuencia recomendada:

```text
1. Diagnóstico Integral
2. Plan de Enseñanza
3. OxTutor + Tutor Humano
4. Seguimiento
5. Reevaluación
```

Con subcomponentes:

```text
ClinicalCaseAnalysisPanel
AIHealthAnalysisPanel
PrecisionTeachingPlanStep
TutorAdaptationStep
FollowUpStrategyStep
SequentialReassessmentStep
TwinStateSidebar
```

Regla estricta:

```text
Toda la interfaz debe estar en español.
No se deben mostrar enums internos en inglés.
```

## 19. Evaluación y Pruebas

Suite actual:

```text
14 tests
```

Cobertura:

```text
Reasoning Engine
Socratic Tutor
Learning Simulation Engine
AI/Health Competency Engine
API endpoints
Eval Harness
```

Entorno de evaluación:

```text
backend/evals/verify_outputs.py
```

Valida:

- Salidas en español.
- Tutor retiene respuesta final.
- Detección de brechas.
- Actualización de dominio.
- Escenarios por ciclo.

## 20. Estado Actual

El MVP ya cuenta con:

```text
backend modular
evaluación core
evaluación IA/Salud Digital
tutor socrático
simulación de aprendizaje
documentación pedagógica
schema de gemelo docente
deploy en Render
conexión preparada con Lovable
```

## 21. Próximos Pasos Técnicos

### Prioridad 1

Crear motor de diagnóstico integral:

```text
Integrated Cognitive Diagnosis Engine
```

### Prioridad 2

Crear motor de plan de enseñanza:

```text
Teaching Precision Plan Engine
```

### Prioridad 3

Crear motor de reevaluación secuencial:

```text
Sequential Reassessment Engine
```

### Prioridad 4

Implementar backend del gemelo docente:

```text
Professor Twin Engine
Faculty AI/Digital Health Competency Engine
```

### Prioridad 5

Persistencia real de sesiones:

```text
student_sessions
case_attempts
ai_health_attempts
tutor_interactions
simulation_runs
teaching_plans
reassessment_events
```

## 22. Conclusión

MedTwin Student ya tiene una base técnica y pedagógica sólida para evolucionar hacia una plataforma de enseñanza médica adaptativa. La arquitectura actual permite evaluar competencias clínicas core y competencias emergentes IA/Salud Digital, generar tutoría socrática y simular trayectorias de aprendizaje.

La siguiente etapa debe mover la integración desde composición frontend hacia motores backend especializados para:

```text
diagnóstico integral
plan de enseñanza de precisión
reevaluación secuencial
gemelo digital docente
```

Esto permitirá que el sistema pase de MVP funcional a plataforma longitudinal de medicina educativa aumentada por IA.

