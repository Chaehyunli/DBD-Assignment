from pydantic import BaseModel
from typing import Optional


class ProfessorResponse(BaseModel):
    """
    Professor 응답 스키마
    """
    professor_id: str
    professor_name: str
    email: Optional[str] = None
    office_room: Optional[str] = None

    class Config:
        from_attributes = True
