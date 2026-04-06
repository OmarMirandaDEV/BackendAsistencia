from pydantic import BaseModel

class SectionCreate(BaseModel):
    section_name: str
    course_id: int