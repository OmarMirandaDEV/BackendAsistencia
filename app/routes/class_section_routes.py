from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.class_section import Section
from app.models.course import Course
from app.schemas.section_schema import SectionCreate
from app.utils.jwt import verify_token

router = APIRouter(prefix="/sections", tags=["Sections"])

@router.post("/")
def create_section(
    section: SectionCreate,
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(verify_token)
):
    teacher_id = teacher_data["id"]

    # 🔍 Verificar que el curso le pertenece al maestro
    course = db.query(Course).filter(
        Course.course_id == section.course_id,
        Course.teacher_id == teacher_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado o no autorizado")

    new_section = Section(
        section_name=section.section_name,
        course_id=section.course_id
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return {
        "message": "Sección creada correctamente",
        "section_id": new_section.section_id
    }

@router.get("/course/{course_id}")
def get_sections_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(verify_token)
):
    teacher_id = teacher_data["id"]

    # Validar que el curso sea del profesor
    course = db.query(Course).filter(
        Course.course_id == course_id,
        Course.teacher_id == teacher_id
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail="No autorizado")

    sections = db.query(Section).filter(
        Section.course_id == course_id
    ).all()

    return sections

@router.get("/")
def get_sections(
    db: Session = Depends(get_db),
    teacher_data: dict = Depends(verify_token)
):
    teacher_id = teacher_data["id"]

    sections = db.query(Section, Course).join(Course).filter(
        Course.teacher_id == teacher_id
    ).all()

    result = []
    for section, course in sections:
        result.append({
            "section_id": section.section_id,
            "section_name": section.section_name,
            "course_id": course.course_id,
            "course_name": course.course_name  # 🔥 AQUÍ ESTÁ LA MAGIA
        })

    return result