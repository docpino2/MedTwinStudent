# Learning Simulation Engine

El Learning Simulation Engine estima cómo cambia el gemelo digital de un estudiante después de una intervención educativa. El modelo inicial es intencionalmente simple, transparente y configurable para que docentes e investigadores puedan auditar sus supuestos.

## Entradas

- Perfil del estudiante.
- Mapa de competencias o conceptos.
- Puntajes basales de dominio.
- Desempeño en un caso clínico.
- Tipo de intervención.
- Calidad del feedback.
- Tiempo invertido.
- Nivel de dificultad.
- Pesos configurables del modelo.

## Salidas

- Puntajes de dominio actualizados.
- Reducción de riesgo predicha.
- Brechas remanentes.
- Próxima actividad recomendada.
- Resumen de trayectoria de aprendizaje.

## Modelo Matemático Inicial

Para cada concepto `c`, el motor calcula un score de impulso educativo:

```text
driver(c) =
  w_performance * case_performance(c)
  + w_intervention * intervention_effect
  + w_feedback * feedback_quality
  + w_time * time_factor
  + w_difficulty * difficulty_alignment
```

Luego estima el cambio de dominio:

```text
readiness(c) = 1 - baseline_mastery(c)

delta(c) =
  (driver(c) - 0.5)
  * max_positive_delta
  * (0.6 + readiness(c))
```

Si el desempeño del concepto es muy bajo, aplica una penalización pequeña:

```text
if case_performance(c) < 0.35:
  delta(c) -= (0.35 - case_performance(c)) * max_negative_delta
```

Finalmente:

```text
updated_mastery(c) = clamp(baseline_mastery(c) + delta(c), 0, 1)
```

## Parámetros Configurables

Valores por defecto:

```json
{
  "performance": 0.28,
  "intervention": 0.22,
  "feedback_quality": 0.2,
  "time_spent": 0.15,
  "difficulty_alignment": 0.15,
  "max_positive_delta": 0.18,
  "max_negative_delta": 0.08,
  "gap_threshold": 0.7
}
```

## Interpretación

- `performance`: cuánto pesa el desempeño observado en el caso.
- `intervention`: efecto promedio esperado del tipo de intervención.
- `feedback_quality`: claridad, especificidad y oportunidad del feedback.
- `time_spent`: aproximación normalizada con techo en 45 minutos.
- `difficulty_alignment`: mayor valor cuando el nivel de dificultad está bien calibrado al desempeño.
- `max_positive_delta`: límite de mejora por simulación.
- `max_negative_delta`: penalización máxima por desempeño muy bajo.
- `gap_threshold`: umbral bajo el cual un concepto sigue siendo brecha.

## Reducción de Riesgo Predicha

El MVP usa una estimación agregada:

```text
risk_reduction =
  mastery_gain * 0.55
  + safety_score * 0.25
  + feedback_quality * 0.2
```

Esta variable no representa riesgo clínico real del paciente. Representa reducción estimada de riesgo educativo: menor probabilidad de que el estudiante repita el mismo patrón de error en un caso comparable.

## Endpoint

```http
POST /api/v1/simulation/simulate
```

Ejemplo resumido:

```json
{
  "student": {},
  "competency_map": [],
  "baseline_mastery_scores": {
    "troponin_kinetics": 0.58
  },
  "clinical_case_performance": {
    "overall_score": 0.62,
    "concept_scores": {
      "troponin_kinetics": 0.4,
      "acs_risk_stratification": 0.68
    },
    "safety_score": 0.7,
    "reasoning_score": 0.65,
    "metacognition_score": 0.55
  },
  "intervention_type": "socratic_tutoring",
  "feedback_quality": 0.85,
  "time_spent_minutes": 25,
  "difficulty_level": 3
}
```

