import datetime
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.class_session import ClassSession


def mark_attendance(db: Session, student_id: int):
    now = datetime.datetime.now()

    # Buscar sesión activa (por fecha actual)
    session = db.query(ClassSession).filter(
        ClassSession.session_date == now.date()
    ).first()

    if not session:
        return {"error": "No hay sesión activa hoy"}

    # Verificar si ya marcó asistencia
    existing = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.session_id == session.session_id
    ).first()

    if existing:
        return {"message": "Asistencia ya registrada"}

    # Registrar asistencia
    new_attendance = Attendance(
        student_id=student_id,
        session_id=session.session_id,
        check_in_time=now,
        status="Presente"
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return {
        "message": "Asistencia registrada",
        "student_id": student_id,
        "session_id": session.session_id
    }