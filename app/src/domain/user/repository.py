from sqlalchemy.orm import Session
from typing import Optional, List
from app.src.domain.user.model import User
from app.src.domain.user.schema import UserCreate, UserUpdate


class UserRepository:
    """
    User 데이터베이스 작업을 담당하는 Repository
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """사용자명으로 사용자 조회"""
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """모든 사용자 조회"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
        """새 사용자 생성"""
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """사용자 정보 업데이트"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        """사용자 삭제"""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True
