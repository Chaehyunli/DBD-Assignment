from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.src.domain.course.repository import CoursesRepository
from app.src.domain.professor.model import Professor


class CoursesService:
    """
    Courses 비즈니스 로직을 담당하는 Service
    """

    def __init__(self, db: Session):
        self.repository = CoursesRepository(db)

    def get_professors_by_course(self, course_code: str) -> List[Professor]:
        """
        특정 과목을 담당하는 모든 교수 조회
        - course_code가 존재하지 않으면 404 에러 발생
        """
        # 과목 존재 여부 확인
        course = self.repository.get_course_by_code(course_code)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with code '{course_code}' not found"
            )

        # 해당 과목을 담당하는 교수 조회
        professors = self.repository.get_professors_by_course_code(course_code)

        return professors
