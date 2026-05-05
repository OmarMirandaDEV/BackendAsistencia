import os
import sys

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8000))
        # Use uvicorn to run the FastAPI app defined in app/main.py
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
    except Exception as e:
        print(f"Error al iniciar la app: {e}", file=sys.stderr)
        sys.exit(1)
