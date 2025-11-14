from sqlalchemy import Column, String, CHAR, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.src.db.base import Base
from app.src.domain.department.model import Department


class Student(Base):
    __tablename__ = "student"

    student_id = Column(CHAR(8), primary_key=True, index=True)
    student_name = Column(String(20), nullable=False)
    grade_year = Column(Numeric(1, 0), nullable=False)
    enrollment_status = Column(String(10), nullable=False)
    overall_gpa = Column(Numeric(3, 2), nullable=False)
    dept_code = Column(String(10), ForeignKey("department.dept_code"))

    # Relationship to Enrollment (one-to-many)
    enrollments = relationship("Enrollment", back_populates="student")
    department = relationship("Department", backref="students")
