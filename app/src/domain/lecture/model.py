from sqlalchemy import Column, String, Integer, Numeric, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.src.db.base import Base
from app.src.domain.course.model import Course
from app.src.domain.professor.model import Professor
from app.src.domain.enrollment.model import Enrollment


class Lecture(Base):
    __tablename__ = "lecture"

    lecture_id = Column(Integer, primary_key=True, index=True)
    semester = Column(String(6), nullable=False)
    lecture_time = Column(String(50))
    lecture_room = Column(String(50))
    capacity = Column(Numeric(3, 0), nullable=False)
    course_code = Column(String(10), ForeignKey("course.course_code"), nullable=False)
    professor_id = Column(CHAR(5), ForeignKey("professor.professor_id"))

    # Relationships
    course = relationship("Course", back_populates="lectures")
    professor = relationship("Professor", back_populates="lectures")
    enrollments = relationship("Enrollment", back_populates="lecture")
