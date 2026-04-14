import numpy as np
from sqlalchemy.orm import Session
from app.models.face import Face
from app.models.student import Student

MATCH_THRESHOLD = 0.6


def recognize_face_with_score(db: Session, new_descriptor):
    faces = db.query(Face).all()

    best_match = None
    min_distance = float("inf")

    for face in faces:
        try:
            stored_descriptor = face.facial_descriptor

            if not stored_descriptor:
                continue

            distance = np.linalg.norm(
                np.array(stored_descriptor) - np.array(new_descriptor)
            )

            if distance < min_distance:
                min_distance = distance
                best_match = face

        except Exception as e:
            print(f"Error con face_id {face.face_id}: {e}")
            continue

    if best_match is None:
        return {
            "student": None,
            "distance": None,
            "threshold": MATCH_THRESHOLD,
        }

    if min_distance < MATCH_THRESHOLD:
        student = db.query(Student).filter(
            Student.student_id == best_match.student_id
        ).first()
        return {
            "student": student,
            "distance": float(min_distance),
            "threshold": MATCH_THRESHOLD,
        }

    return {
        "student": None,
        "distance": float(min_distance),
        "threshold": MATCH_THRESHOLD,
    }


def recognize_face(db: Session, new_descriptor):
    result = recognize_face_with_score(db, new_descriptor)
    return result["student"]