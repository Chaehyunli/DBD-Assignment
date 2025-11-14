from pydantic import BaseModel
from typing import Optional


class CourseResponse(BaseModel):
    """
    Course 응답 스키마
    """
    course_code: str
    course_name: str
    credits: int

    class Config:
        from_attributes = True
