from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.src.db.base import get_db
from app.src.domain.scholarship.service import ScholarshipService
from app.src.domain.scholarship.schema import ScholarshipCandidateResponse

router = APIRouter()


@router.get("/candidates", response_model=List[ScholarshipCandidateResponse])
async def get_scholarship_candidates(
    semester: str = Query(..., description="학기 (예: 2025-2)", max_length=6),
    gpa_threshold: float = Query(..., description="최소 GPA 기준 (예: 4.0)", ge=0.0, le=4.5),
    status: str = Query("재학", description="재학 상태", max_length=10),
    db: Session = Depends(get_db)
):
    """
    (UR012) 특정 학기의 평점 기준을 충족하는 재학생 명단을 조회합니다.

    - **semester**: 학기 (예: 2025-2) - 필수
    - **gpa_threshold**: 최소 GPA 기준 (예: 4.0) - 필수
    - **status**: 재학 상태 (기본값: "재학")
    - **Returns**: 조건을 만족하는 학생 목록 (GPA 높은 순)
    - **Error**: 400 - 필수 파라미터 누락 또는 잘못된 값
    """
    service = ScholarshipService(db)
    candidates = service.get_scholarship_candidates(
        semester=semester,
        gpa_threshold=gpa_threshold,
        status=status
    )
    return candidates
