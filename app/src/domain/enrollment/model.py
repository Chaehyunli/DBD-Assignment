from sqlalchemy import Column, String, CHAR, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.src.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollment"

    student_id = Column(CHAR(8), ForeignKey("student.student_id", ondelete="CASCADE"), primary_key=True)
    lecture_id = Column(Integer, ForeignKey("lecture.lecture_id", ondelete="CASCADE"), primary_key=True)
    grade = Column(String(2))

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    lecture = relationship("Lecture", back_populates="enrollments")
