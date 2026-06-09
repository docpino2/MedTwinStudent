# Preparación para GitHub

Repositorio recomendado:

```text
medtwin-student
```

## Antes de publicar

- No subir archivos `.env` reales.
- Usar `backend/.env.example` y `frontend/.env.example` como plantillas.
- Mantener fuera de Git los caches, outputs de evaluación y dependencias instaladas.
- Conectar Render usando `render.yaml`.
- Conectar Vercel desde `frontend/`.

## Comandos para remoto

Después de crear el repositorio vacío en GitHub:

```bash
git remote add origin git@github.com:<usuario>/medtwin-student.git
git push -u origin main
```

Si prefieres HTTPS:

```bash
git remote add origin https://github.com/<usuario>/medtwin-student.git
git push -u origin main
```

