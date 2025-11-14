from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app.src.db.base import get_db
from app.src.domain.lecture.service import LectureService
from app.src.domain.lecture.schema import LectureCreate, LectureResponse, LectureStudentResponse
from app.src.core.config import settings

router = APIRouter(prefix=f"{settings.API_V1_STR}/lectures", tags=["Lectures"])

# Dependency to get LectureService
def get_lecture_service(db: Session = Depends(get_db)) -> LectureService:
    return LectureService(db)


@router.post("", response_model=LectureResponse, status_code=status.HTTP_201_CREATED)
async def create_lecture(
    lecture_create: LectureCreate,
    lecture_service: LectureService = Depends(get_lecture_service)
):
    """
    (UR005) 새로운 강의(Lecture)를 개설합니다.
    """
    return lecture_service.create_lecture(lecture_create)


@router.get("/{lecture_id}", response_model=LectureResponse)
async def get_lecture_by_id(
    lecture_id: int,
    lecture_service: LectureService = Depends(get_lecture_service)
):
    """
    (8) 고유한 lecture_id로 특정 강의 하나의 상세 정보를 조회합니다.
    """
    return lecture_service.get_lecture(lecture_id)


@router.get("", response_model=List[LectureResponse])
async def get_lectures(
    semester: Optional[str] = Query(None, description="특정 학기로 필터링 (예: 2025-2)"),
    course_code: Optional[str] = Query(None, description="특정 과목 코드로 필터링 (예: BUS101)"),
    professor_id: Optional[str] = Query(None, description="특정 교수 번호로 필터링 (예: P4001)"),
    lecture_service: LectureService = Depends(get_lecture_service)
):
    """
    (7, 9, 10 통합) 강의 목록을 조회합니다. 과목코드, 학기, 교수번호를 쿼리 파라미터로 제공하여 결과를 필터링할 수 있습니다.
    """
    return lecture_service.get_lectures(semester, course_code, professor_id)


@router.get("/{lecture_id}/students", response_model=List[LectureStudentResponse])
async def get_students_in_lecture(
    lecture_id: int,
    lecture_service: LectureService = Depends(get_lecture_service)
):
    """
    (UR009) 특정 강의(lecture)를 수강하는 모든 학생 명단을 조회합니다.
    """
    return lecture_service.get_students_in_lecture(lecture_id)
    