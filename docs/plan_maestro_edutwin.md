# Plan Maestro EduTwin: Gemelo Digital Educativo Longitudinal

## 1. Propósito

Este plan maestro incorpora la hoja de ruta priorizada para transformar el MVP actual de **MedTwin Student** en **EduTwin**, una plataforma escalable de gemelos digitales educativos.

La marca paraguas es:

```text
EduTwin
```

El MVP actual se mantiene en:

```text
/Users/oxler/Documents/New project/MedTwinStudent
```

El objetivo no es agregar más agentes por acumulación, sino cerrar el ciclo educativo longitudinal:

```text
evidencia observada
→ estimación con incertidumbre
→ intervención
→ nueva evidencia
→ actualización del gemelo
→ decisión educativa
```

Todo texto visible para estudiante o docente debe permanecer en **español**.

## 2. Estado Operativo Actual

### Backend

Backend FastAPI desplegado en Render:

```text
https://medtwin-student-api.onrender.com
```

Endpoints actuales:

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

### Frontend

El frontend productivo está en Lovable:

```text
https://edugemelodigital.lovable.app
```

Importante:

```text
El frontend Next.js local no es la fuente de verdad productiva.
No debe modificarse como si fuera el frontend real.
Los cambios de interfaz deben entregarse como prompts/instrucciones para Lovable.
```

### Base de Datos

PostgreSQL está desplegado en Render, pero la implementación productiva todavía no usa repositorios PostgreSQL como fuente principal para todos los flujos. Persisten flujos basados en seeds y servicios determinísticos.

## 3. Diagnóstico Técnico-Pedagógico

La visión pedagógica del proyecto es sólida. El MVP ya representa:

- competencias clínicas core;
- competencias emergentes IA/Salud Digital;
- tutoría socrática;
- simulación de aprendizaje;
- pruebas de salidas en español;
- documentación técnica;
- despliegue backend funcional.

Sin embargo, el MVP actual todavía opera principalmente como:

```text
evaluador determinístico sobre datos semilla
```

y no todavía como:

```text
gemelo digital longitudinal basado en evidencia persistente
```

La brecha principal no es conceptual. Es de **persistencia, trazabilidad, evidencia observada, incertidumbre y cierre longitudinal del ciclo educativo**.

## 4. Principios de Arquitectura Pedagógica

### 4.1 Fuente de Verdad en Backend

El navegador no debe enviar perfiles completos de dominio, rúbricas autoritativas o casos completos como si fueran verdad confiable.

El frontend debe enviar:

```text
student_id
case_version_id
session_id
respuesta del estudiante
confianza antes/después
metadatos de interacción
```

El backend debe cargar:

```text
perfil real del estudiante
versión del caso
rúbrica
estado longitudinal
estimaciones previas
historial de evidencia
```

### 4.2 Evidencia Antes que Score

Cada inferencia debe poder reconstruirse desde evidencia.

Regla:

```text
estado anterior + evidencia + versión del modelo = estado nuevo
```

### 4.3 Predicción Separada de Observación

El sistema debe separar:

```text
predicted_learning_gain
observed_learning_gain
predicted_risk
observed_transfer_risk
```

### 4.4 IA Bajo Control

El LLM debe interpretar lenguaje y generar diálogo, pero no debe controlar todo el ciclo.

Regla:

```text
LLM interpreta y dialoga.
Rúbricas validan.
Motor longitudinal actualiza.
Docente revisa y puede hacer override.
```

## 5. Secuencia Objetivo del Gemelo Digital del Estudiante

### Fase 1. Diagnóstico Cognitivo Integral

#### 1.1 Análisis de Caso Clínico en Dominio Específico

Entrada mínima:

```text
student_id
case_version_id
session_id
respuesta del estudiante
confianza pre-respuesta
confianza post-respuesta
tiempo de respuesta
pistas usadas
```

Evaluación:

- representación del problema;
- razonamiento mecanístico;
- diagnóstico diferencial;
- priorización de riesgo;
- seguridad clínica;
- metacognición;
- sesgos cognitivos.

#### 1.2 Análisis de Uso de Modelos de IA Médica

Entrada mínima:

