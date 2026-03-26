from fastapi import FastAPI
from app.config.database import engine, Base
from app.models import *
from app.routes import teacher_routes

app = FastAPI()

app.include_router(teacher_routes.router)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Probar conexión
@app.get("/")
def test_connection():
    try:
        conn = engine.connect()
        return {"message": "Conectado a la base de datos"}
    except:
        return {"message": "Error de conexión"}