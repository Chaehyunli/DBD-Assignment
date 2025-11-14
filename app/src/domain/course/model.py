from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from app.src.db.base import Base


class Course(Base):
    __tablename__ = "course"

    course_code = Column(String(10), primary_key=True, index=True)
    course_name = Column(String(50), nullable=False, unique=True)
    credits = Column(Numeric(1, 0), nullable=False)

    # Relationship to Lecture (one-to-many)
    lectures = relationship("Lecture", back_populates="course")
