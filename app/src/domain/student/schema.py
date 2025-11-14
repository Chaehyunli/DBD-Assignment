from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from app.src.core.grade_utils import is_valid_grade, VALID_GRADES


class GradeUpdateRequest(BaseModel):
    """
    성적 수정 요청 스키마
    """
    grade: str = Field(..., max_length=2, description="성적 (A+, A, B+, B, C+, C, D+, D, F)")

    @field_validator('grade')
    @classmethod
    def validate_grade(cls, v: str) -> str:
        if not is_valid_grade(v):
            raise ValueError(f"Invalid grade. Valid grades: {', '.join(VALID_GRADES)}")
        return v


class GradeUpdateResponse(BaseModel):
    """
    성적 수정 응답 스키마
    """
    student_id: str = Field(..., description="학번")
    lecture_id: int = Field(..., description="강의 ID")
    updated_grade: str = Field(..., description="수정된 성적")
    message: str = Field(..., description="성공 메시지")
    updated_semester_gpa: float = Field(..., description="재계산된 학기 평점")
    updated_overall_gpa: float = Field(..., description="재계산된 전체 평점")

    class Config:
        from_attributes = True


class CourseGrade(BaseModel):
    """
    과목별 성적 정보
    """
    course_name: str = Field(..., description="과목명")
    credits: int = Field(..., description="학점")
    grade: Optional[str] = Field(None, description="성적")

    class Config:
        from_attributes = True


class SemesterReport(BaseModel):
    """
    학기별 성적표
    """
    semester: str = Field(..., description="학기")
    semester_gpa: float = Field(..., description="학기 평점")
    earned_credits: int = Field(..., description="취득 학점")
    courses: List[CourseGrade] = Field(default_factory=list, description="수강 과목 목록")

    class Config:
        from_attributes = True


class StudentReport(BaseModel):
    """
    학생 전체 성적표
    """
    student_id: str = Field(..., description="학번")
    student_name: str = Field(..., description="학생 이름")
    department_name: str = Field(..., description="학과명")
    overall_gpa: float = Field(..., description="전체 평점")
    semesters: List[SemesterReport] = Field(default_factory=list, description="학기별 성적")

    class Config:
        from_attributes = True
