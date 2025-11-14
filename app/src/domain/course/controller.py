from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.src.db.base import get_db
from app.src.domain.course.service import CoursesService
from app.src.domain.professor.schema import ProfessorResponse

router = APIRouter()


@router.get("/{course_code}/professors", response_model=List[ProfessorResponse])
async def get_professors_by_course(
    course_code: str,
    db: Session = Depends(get_db)
):
    """
    (UR010) 특정 과목을 담당했던 (혹은 담당하는) 모든 교수의 목록을 조회합니다.

    - **course_code**: 과목 코드 (예: CS101)
    - **Returns**: 해당 과목을 담당하는 교수 목록
    - **Error**: 404 - course_code가 존재하지 않을 경우
    """
    service = CoursesService(db)
    professors = service.get_professors_by_course(course_code)
    return professors
