from pydantic import BaseModel, EmailStr

class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class TeacherLogin(BaseModel):
    email: EmailStr
    password: str