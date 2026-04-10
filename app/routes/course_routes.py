from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course_schema import CourseCreate
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_teacher
from app.utils.jwt import verify_token 

router = APIRouter(prefix="/courses", tags=["Courses"])


# CREAR CURSO
@router.post("/")
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_teacher = Depends(get_current_teacher)
):
    new_course = Course(
        course_name=data.course_name,
        teacher_id=current_teacher["id"]
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return {
        "message": "Curso creado correctamente",
        "course": {
            "id": new_course.course_id,
            "name": new_course.course_name
        }
    }

@router.get("/")
def get_courses(db: Session = Depends(get_db), user=Depends(verify_token)):
    
    teacher_id = user["id"]

    courses = db.query(Course).filter(Course.teacher_id == teacher_id).all()

    return courses