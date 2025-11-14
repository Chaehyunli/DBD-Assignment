from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.src.db.base import Base


class Department(Base):
    __tablename__ = "department"

    dept_code = Column(String(10), primary_key=True, index=True)
    dept_name = Column(String(50), nullable=False)
    office_location = Column(String(100))
    office_phone_number = Column(String(15))

    # Relationships (assuming Professor and Student models will have dept_code)
    # professors = relationship("Professor", back_populates="department")
    # students = relationship("Student", back_populates="department")
