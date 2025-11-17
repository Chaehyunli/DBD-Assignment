from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.src.db.base import get_db
from app.src.domain.student.service import StudentService
from app.src.domain.student.schema import (
    GradeUpdateRequest,
    GradeUpdateResponse,
    StudentReport
)

router = APIRouter()


@router.patch(
    "/{student_id}/lectures/{lecture_id}/grade",
    response_model=GradeUpdateResponse
)
async def update_student_grade(
    student_id: str,
    lecture_id: int,
    grade_update: GradeUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    (UR008) 특정 학생의 수강 성적을 수정하고, 연관된 학기 평점 및 전체 평점을 갱신합니다.

    트랜잭션 내에서 다음 작업을 수행합니다:
    1. enrollment 테이블의 grade 수정
    2. student_semester_gpa 테이블의 학기 평점 재계산 및 업데이트
    3. student 테이블의 overall_gpa 재계산 및 업데이트

    - **student_id**: 학번 (예: S1000001)
    - **lecture_id**: 강의 ID (예: 1)
    - **grade**: 성적 (A+, A0, B+, B0, C+, C0, D+, D0, F)
    - **Returns**: 갱신된 성적 및 평점 정보
    - **Error**: 404 - 학생 또는 수강 내역이 존재하지 않음
    """
    service = StudentService(db)
    result = service.update_grade(
        student_id=student_id,
        lecture_id=lecture_id,
        grade=grade_update.grade
    )
    return result


@router.get("/{student_id}/report", response_model=StudentReport)
async def get_student_report(
    student_id: str,
    db: Session = Depends(get_db)
):
    """
    (UR007) 특정 학생의 전체 성적표를 학기별로 조회합니다.

    student, student_semester_gpa, enrollment, lecture, course, department 테이블을
    조인하여 학생의 전체 성적표를 반환합니다.

    - **student_id**: 학번 (예: S1000001)
    - **Returns**: 학생의 전체 성적표 (학기별 성적 포함)
    - **Error**: 404 - 학생이 존재하지 않음
    """
    service = StudentService(db)
    report = service.get_student_report(student_id)
    return report