```text
prompt del estudiante
intención de uso de IA
salida del modelo
crítica del estudiante
incertidumbre declarada
privacidad
verificación con guías/fuentes
escalamiento humano
```

Evaluación:

- prompting clínico responsable;
- crítica de salidas IA;
- detección de omisiones peligrosas;
- privacidad y gobernanza;
- sobredependencia de IA;
- colaboración humano-IA;
- metacognición aumentada por IA.

### Fase 2. Plan Especializado de Enseñanza

El plan debe generarse desde:

```text
brechas core
brechas IA/Salud Digital
incertidumbre
riesgo integrado
ciclo formativo
historial de respuesta a intervenciones
```

Salida esperada:

```text
objetivo clínico
objetivo IA/Digital
estrategia OxTutor
estrategia tutor humano
actividad de práctica
criterio de éxito
plazo de seguimiento
criterio de reevaluación
```

### Fase 3. Adaptación de OxTutor IA y Tutor Humano

OxTutor debe:

- usar todo el historial de conversación;
- operar con máquina de estados;
- no retener siempre la respuesta final;
- alcanzar condición de cierre;
- escalar a tutor humano cuando corresponda.

Estados objetivo:

```text
elicitar representación
→ explorar mecanismo/diferencial
→ comprobar seguridad
→ pedir justificación
→ comprobar metacognición
→ debrief
→ transferencia
```

Tutor humano debe:

- revisar evidencia;
- validar inferencias de alto impacto;
- hacer override;
- orientar profesionalismo, seguridad y contexto institucional.

### Fase 4. Estrategias Discriminadas y Seguimiento

Las estrategias deben discriminarse por:

```text
ciclo formativo
tipo de brecha
riesgo educativo
dependencia de pistas
uso de IA
respuesta previa a intervención
```

### Fase 5. Nueva Evaluación Secuencial

La reevaluación debe usar un nuevo caso, idealmente isomórfico o de transferencia.

Debe detectar:

- cambio conceptual;
- cambio en representación del problema;
- cambio en priorización;
- cambio en crítica de IA;
- cambio metacognitivo;
- transferencia a caso nuevo;
- persistencia de sesgos.

## 6. Contraste con el Estado Actual

| Área | Estado actual | Estado objetivo | Brecha |
| --- | --- | --- | --- |
| Datos del estudiante | Seeds y objetos enviados por frontend | Backend como fuente de verdad por `student_id` | Alta |
| Casos | Un caso semilla de dolor torácico | Casos versionados en DB | Alta |
| Intentos | No persistencia longitudinal completa | `assessment_attempts` + sesiones + eventos | Alta |
| Mastery | Actualización determinística simple | Estimación derivada con incertidumbre | Alta |
| Tutor | Usa principalmente respuesta reciente | Usa historial + máquina de estados | Media-alta |
| IA/Salud Digital | Evaluador determinístico inicial | Evidencia persistente + rúbricas versionadas | Media-alta |
| Plan de enseñanza | Composición conceptual/frontend | Motor backend de plan de precisión | Alta |
| Reevaluación | Simulación de cambio | Transferencia observada en caso nuevo | Alta |
| Frontend | Flujo Lovable conectado | Wizard longitudinal con revelación controlada | Media |
| Gobernanza | Variables y CORS básicos | RBAC, consentimiento, auditoría, retención | Alta |

## 7. Modelo de Datos Objetivo

Entidades objetivo:

```text
organizations
users
roles
students
courses
enrollments
learning_sessions
case_versions
assessment_attempts
rubric_observations
evidence_events
mastery_estimates
interventions
intervention_exposures
transfer_assessments
teacher_reviews
consents
audit_events
```

### 7.1 Ledger de Evidencia

`evidence_events` debe ser inmutable.

Ejemplos de eventos:

```text
case_attempt_submitted
confidence_reported
rubric_observation_created
hint_used
tutor_question_answered
ai_prompt_submitted
ai_output_critiqued
intervention_exposed
teacher_override_created
transfer_case_completed
```

### 7.2 Estimaciones de Dominio

`mastery_estimates` debe ser una proyección derivada:

```text
student_id
competency_id
estimated_mastery
uncertainty
evidence_count
model_version
last_observed_at
explanation
```

## 8. Motor de Estimación Defendible

