from sqlalchemy.orm import Session
from typing import List, Optional
from app.src.domain.course.model import Course
from app.src.domain.professor.model import Professor
from app.src.domain.lecture.model import Lecture


class CoursesRepository:
    """
    Courses 데이터베이스 작업을 담당하는 Repository
    """

    def __init__(self, db: Session):
        self.db = db

    def get_course_by_code(self, course_code: str) -> Optional[Course]:
        """과목 코드로 과목 조회"""
        return self.db.query(Course).filter(Course.course_code == course_code).first()

    def get_professors_by_course_code(self, course_code: str) -> List[Professor]:
        """
        특정 과목을 담당하는 모든 교수 조회 (중복 제거)
        course -> lecture -> professor 테이블을 조인
        """
        professors = (
            self.db.query(Professor)
            .join(Lecture, Lecture.professor_id == Professor.professor_id)
            .join(Course, Course.course_code == Lecture.course_code)
            .filter(Course.course_code == course_code)
            .distinct()
            .all()
        )
        return professors
