Despliegue en Render (pasos rápidos)

1) Subir repo a GitHub
- Usa `scripts/push_repo.ps1` si tienes GH CLI, o crea el repo manualmente y haz push.

2) En Render
- New -> Web Service -> Connect GitHub -> selecciona tu repo.
- Environment: Docker
- Dockerfile path: `Dockerfile`
- Env Vars (agregar):
  - DATABASE_URL
  - SUPABASE_URL
  - SUPABASE_KEY
  - FACE_RECO_ENABLED (opcional, 1 para habilitar)
- Crear servicio y esperar deploy.

3) Logs
- Si el build falla, ve a la sección de Logs del servicio y copia el error.
- Si falla por compilación nativa, Render mostrará qué paquete falta; pega los logs en el issue y te ayudo a corregir.

Alternativa sin Docker:
- En Render selecciona Environment: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT`
- Nota: la funcionalidad de reconocimiento facial NO estará disponible (las rutas devolverán 503).
