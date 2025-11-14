from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.src.domain.lecture.repository import LectureRepository
from app.src.domain.lecture.schema import LectureCreate, LectureResponse, LectureStudentResponse
from app.src.domain.lecture.model import Lecture


class LectureService:
    def __init__(self, db: Session):
        self.repository = LectureRepository(db)

    def create_lecture(self, lecture_create: LectureCreate) -> Lecture:
        # Validate course_code and professor_id existence
        if not self.repository.check_course_exists(lecture_create.course_code):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with code {lecture_create.course_code} not found."
            )
        if lecture_create.professor_id and not self.repository.check_professor_exists(lecture_create.professor_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Professor with ID {lecture_create.professor_id} not found."
            )
        
        return self.repository.create_lecture(lecture_create)

    def get_lecture(self, lecture_id: int) -> Optional[Lecture]:
        lecture = self.repository.get_lecture_by_id(lecture_id)
        if not lecture:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lecture with ID {lecture_id} not found."
            )
        return lecture

    def get_lectures(
        self,
        semester: Optional[str] = None,
        course_code: Optional[str] = None,
        professor_id: Optional[str] = None
    ) -> List[Lecture]:
        # Validate existence of course_code or professor_id if provided
        if course_code and not self.repository.check_course_exists(course_code):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with code {course_code} not found."
            )
        if professor_id and not self.repository.check_professor_exists(professor_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Professor with ID {professor_id} not found."
            )

        return self.repository.get_lectures(semester, course_code, professor_id)

    def get_students_in_lecture(self, lecture_id: int) -> List[Dict[str, Any]]:
        if not self.repository.get_lecture_by_id(lecture_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lecture with ID {lecture_id} not found."
            )
        return self.repository.get_students_by_lecture_id(lecture_id)

    def update_student_grade(self, student_id: str, lecture_id: int, new_grade: str) -> Dict[str, Any]:
        if not self.repository.check_student_exists(student_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found."
            )
        if not self.repository.get_lecture_by_id(lecture_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lecture with ID {lecture_id} not found."
            )
        if not self.repository.check_enrollment_exists(student_id, lecture_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student {student_id} is not enrolled in lecture {lecture_id}."
            )
        
        updated_enrollment = self.repository.update_enrollment_grade(student_id, lecture_id, new_grade)
        if not updated_enrollment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update grade."
            )
        
        # In a real scenario, this would trigger GPA recalculation.
        # For now, we return a simplified response.
        return {
            "student_id": student_id,
            "lecture_id": lecture_id,
            "updated_grade": new_grade,
            "message": "성적이 성공적으로 수정되었습니다.",
            "updated_semester_gpa": "N/A", # Placeholder
            "updated_overall_gpa": "N/A" # Placeholder
        }
