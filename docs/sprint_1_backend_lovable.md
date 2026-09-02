# Sprint 1: Validez del MVP y Persistencia Inicial

## Objetivo

Convertir el primer flujo productivo del gemelo digital en un flujo basado en IDs y evidencia persistente:

```text
student_id + case_version_id + session_id + respuesta + confianza
→ intento persistido
→ eventos de evidencia
→ estimación de mastery con incertidumbre
```

## Cambios Backend Implementados

### Nuevas Entidades

```text
learning_sessions
evidence_events
mastery_estimates
```

### `learning_sessions`

Representa una sesión longitudinal del gemelo digital.

Campos principales:

```text
id
student_id
case_version_id
status
current_phase
created_at
updated_at
```

### `evidence_events`

Ledger append-only de evidencia observada.

Eventos actuales:

```text
learning_session_started
core_attempt_submitted
confidence_reported
core_reasoning_observed
```

### `mastery_estimates`

Proyección derivada del estado del gemelo.

Campos principales:

```text
student_id
competency_id
estimated_mastery
uncertainty
evidence_count
model_version
explanation
last_observed_at
```

## Endpoints Productivos Nuevos

### Iniciar Sesión

```http
POST /api/v1/sessions/start
```

Request:

```json
{
  "student_id": "stu_clinical_001",
  "case_version_id": "case_chest_pain_001"
}
```

Response:

```json
{
  "session_id": "session_...",
  "student_id": "stu_clinical_001",
  "case_version_id": "case_chest_pain_001",
  "status": "iniciada",
  "current_phase": "diagnostico_integral"
}
```

### Enviar Intento Core

```http
POST /api/v1/sessions/attempts/core
```

Request:

```json
{
  "student_id": "stu_clinical_001",
  "case_version_id": "case_chest_pain_001",
  "session_id": "session_...",
  "student_response": "Considero síndrome coronario agudo...",
  "confidence_before": 0.45,
  "confidence_after": 0.68,
  "elapsed_seconds": 180,
  "hints_used": []
}
```

Response:

```json
{
  "attempt_id": "attempt_...",
  "session_id": "session_...",
  "reasoning": {},
  "mastery_estimates": [
    {
      "competency_id": "troponin_kinetics",
      "estimated_mastery": 0.52,
      "uncertainty": 0.25,
      "evidence_count": 1,
      "model_version": "deterministic-mastery-v1",
      "explanation": "Estado previo ... evidencia ... estado nuevo ..."
    }
  ],
  "evidence_event_ids": ["evidence_..."],
  "message": "Intento core persistido y estimaciones del gemelo actualizadas con incertidumbre."
}
```

## Prompt para Lovable

```text
Actualiza el flujo productivo de MedTwin Student para usar los endpoints persistentes por IDs.

Reglas obligatorias:
1. No enviar StudentProfile completo en el intento productivo.
2. No enviar ClinicalCase completo en el intento productivo.
3. No enviar mastery, rúbricas internas ni razonamiento esperado desde el navegador.
4. Antes del intento, solicitar confianza inicial del estudiante.
5. Después de escribir la respuesta, solicitar confianza posterior.
6. Registrar tiempo de respuesta y pistas usadas.
7. Todo texto visible debe permanecer en español.

Flujo:

1. Al seleccionar estudiante y caso, llamar:
POST /api/v1/sessions/start

Body:
{
  "student_id": selectedStudent.id,
  "case_version_id": selectedCase.id
}

Guardar session_id en el estado local de la sesión.

2. Al enviar el análisis core, llamar:
POST /api/v1/sessions/attempts/core

Body:
{
  "student_id": selectedStudent.id,
  "case_version_id": selectedCase.id,
  "session_id": sessionId,
  "student_response": studentResponse,
  "confidence_before": confidenceBefore,
  "confidence_after": confidenceAfter,
  "elapsed_seconds": elapsedSeconds,
  "hints_used": hintsUsed
}

3. Usar response.reasoning para mostrar Diagnóstico Core.
4. Usar response.mastery_estimates para mostrar estado del gemelo con incertidumbre.
5. Mostrar evidence_event_ids solo en vista docente o modo técnico.

Validaciones:
- No permitir iniciar intento sin session_id.
- No permitir enviar intento sin confidence_before y confidence_after.
- No mostrar respuesta esperada, rúbrica o solución antes del intento.
- Si el endpoint productivo falla, mostrar error en español y no autodeclarar mastery desde el cliente.

Mantener los endpoints antiguos solo como fallback demo, no como flujo productivo.
```

## Criterios de Aceptación

- El backend crea una sesión longitudinal.
- El intento core se envía por IDs.
- La respuesta queda persistida.
- Se crean eventos de evidencia.
- Se actualizan estimaciones con incertidumbre.
- El frontend no necesita enviar mastery ni caso autoritativo completo.
- Todo texto visible permanece en español.

