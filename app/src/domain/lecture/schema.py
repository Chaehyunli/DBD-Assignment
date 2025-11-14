from pydantic import BaseModel, Field
from typing import Optional


class LectureBase(BaseModel):
    semester: str = Field(..., max_length=6)
    lecture_time: Optional[str] = Field(None, max_length=50)
    lecture_room: Optional[str] = Field(None, max_length=50)
    capacity: int = Field(..., ge=1, le=999)
    course_code: str = Field(..., max_length=10)
    professor_id: Optional[str] = Field(None, max_length=5)


class LectureCreate(LectureBase):
    pass


class LectureResponse(LectureBase):
    lecture_id: int

    class Config:
        from_attributes = True


class LectureStudentResponse(BaseModel):
    student_id: str = Field(..., max_length=8)
    student_name: str = Field(..., max_length=20)
    department_name: str # This will come from a join with Department table, need to handle in repository
    grade_year: int = Field(..., ge=1, le=4)
    grade_received: Optional[str] = Field(None, max_length=2)

    class Config:
        from_attributes = True
