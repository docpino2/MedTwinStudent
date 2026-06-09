# Competencias IA/Salud Digital

MedTwin Student trata el uso de IA y salud digital como una familia explícita de competencias emergentes del estudiante de medicina. No se evalúa solo si el estudiante “usa IA”, sino cómo la usa: con razonamiento clínico, privacidad, verificación, metacognición, seguridad y responsabilidad profesional.

## Principio Pedagógico

La IA no debe funcionar como atajo cognitivo. Debe ser un instrumento para:

- Formular mejores preguntas clínicas.
- Ampliar y contrastar hipótesis.
- Detectar brechas y sesgos.
- Verificar información.
- Practicar razonamiento bajo incertidumbre.
- Aprender con agentes educativos.
- Mantener privacidad, seguridad y supervisión humana.

## Progresión por Ciclo

### Ciencias Básicas

Foco: comprensión conceptual, metacognición y aprendizaje autorregulado.

Competencias esperadas:

- Formular preguntas biomédicas claras para un modelo generativo.
- Pedir explicaciones mecanísticas sin aceptar respuestas de memoria.
- Declarar incertidumbre y nivel de confianza.
- Usar IA para detectar brechas conceptuales.
- Evitar estudiar pasivamente copiando respuestas del modelo.

Evidencias observables:

- Prompt con pregunta conceptual específica.
- Solicitud de analogías, mecanismos o preguntas de autoevaluación.
- Reflexión sobre qué no entiende.
- Crítica básica de una explicación generada.

Fallos comunes:

- Prompt vago.
- Copiar respuesta sin procesamiento.
- Sobreconfianza por fluidez del modelo.
- No verificar conceptos fundamentales.

### Ciencias Clínicas

Foco: razonamiento diferencial, verificación crítica y sesgos cognitivos.

Competencias esperadas:

- Pedir diferenciales priorizados y diagnósticos peligrosos.
- Solicitar rasgos discriminantes y datos que cambien probabilidad.
- Criticar salidas IA por omisiones, alucinaciones o falta de fuentes.
- Reconocer sesgos como anclaje, cierre prematuro y confirmación.
- Usar IA para comparar hipótesis, no para delegar juicio.

Evidencias observables:

- Prompt con contexto clínico, red flags e incertidumbre.
- Crítica escrita de la respuesta IA.
- Identificación de una omisión peligrosa.
- Reordenamiento del diferencial con justificación.

Fallos comunes:

- Pedir “diagnóstico final”.
- Aceptar salida IA sin contraste.
- No detectar que la IA omitió diagnósticos peligrosos.
- Confirmar hipótesis inicial con el modelo.

### Internado

Foco: seguridad, priorización, gobernanza, escalamiento y restricciones del sistema.

Competencias esperadas:

- Usar IA sin exponer datos identificables.
- Integrar IA con protocolos, supervisión y límites institucionales.
- Decidir qué debe hacerse primero bajo incertidumbre.
- Escalar a supervisor cuando hay riesgo clínico.
- Orquestar agentes educativos: tutor, simulador, evaluador y debrief.
- Documentar límites de la salida IA y responsabilidad humana.

Evidencias observables:

- Prompt anonimizado.
- Decisión de escalamiento explícita.
- Crítica de salida IA con foco en seguridad y disposición.
- Uso de agentes en flujo educativo verificable.

Fallos comunes:

- Incluir información identificable.
- Automatizar decisiones sin supervisión.
- Sobreconfiar en una salida generada.
- Ignorar restricciones del sistema.
- Usar IA fuera del marco institucional.

## Rúbrica 0 a 4

| Puntaje | Nivel | Descripción |
| --- | --- | --- |
| 0 | No observado | No usa IA o la usa de forma insegura, acrítica o con violación de privacidad. |
| 1 | Novato | Formula prompts vagos y acepta respuestas sin verificar. |
| 2 | En desarrollo | Incluye algo de contexto y reconoce algunos límites, pero omite seguridad, sesgos o verificación. |
| 3 | Competente | Usa IA con contexto, propósito, crítica, privacidad y razonamiento clínico seguro. |
| 4 | Adaptativo | Orquesta IA y agentes de forma crítica, segura, supervisada y metacognitiva bajo incertidumbre. |

## Endpoints

```http
GET /api/v1/ai-health/competencies
POST /api/v1/ai-health/evaluate
```

## Ejemplo de Evaluación

```json
{
  "student": {},
  "clinical_case": {},
  "intent": "differential_diagnosis",
  "student_ai_prompt": "Tengo un paciente de 58 años con dolor torácico con el esfuerzo, irradiación al brazo izquierdo y diaforesis. Sin datos identificables. Dame un diferencial priorizado, causas peligrosas, discriminadores y límites de tu respuesta.",
  "ai_model_output": "Podría ser SCA, reflujo o ansiedad...",
  "student_critique": "La salida es incompleta si no incluye disección aórtica o TEP según contexto. Debo verificar ECG, troponinas seriadas y guías. No reemplaza mi juicio clínico.",
  "declared_uncertainty": "No sé todavía si es SCA, pero hay alto riesgo.",
  "used_patient_identifiers": false,
  "cited_sources_or_guidelines": true,
  "escalated_to_human_supervisor": false
}
```

