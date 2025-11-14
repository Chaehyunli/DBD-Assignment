from pydantic import BaseModel, Field
from typing import Optional


class ScholarshipCandidateResponse(BaseModel):
    """
    장학금 대상자 응답 스키마
    """
    student_id: str = Field(..., max_length=8, description="학번")
    student_name: str = Field(..., max_length=20, description="학생 이름")
    department_name: str = Field(..., description="학과명")
    status: str = Field(..., max_length=10, description="재학 상태")
    semester: str = Field(..., max_length=6, description="학기")
    semester_gpa: float = Field(..., description="학기 평점")

    class Config:
        from_attributes = True
