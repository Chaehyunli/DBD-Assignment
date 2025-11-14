from sqlalchemy import Column, String, CHAR, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.src.db.base import Base


class StudentSemesterGPA(Base):
    """
    StudentSemesterGPA 모델 - 학기별 학생 성적
    """
    __tablename__ = "student_semester_gpa"

    student_id = Column(CHAR(8), ForeignKey("student.student_id", ondelete="CASCADE"), primary_key=True)
    semester = Column(String(6), primary_key=True, nullable=False)
    semester_gpa = Column(Numeric(3, 2), nullable=False)
    earned_credits = Column(Numeric(3, 0), nullable=False)

    # Relationships
    # student = relationship("Student", back_populates="semester_gpas")
