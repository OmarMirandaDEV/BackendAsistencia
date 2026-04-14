from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services.face_recognition_service import recognize_face_with_score

router = APIRouter(prefix="/recognition", tags=["Recognition"])


def _build_confidence(distance, threshold):
    if distance is None or not threshold:
        return 0.0

    ratio = 1 - (distance / threshold)
    bounded = max(0.0, min(1.0, ratio))
    return round(bounded * 100, 2)

@router.post("/")
def recognize(data: dict, db: Session = Depends(get_db)):
    descriptor = data["descriptor"]

    result = recognize_face_with_score(db, descriptor)
    student = result["student"]
    distance = result["distance"]
    threshold = result["threshold"]

    if student:
        return {
            "message": "Estudiante reconocido",
            "verified": True,
            "student_id": student.student_id,
            "name": f"{student.first_name} {student.last_name}",
            "distance": distance,
            "threshold": threshold,
            "confidence": _build_confidence(distance, threshold),
        }
    else:
        return {
            "message": "No reconocido",
            "verified": False,
            "distance": distance,
            "threshold": threshold,
            "confidence": _build_confidence(distance, threshold),
        }