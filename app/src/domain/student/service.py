from typing import Tuple, Dict, List
from collections import defaultdict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.src.domain.student.repository import StudentRepository
from app.src.domain.student.schema import (
    GradeUpdateResponse,
    StudentReport,
    SemesterReport,
    CourseGrade
)
from app.src.core.grade_utils import grade_to_point


class StudentService:
    """
    Student 비즈니스 로직을 담당하는 Service
    """

    def __init__(self, db: Session):
        self.repository = StudentRepository(db)
        self.db = db

    def update_grade(
        self, student_id: str, lecture_id: int, grade: str
    ) -> GradeUpdateResponse:
        """
        학생 성적 수정 및 평점 연쇄 갱신

        1. enrollment의 grade 수정
        2. 해당 학기의 semester_gpa 재계산 및 업데이트
        3. 전체 overall_gpa 재계산 및 업데이트

        모든 작업은 트랜잭션 내에서 수행됩니다.
        """
        try:
            # 1. 학생 존재 확인
            student = self.repository.get_student_by_id(student_id)
            if not student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with id '{student_id}' not found"
                )

            # 2. 수강 신청 정보 확인
            enrollment = self.repository.get_enrollment(student_id, lecture_id)
            if not enrollment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Enrollment not found for student '{student_id}' and lecture '{lecture_id}'"
                )

            # 3. 강의의 학기 정보 조회
            semester = self.repository.get_lecture_semester(lecture_id)
            if not semester:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Lecture with id '{lecture_id}' not found"
                )

            # 4. 성적 업데이트
            self.repository.update_enrollment_grade(student_id, lecture_id, grade)

            # 5. 학기 평점 재계산 및 업데이트
            semester_gpa = self._recalculate_semester_gpa(student_id, semester)

            # 6. 전체 평점 재계산 및 업데이트
            overall_gpa = self._recalculate_overall_gpa(student_id)

            # 7. 커밋
            self.db.commit()

            # 8. 응답 생성
            return GradeUpdateResponse(
                student_id=student_id,
                lecture_id=lecture_id,
                updated_grade=grade,
                message="성적이 성공적으로 수정되었으며, 평점이 연쇄 갱신되었습니다.",
                updated_semester_gpa=round(semester_gpa, 2),
                updated_overall_gpa=round(overall_gpa, 2)
            )

        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update grade: {str(e)}"
            )

    def _recalculate_semester_gpa(self, student_id: str, semester: str) -> float:
        """
        학기 평점 재계산

        GPA = Σ(학점 × 평점) / Σ학점
        """
        enrollments = self.repository.get_semester_enrollments(student_id, semester)

        if not enrollments:
            return 0.0

        total_points = 0.0
        total_credits = 0

        for enrollment, credits in enrollments:
            if enrollment.grade:  # 성적이 있는 경우만 계산
                point = grade_to_point(enrollment.grade)
                total_points += point * float(credits)
                total_credits += int(credits)

        if total_credits == 0:
            semester_gpa = 0.0
        else:
            semester_gpa = total_points / total_credits

        # 학기 평점 업데이트
        self.repository.update_semester_gpa(
            student_id=student_id,
            semester=semester,
            gpa=semester_gpa,
            earned_credits=total_credits
        )

        return semester_gpa

    def _recalculate_overall_gpa(self, student_id: str) -> float:
        """
        전체 평점 재계산

        전체 GPA = Σ(학기 학점 × 학기 평점) / Σ학기 학점
        """
        semester_gpas = self.repository.get_all_semester_gpas(student_id)

        if not semester_gpas:
            return 0.0

        total_points = 0.0
        total_credits = 0

        for semester_gpa in semester_gpas:
            if semester_gpa.earned_credits > 0:
                total_points += float(semester_gpa.semester_gpa) * float(semester_gpa.earned_credits)
                total_credits += int(semester_gpa.earned_credits)

        if total_credits == 0:
            overall_gpa = 0.0
        else:
            overall_gpa = total_points / total_credits

        # 전체 평점 업데이트
        self.repository.update_overall_gpa(student_id, overall_gpa)

        return overall_gpa

    def get_student_report(self, student_id: str) -> StudentReport:
        """
        학생 전체 성적표 조회

        student, student_semester_gpa, enrollment, lecture, course, department 테이블을
        조인하여 학생의 전체 성적표를 반환합니다.
        """
        # 1. 학생 정보와 학과명 조회
        student_data = self.repository.get_student_with_department(student_id)
        if not student_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id '{student_id}' not found"
            )

        student, department_name = student_data

        # 2. 학생의 모든 학기 평점 조회
        semester_gpas = self.repository.get_all_semester_gpas(student_id)
        semester_gpa_dict = {
            sg.semester: (float(sg.semester_gpa), int(sg.earned_credits))
            for sg in semester_gpas
        }

        # 3. 학생의 모든 수강 내역 조회
        enrollments = self.repository.get_student_enrollments_with_courses(student_id)

        # 4. 학기별로 그룹화
        semester_courses: Dict[str, List[CourseGrade]] = defaultdict(list)
        for semester, course_name, credits, grade in enrollments:
            semester_courses[semester].append(
                CourseGrade(
                    course_name=course_name,
                    credits=int(credits),
                    grade=grade
                )
            )

        # 5. 학기별 성적표 생성
        semesters_list = []
        for semester in sorted(semester_courses.keys()):
            gpa, earned_credits = semester_gpa_dict.get(semester, (0.0, 0))
            semesters_list.append(
                SemesterReport(
                    semester=semester,
                    semester_gpa=round(gpa, 2),
                    earned_credits=earned_credits,
                    courses=semester_courses[semester]
                )
            )

        # 6. 전체 성적표 생성
        return StudentReport(
            student_id=student.student_id,
            student_name=student.student_name,
            department_name=department_name,
            overall_gpa=round(float(student.overall_gpa), 2),
            semesters=semesters_list
        )
