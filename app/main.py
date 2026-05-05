from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine, Base
from app.models import *
from app.routes import teacher_routes
from app.routes import course_routes
from app.routes import class_section_routes
from app.routes import class_session_routes
from app.routes import student_routes
from app.routes import face_routes
from app.routes import recognition_routes
from app.routes import attendance_routes
from app.routes import group_attendance_routes
from app.routes import report_routes
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Get allowed origins from env, default to localhost + common Render patterns
allowed_origins = os.environ.get("ALLOWED_ORIGINS", 
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
).split(",")

# Also allow all Render deployments (*.onrender.com)
origins = allowed_origins + [
    "https://*.onrender.com",
    "*"  # Allow all for now (can restrict later)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

app.include_router(teacher_routes.router)
app.include_router(course_routes.router)
app.include_router(class_section_routes.router)
app.include_router(class_session_routes.router)
app.include_router(student_routes.router)
app.include_router(face_routes.router)
app.include_router(recognition_routes.router)
app.include_router(attendance_routes.router)
app.include_router(group_attendance_routes.router)
app.include_router(report_routes.router)

# Flag para lazy init de tablas
_tables_created = False

def ensure_tables():
    """Crea las tablas la primera vez que se necesiten (lazy init)."""
    global _tables_created
    if not _tables_created:
        try:
            Base.metadata.create_all(bind=engine)
            _tables_created = True
        except Exception as e:
            print(f"Warning: Could not create tables at startup: {e}")

# Probar conexión
@app.get("/")
def test_connection():
    try:
        ensure_tables()  # Intenta crear tablas la primera vez
        conn = engine.connect()
        conn.close()
        return {"status": "ok", "message": "Conectado a la base de datos"}
    except Exception as e:
        return {"status": "error", "message": f"Error de conexión: {str(e)}"}