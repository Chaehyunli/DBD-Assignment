from sqlalchemy import Column, String, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.src.db.base import Base

class Professor(Base):
    """
    Professor 모델
    """
    __tablename__ = "professor"

    professor_id = Column(CHAR(5), primary_key=True)

    professor_name = Column(String(20), nullable=False)
    office_room = Column(String(50))
    email = Column(String(50), unique=True)
    dept_code = Column(String(10), ForeignKey("department.dept_code"))

    # Relationship to Lecture (one-to-many)
    lectures = relationship("Lecture", back_populates="professor")
    # department = relationship("Department", backref="professors")
