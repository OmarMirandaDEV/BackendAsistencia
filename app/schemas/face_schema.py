from pydantic import BaseModel

class FaceCreate(BaseModel):
    facial_descriptor: str
    student_id: int