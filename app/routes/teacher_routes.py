from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.teacher import Teacher
from app.dependencies.database import get_db
from app.utils.security import verify_password, hash_password
from app.utils.jwt import create_access_token
from app.schemas.teacher_schema import TeacherCreate, TeacherLogin

router = APIRouter(prefix="/teachers", tags=["Teachers"])


# REGISTER
@router.post("/register")
def register(data: TeacherCreate, db: Session = Depends(get_db)):

    # Verificar si ya existe
    existing = db.query(Teacher).filter(Teacher.email == data.email).first()
    if existing:
        return {"error": "El correo ya está registrado"}

    new_teacher = Teacher(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return {"message": "Profesor creado correctamente"}


# LOGIN
@router.post("/login")
def login(data: TeacherLogin, db: Session = Depends(get_db)):
    
    teacher = db.query(Teacher).filter(Teacher.email == data.email).first()

    if not teacher:
        return {"error": "Usuario no encontrado"}

    if not verify_password(data.password, teacher.password):
        return {"error": "Contraseña incorrecta"}

    token = create_access_token({
        "sub": teacher.email,
        "id": teacher.teacher_id
    })

    return {
        "message": f"Bienvenid@ al sistema {teacher.name}",
        "access_token": token,
        "token_type": "bearer"
    }