### Estado Inicial

Mantener reglas determinísticas como baseline auditable.

### Siguiente Paso

Implementar un modelo simple tipo Bayesian Knowledge Tracing o Elo educativo.

Requisitos:

- guardar incertidumbre;
- no sumar/restar mastery fijo por una sola respuesta;
- explicar cada actualización;
- calibrar con desempeño posterior;
- diferenciar predicción vs transferencia observada.

### Futuro

Incorporar IRT:

```text
dificultad del caso
discriminación del ítem/caso
probabilidad de acierto
capacidad latente
```

## 9. Arquitectura Agéntica Controlada

Crear un `Learning Orchestrator`.

Agentes o servicios coordinados:

```text
Assessor
Socratic Tutor
Curriculum Retriever
Case Simulator
Safety Critic
Intervention Planner
```

Regla:

```text
Ningún LLM único debe generar el caso, calificar, actualizar mastery y prescribir intervención sin controles independientes.
```

## 10. Banco Clínico

Antes de expandir dominios, profundizar dolor torácico.

Meta:

```text
20 a 30 casos versionados
```

Tipos:

- casos isomórficos;
- casos contrastantes;
- variaciones por edad, sexo, prevalencia y contexto;
- información incompleta;
- evolución temporal;
- errores o alucinaciones deliberadas de IA;
- comunicación, handoff y escalamiento;
- dificultad y discriminación revisadas por docentes.

Después:

```text
disnea aguda
dolor abdominal
```

## 11. Seguridad y Gobernanza

Requisitos:

- autenticación institucional;
- RBAC estudiante/docente/admin/investigador;
- aislamiento por institución;
- pseudonimización;
- consentimiento;
- finalidad, retención y eliminación;
- auditoría de acceso;
- detección de identificadores antes de llamar LLM;
- versionado de prompts, modelos, casos y rúbricas;
- registro de override docente;
- no usar historias clínicas reales sin proceso institucional formal.

## 12. Render Workflows

No usar Render Workflows para cada turno interactivo de OxTutor.

Mantener en FastAPI:

```text
sesiones interactivas
respuestas inmediatas
tutoría sincrónica
intentos de caso
```

Usar Workflows después para:

```text
generación masiva de casos
validación masiva de casos
embeddings
analítica de cohortes
recalibración de modelos
evaluaciones masivas
informes docentes
análisis de drift/sesgo
```

## 13. Evals Requeridas

Crear evaluaciones para:

- concordancia con docentes;
- validez de contenido;
- paráfrasis;
- negaciones;
- respuestas parciales;
- español regional;
- errores ortográficos;
- prompt injection;
- solicitud de respuesta final;
- fuga de identificadores;
- equidad por subgrupos;
- estabilidad psicométrica;
- invariantes de scoring;
- transferencia a caso nuevo;
- regresiones al cambiar modelo.

## 14. Primer Sprint Ejecutable

### Objetivo del Sprint

Corregir la validez mínima del MVP y crear la base persistente para intentos reales.

Duración sugerida:

```text
1 a 2 semanas
```

### 14.1 Backend

#### Tarea B1. Contratos por IDs

Crear nuevos request schemas para flujos productivos:

```text
student_id
case_version_id
session_id
student_response
confidence_before
confidence_after
elapsed_seconds
hints_used
```

No aceptar `StudentProfile` ni `ClinicalCase` completos desde frontend para endpoints productivos.

Endpoints nuevos o versión 2:

```text
POST /api/v1/sessions/start
POST /api/v1/attempts/core
POST /api/v1/attempts/ai-health
```

#### Tarea B2. Repositorios PostgreSQL

Crear repositorios para:

```text
students
case_versions
learning_sessions
assessment_attempts
evidence_events
```

El primer objetivo es persistir intentos, no aún reemplazar toda la lógica.

#### Tarea B3. Ledger de Evidencia

Crear tabla y modelo:

```text
evidence_events
```

Debe registrar:

```text
event_id
organization_id
student_id
session_id
event_type
payload
model_version
created_at
```

Regla:

```text
append-only
```

#### Tarea B4. Mastery con Incertidumbre

Crear tabla:

```text
mastery_estimates
```

Campos mínimos:

