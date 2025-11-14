from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional, Dict, Any

from app.src.domain.lecture.model import Lecture
from app.src.domain.course.model import Course
from app.src.domain.professor.model import Professor
from app.src.domain.student.model import Student
from app.src.domain.enrollment.model import Enrollment
from app.src.domain.department.model import Department
from app.src.domain.lecture.schema import LectureCreate


class LectureRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_lecture(self, lecture_create: LectureCreate) -> Lecture:
        db_lecture = Lecture(
            semester=lecture_create.semester,
            lecture_time=lecture_create.lecture_time,
            lecture_room=lecture_create.lecture_room,
            capacity=lecture_create.capacity,
            course_code=lecture_create.course_code,
            professor_id=lecture_create.professor_id
        )
        self.db.add(db_lecture)
        self.db.commit()
        self.db.refresh(db_lecture)
        return db_lecture

    def get_lecture_by_id(self, lecture_id: int) -> Optional[Lecture]:
        return self.db.query(Lecture).options(
            joinedload(Lecture.course),
            joinedload(Lecture.professor)
        ).filter(Lecture.lecture_id == lecture_id).first()

    def get_lectures(
        self,
        semester: Optional[str] = None,
        course_code: Optional[str] = None,
        professor_id: Optional[str] = None
    ) -> List[Lecture]:
        query = self.db.query(Lecture).options(
            joinedload(Lecture.course),
            joinedload(Lecture.professor)
        )
        if semester:
            query = query.filter(Lecture.semester == semester)
        if course_code:
            query = query.filter(Lecture.course_code == course_code)
        if professor_id:
            query = query.filter(Lecture.professor_id == professor_id)
        return query.all()

    def get_students_by_lecture_id(self, lecture_id: int) -> List[Dict[str, Any]]:
        results = self.db.query(
            Student.student_id,
            Student.student_name,
            Department.dept_name.label("department_name"),
            Student.grade_year,
            Enrollment.grade.label("grade_received")
        ).join(
            Enrollment, Enrollment.student_id == Student.student_id
        ).join(
            Lecture, Enrollment.lecture_id == Lecture.lecture_id
        ).join(
            Department, Student.dept_code == Department.dept_code
        ).filter(
            Lecture.lecture_id == lecture_id
        ).all()

        # Convert Row objects to dictionaries
        return [row._asdict() for row in results]

    def update_enrollment_grade(self, student_id: str, lecture_id: int, new_grade: str) -> Optional[Enrollment]:
        enrollment = self.db.query(Enrollment).filter(
            and_(Enrollment.student_id == student_id, Enrollment.lecture_id == lecture_id)
        ).first()
        if enrollment:
            enrollment.grade = new_grade
            self.db.commit()
            self.db.refresh(enrollment)
        return enrollment

    def check_course_exists(self, course_code: str) -> bool:
        return self.db.query(Course).filter(Course.course_code == course_code).first() is not None

    def check_professor_exists(self, professor_id: str) -> bool:
        return self.db.query(Professor).filter(Professor.professor_id == professor_id).first() is not None

    def check_student_exists(self, student_id: str) -> bool:
        return self.db.query(Student).filter(Student.student_id == student_id).first() is not None

    def check_enrollment_exists(self, student_id: str, lecture_id: int) -> bool:
        return self.db.query(Enrollment).filter(
            and_(Enrollment.student_id == student_id, Enrollment.lecture_id == lecture_id)
        ).first() is not None
