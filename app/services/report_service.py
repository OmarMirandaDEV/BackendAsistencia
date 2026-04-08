from sqlalchemy.orm import Session
from sqlalchemy import func
import datetime

from app.models.student import Student
from app.models.attendance import Attendance
from app.models.class_session import ClassSession
from app.models.class_section import Section
from app.models.course import Course


# RESUMEN GENERAL
def get_dashboard_summary(db: Session, teacher_id: int):
    today = datetime.date.today()

    # total estudiantes del profesor
    total_students = db.query(Student).join(Section).join(Course).filter(
        Course.teacher_id == teacher_id
    ).count()

    # total asistencias hoy
    total_attendance = db.query(Attendance).join(ClassSession).join(Course).filter(
        ClassSession.session_date == today,
        Course.teacher_id == teacher_id
    ).count()

    percentage = 0
    if total_students > 0:
        percentage = (total_attendance / total_students) * 100

    return {
        "total_students": total_students,
        "attendance_today": total_attendance,
        "percentage": round(percentage, 2)
    }


# ASISTENCIA POR CURSO
def get_course_attendance(db: Session, course_id: int):
    today = datetime.date.today()

    session = db.query(ClassSession).filter(
        ClassSession.course_id == course_id,
        ClassSession.session_date == today
    ).first()

    if not session:
        return {"message": "No hay sesión hoy"}

    students = db.query(Student).join(Section).filter(
        Section.course_id == course_id
    ).all()

    attendance_records = db.query(Attendance).filter(
        Attendance.session_id == session.session_id
    ).all()

    attended_ids = {a.student_id for a in attendance_records}

    result = []

    for student in students:
        result.append({
            "student_id": student.student_id,
            "name": f"{student.first_name} {student.last_name}",
            "status": "Present" if student.student_id in attended_ids else "Absent"
        })

    return result


# HISTORIAL DE ESTUDIANTE
def get_student_history(db: Session, student_id: int):
    records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    result = []

    for r in records:
        result.append({
            "session_id": r.session_id,
            "date": r.check_in_time,
            "status": r.status
        })

    return result

# REPORTE POR RANGO DE FECHAS
def get_attendance_by_range(db: Session, teacher_id: int, start_date, end_date):
    records = db.query(Attendance).join(ClassSession).join(Course).filter(
        ClassSession.session_date >= start_date,
        ClassSession.session_date <= end_date,
        Course.teacher_id == teacher_id
    ).all()

    result = []

    for r in records:
        result.append({
            "student_id": r.student_id,
            "session_id": r.session_id,
            "date": r.check_in_time,
            "status": r.status
        })

    return result


# DIARIO
def get_daily_report(db: Session, teacher_id: int):
    today = datetime.date.today()
    return get_attendance_by_range(db, teacher_id, today, today)


# SEMANAL
def get_weekly_report(db: Session, teacher_id: int):
    today = datetime.date.today()
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)

    return get_attendance_by_range(db, teacher_id, start_week, end_week)


# MENSUAL
def get_monthly_report(db: Session, teacher_id: int):
    today = datetime.date.today()
    start_month = today.replace(day=1)

    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)

    end_month = next_month - datetime.timedelta(days=1)

    return get_attendance_by_range(db, teacher_id, start_month, end_month)


# SEMESTRAL
def get_semester_report(db: Session, teacher_id: int):
    today = datetime.date.today()
    start_semester = today - datetime.timedelta(days=180)

    return get_attendance_by_range(db, teacher_id, start_semester, today)