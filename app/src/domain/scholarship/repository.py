from sqlalchemy.orm import Session
from typing import List, Optional
from app.src.domain.student.model import Student
from app.src.domain.student_semester_gpa.model import StudentSemesterGPA
from app.src.domain.department.model import Department


class ScholarshipRepository:
    """
    Scholarship 데이터베이스 작업을 담당하는 Repository
    """

    def __init__(self, db: Session):
        self.db = db

    def get_scholarship_candidates(
        self,
        semester: str,
        gpa_threshold: float,
        status: str
    ) -> List[tuple]:
        """
        장학금 대상자 조회
        student_semester_gpa -> student -> department 테이블을 조인하여
        조건에 맞는 학생을 검색합니다.

        Returns:
            List[tuple]: (Student, Department.dept_name, StudentSemesterGPA.semester, StudentSemesterGPA.semester_gpa)
        """
        results = (
            self.db.query(
                Student,
                Department.dept_name,
                StudentSemesterGPA.semester,
                StudentSemesterGPA.semester_gpa
            )
            .join(StudentSemesterGPA, StudentSemesterGPA.student_id == Student.student_id)
            .join(Department, Department.dept_code == Student.dept_code)
            .filter(StudentSemesterGPA.semester == semester)
            .filter(StudentSemesterGPA.semester_gpa >= gpa_threshold)
            .filter(Student.enrollment_status == status)
            .order_by(StudentSemesterGPA.semester_gpa.desc())
            .all()
        )

        return results
