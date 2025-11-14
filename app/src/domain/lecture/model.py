from sqlalchemy import Column, String, Numeric, Integer, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.src.db.base import Base


class Lecture(Base):
    """
    Lecture 모델
    """
    __tablename__ = "lecture"

    lecture_id = Column(Integer, primary_key=True, autoincrement=True)
    semester = Column(String(6), nullable=False)
    lecture_time = Column(String(50))
    lecture_room = Column(String(50))
    capacity = Column(Numeric(3, 0), nullable=False)
    course_code = Column(String(10), ForeignKey("course.course_code"), nullable=False)
    professor_id = Column(CHAR(5), ForeignKey("professor.professor_id"))

    # Relationships
    course = relationship("Course", back_populates="lectures")
    professor = relationship("Professor", back_populates="lectures")
