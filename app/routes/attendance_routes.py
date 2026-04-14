from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.dependencies.database import get_db
from app.services.face_recognition_service import recognize_face
from app.services.attendance_service import mark_attendance
from app.models.student import Student

router = APIRouter(prefix="/attendance", tags=["Attendance"])


class AttendanceMarkRequest(BaseModel):
    student_id: int


@router.post("/recognize")
def recognize_and_mark(data: dict, db: Session = Depends(get_db)):
    descriptor = data["descriptor"]

    # reconocer estudiante
    student = recognize_face(db, descriptor)

    if not student:
        return {"message": "No reconocido"}

    # marcar asistencia
    result = mark_attendance(db, student.student_id)

    return {
        "student": {
            "id": student.student_id,
            "name": f"{student.first_name} {student.last_name}"
        },
        "attendance": result
    }


@router.post("/mark")
def mark_by_student(data: AttendanceMarkRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.student_id == data.student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    result = mark_attendance(db, student.student_id)

    return {
        "student": {
            "id": student.student_id,
            "name": f"{student.first_name} {student.last_name}"
        },
        "attendance": result
    }