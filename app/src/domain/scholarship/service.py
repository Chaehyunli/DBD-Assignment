from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.src.domain.scholarship.repository import ScholarshipRepository
from app.src.domain.scholarship.schema import ScholarshipCandidateResponse


class ScholarshipService:
    """
    Scholarship 비즈니스 로직을 담당하는 Service
    """

    def __init__(self, db: Session):
        self.repository = ScholarshipRepository(db)

    def get_scholarship_candidates(
        self,
        semester: str,
        gpa_threshold: float,
        status: str = "재학"
    ) -> List[ScholarshipCandidateResponse]:
        """
        장학금 대상자 조회
        - semester와 gpa_threshold는 필수
        - status는 기본값 "재학"
        """
        # 파라미터 검증
        if not semester:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="semester parameter is required"
            )

        if gpa_threshold is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="gpa_threshold parameter is required"
            )

        # GPA 범위 검증
        if gpa_threshold < 0.0 or gpa_threshold > 4.5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="gpa_threshold must be between 0.0 and 4.5"
            )

        # 재학 상태 검증
        valid_statuses = ["재학", "휴학", "졸업"]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"status must be one of: {', '.join(valid_statuses)}"
            )

        # 데이터 조회
        results = self.repository.get_scholarship_candidates(
            semester=semester,
            gpa_threshold=gpa_threshold,
            status=status
        )

        # 응답 스키마로 변환
        candidates = []
        for student, dept_name, semester, semester_gpa in results:
            candidates.append(
                ScholarshipCandidateResponse(
                    student_id=student.student_id,
                    student_name=student.student_name,
                    department_name=dept_name,
                    status=student.enrollment_status,
                    semester=semester,
                    semester_gpa=float(semester_gpa)
                )
            )

        return candidates
