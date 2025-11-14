from sqlalchemy import Column, String, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.src.db.base import Base
from app.src.domain.department.model import Department


class Professor(Base):
    __tablename__ = "professor"

    professor_id = Column(CHAR(5), primary_key=True, index=True)
    professor_name = Column(String(20), nullable=False)
    office_room = Column(String(50))
    email = Column(String(50), unique=True)
    dept_code = Column(String(10), ForeignKey("department.dept_code"))

    # Relationship to Lecture (one-to-many)
    lectures = relationship("Lecture", back_populates="professor")
    department = relationship("Department", backref="professors")