```text
student_id
competency_id
estimated_mastery
uncertainty
evidence_count
model_version
last_observed_at
explanation
```

En este sprint puede actualizarse con baseline determinístico, pero debe guardar incertidumbre y explicación.

#### Tarea B5. Alembic

Agregar migraciones versionadas.

Desactivar en producción:

```text
INIT_DB_ON_STARTUP=false
```

Mantener comando manual o job de migración:

```text
alembic upgrade head
```

### 14.2 Render

Configurar producción:

```env
INIT_DB_ON_STARTUP=false
```

Mantener:

```env
PYTHON_VERSION=3.11.11
DATABASE_URL=postgresql+psycopg://...
BACKEND_CORS_ORIGINS=https://edugemelodigital.lovable.app
BACKEND_CORS_ORIGIN_REGEX=https://.*\.lovable\.app
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

Nota:

```text
El regex de Lovable puede mantenerse durante previews autorizados.
Para producción institucional, restringir a dominios exactos.
```

### 14.3 Lovable

No modificar frontend local. Entregar prompt a Lovable.

Prompt recomendado:

```text
Ajusta el flujo productivo para que el navegador no envíe perfiles completos de mastery ni casos clínicos completos a endpoints productivos.

Cambios obligatorios:
1. Eliminar cualquier respuesta clínica prellenada, respuesta modelo o razonamiento esperado antes del intento.
2. Ocultar rúbricas, razonamiento esperado, solución, red flags internas y criterios de scoring hasta que el estudiante finalice el intento o hasta entrar como rol docente.
3. Solicitar confianza antes de responder y confianza después de responder.
4. Enviar al backend solamente:
   - student_id
   - case_version_id
   - session_id
   - student_response
   - confidence_before
   - confidence_after
   - elapsed_seconds
   - hints_used
5. Mantener fallback demo solo para modo demostración claramente indicado.
6. Todo texto visible debe estar en español.
7. No mostrar enums crudos del backend en inglés; traducirlos centralmente.

Flujo visual:
Alumno → Caso → Diagnóstico Core → Diagnóstico IA/Salud Digital → Plan → OxTutor + Tutor Humano → Seguimiento → Reevaluación.

El intento debe comenzar con caso limpio y revelación controlada. El estudiante no debe ver respuesta esperada, rúbrica ni feedback antes de enviar su respuesta.
```

### 14.4 Evals del Sprint

Agregar tests para:

- endpoint productivo rechaza `StudentProfile` completo si no corresponde;
- intento queda persistido;
- evidence_event se crea por intento;
- confidence_before y confidence_after son obligatorios;
- frontend no necesita enviar mastery;
- respuesta clínica prellenada no existe en mock productivo;
- salidas visibles siguen en español.

## 15. Criterios de Aceptación Iniciales

El sprint 1 se considera completo si:

- ninguna respuesta o razonamiento esperado se muestra antes del intento;
- cada intento queda persistido;
- cada intento puede reconstruirse desde `evidence_events`;
- el cliente no puede autodeclarar mastery;
- el gemelo diferencia predicción de evidencia observada;
- tutor y reevaluación pertenecen a la misma sesión longitudinal;
- toda inferencia muestra evidencia, incertidumbre y versión;
- los cambios de frontend se entregan como instrucciones listas para Lovable;
- todo texto visible permanece en español.

## 16. Secuencia de Ejecución Recomendada

```text
Fase 1:
Validez del MVP + contratos por IDs + persistencia de intentos.

Fase 2:
Ledger de evidencias + mastery con incertidumbre + dashboard temporal.

Fase 3:
Sesión integrada y máquina de estados del tutor.

Fase 4:
Orquestador agéntico con assessor, safety critic y human override.

Fase 5:
Banco clínico profundo y piloto institucional.

Fase 6:
Render Workflows para procesos offline y analítica de cohortes.
```

## 17. Decisión Técnica Inmediata

La próxima implementación debe evitar ampliar la complejidad visual o agéntica antes de resolver persistencia y validez.

Prioridad real:

```text
contratos por IDs
persistencia de intentos
ledger de evidencia
mastery con incertidumbre
front sin respuestas prellenadas
```

Esto convierte el MVP en el primer eslabón de un gemelo digital longitudinal defendible.

