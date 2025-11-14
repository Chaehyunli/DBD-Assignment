from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from app.src.db.base import Base


class Course(Base):
    """
    Course 모델
    """
    __tablename__ = "course"

    course_code = Column(String(10), primary_key=True)
    course_name = Column(String(50), nullable=False, unique=True)
    credits = Column(Numeric(1, 0), nullable=False)

    # Relationships

    lectures = relationship("Lecture", back_populates="course")
