from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.services.face_recognition_service import recognize_face
from app.services.attendance_service import mark_attendance

router = APIRouter(prefix="/attendance", tags=["Attendance"])


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