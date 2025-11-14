from sqlalchemy.orm import Session
from typing import Optional, List, Tuple, Dict, Any
from app.src.domain.student.model import Student
from app.src.domain.enrollment.model import Enrollment
from app.src.domain.student_semester_gpa.model import StudentSemesterGPA
from app.src.domain.lecture.model import Lecture
from app.src.domain.course.model import Course
from app.src.domain.department.model import Department


class StudentRepository:
    """
    Student 데이터베이스 작업을 담당하는 Repository
    """

    def __init__(self, db: Session):
        self.db = db

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """학번으로 학생 조회"""
        return self.db.query(Student).filter(Student.student_id == student_id).first()

    def get_enrollment(self, student_id: str, lecture_id: int) -> Optional[Enrollment]:
        """수강 신청 정보 조회"""
        return (
            self.db.query(Enrollment)
            .filter(
                Enrollment.student_id == student_id,
                Enrollment.lecture_id == lecture_id
            )
            .first()
        )

    def update_enrollment_grade(self, student_id: str, lecture_id: int, grade: str) -> None:
        """수강 성적 업데이트"""
        enrollment = self.get_enrollment(student_id, lecture_id)
        if enrollment:
            enrollment.grade = grade
            self.db.flush()  # 변경사항 즉시 반영 (커밋 전)

    def get_semester_enrollments(
        self, student_id: str, semester: str
    ) -> List[Tuple[Enrollment, int]]:
        """
        특정 학기의 학생 수강 내역 조회 (학점과 함께)
        Returns: List[(Enrollment, credits)]
        """
        results = (
            self.db.query(Enrollment, Course.credits)
            .join(Lecture, Lecture.lecture_id == Enrollment.lecture_id)
            .join(Course, Course.course_code == Lecture.course_code)
            .filter(Enrollment.student_id == student_id)
            .filter(Lecture.semester == semester)
            .all()
        )
        return results

    def get_or_create_semester_gpa(
        self, student_id: str, semester: str
    ) -> StudentSemesterGPA:
        """학기 평점 레코드 조회 또는 생성"""
        semester_gpa = (
            self.db.query(StudentSemesterGPA)
            .filter(
                StudentSemesterGPA.student_id == student_id,
                StudentSemesterGPA.semester == semester
            )
            .first()
        )

        if not semester_gpa:
            semester_gpa = StudentSemesterGPA(
                student_id=student_id,
                semester=semester,
                semester_gpa=0.0,
                earned_credits=0
            )
            self.db.add(semester_gpa)
            self.db.flush()

        return semester_gpa

    def update_semester_gpa(
        self, student_id: str, semester: str, gpa: float, earned_credits: int
    ) -> None:
        """학기 평점 업데이트"""
        semester_gpa = self.get_or_create_semester_gpa(student_id, semester)
        semester_gpa.semester_gpa = gpa
        semester_gpa.earned_credits = earned_credits
        self.db.flush()

    def get_all_semester_gpas(self, student_id: str) -> List[StudentSemesterGPA]:
        """학생의 모든 학기 평점 조회"""
        return (
            self.db.query(StudentSemesterGPA)
            .filter(StudentSemesterGPA.student_id == student_id)
            .all()
        )

    def update_overall_gpa(self, student_id: str, overall_gpa: float) -> None:
        """전체 평점 업데이트"""
        student = self.get_student_by_id(student_id)
        if student:
            student.overall_gpa = overall_gpa
            self.db.flush()

    def get_lecture_semester(self, lecture_id: int) -> Optional[str]:
        """강의의 학기 정보 조회"""
        lecture = self.db.query(Lecture).filter(Lecture.lecture_id == lecture_id).first()
        return lecture.semester if lecture else None

    def get_student_with_department(self, student_id: str) -> Optional[Tuple[Student, str]]:
        """
        학생 정보와 학과명 조회
        Returns: (Student, department_name) or None
        """
        result = (
            self.db.query(Student, Department.dept_name)
            .join(Department, Department.dept_code == Student.dept_code)
            .filter(Student.student_id == student_id)
            .first()
        )
        return result

    def get_student_enrollments_with_courses(
        self, student_id: str
    ) -> List[Tuple[str, str, int, Optional[str]]]:
        """
        학생의 모든 수강 내역 조회 (학기, 과목명, 학점, 성적)
        Returns: List[(semester, course_name, credits, grade)]
        """
        results = (
            self.db.query(
                Lecture.semester,
                Course.course_name,
                Course.credits,
                Enrollment.grade
            )
            .join(Lecture, Lecture.lecture_id == Enrollment.lecture_id)
            .join(Course, Course.course_code == Lecture.course_code)
            .filter(Enrollment.student_id == student_id)
            .order_by(Lecture.semester, Course.course_name)
            .all()
        )
        return results
