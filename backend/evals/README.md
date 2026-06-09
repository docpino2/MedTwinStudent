# Entorno de pruebas de salidas

Este directorio contiene un entorno reproducible para verificar las salidas principales de MedTwin Student sin depender de un servidor web, base de datos o conexión externa.

## Qué valida

- El Socratic Tutor Agent responde en español.
- El Tutor no entrega la respuesta final inmediatamente.
- El Reasoning Engine devuelve análisis, brechas, sesgo y actividad recomendada.
- El Learning Simulation Engine actualiza dominio, calcula reducción de riesgo y recomienda una siguiente actividad.
- Las salidas visibles para usuario contienen señales lingüísticas en español.

## Ejecutar

Desde `backend/`:

```bash
python evals/verify_outputs.py
```

El comando imprime un resumen y escribe el reporte completo en:

```text
evals/output/latest_outputs.json
```

## Criterio de éxito

El campo `status` debe ser:

```json
"passed"
```

Si alguna validación falla, el script termina con código de salida `1` y lista los errores en `checks.failed`.

