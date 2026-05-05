# Proyecto-TI — Despliegue en Render (Docker)

Pasos rápidos para desplegar en Render usando Docker:

1. Completa `.env` localmente (puedes partir de `.env.example`).

2. Probar localmente con Docker:

```bash
docker build -t proyecto-ti .
docker run -e DATABASE_URL="postgresql://..." -e SUPABASE_URL="..." -e SUPABASE_KEY="..." -p 8000:8000 proyecto-ti
```

3. Deploy en Render:
- Crea un nuevo *Web Service* en https://render.com y conecta tu repositorio.
- Selecciona **Docker** como método de despliegue (o sube `render.yaml`).
- Agrega las variables de entorno `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_KEY` en la sección de *Environment* en Render.

Opciones de despliegue y dependencias:
- Si necesitas reconocimiento facial (usa `face-recognition` native), despliega con **Docker**. He incluido `requirements.docker.txt` y `Dockerfile` para eso.
- Si prefieres no usar dependencias nativas y desplegar directamente en Render sin Docker, el proyecto ahora puede arrancar sin la funcionalidad de reconocimiento facial. En ese caso la ruta relacionada devolverá 503 con un mensaje indicando que la funcionalidad no está disponible.

Para desplegar sin Docker en Render, selecciona Environment `Python` y usa `requirements.txt` (sin `face-recognition`). Para soporte completo de face-recognition, elige Docker y `requirements.docker.txt`.

Notas:
- El punto de entrada es `run.py` (lanza `uvicorn` leyendo `PORT`).
- Asegúrate de que `requirements.txt` esté en UTF-8 y contenga todas las dependencias. Si ves errores de instalación en Render, primero prueba instalar localmente.
