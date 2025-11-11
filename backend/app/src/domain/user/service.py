from typing import Optional, List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.src.domain.user.repository import UserRepository
from app.src.domain.user.schema import UserCreate, UserUpdate, UserResponse
from app.src.domain.user.model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    User 비즈니스 로직을 담당하는 Service
    """

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_user(self, user_id: int) -> Optional[User]:
        """사용자 조회"""
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        return self.repository.get_by_email(email)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """사용자 목록 조회"""
        return self.repository.get_all(skip=skip, limit=limit)

    def create_user(self, user_create: UserCreate) -> User:
        """
        새 사용자 생성
        - 비밀번호 해싱
        - 중복 검사
        """
        # 이메일 중복 검사
        if self.repository.get_by_email(user_create.email):
            raise ValueError("Email already registered")

        # 사용자명 중복 검사
        if self.repository.get_by_username(user_create.username):
            raise ValueError("Username already taken")

        # 비밀번호 해싱
        hashed_password = self._hash_password(user_create.password)

        # 사용자 생성
        return self.repository.create(user_create, hashed_password)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """사용자 정보 업데이트"""
        # 비밀번호가 포함된 경우 해싱
        if user_update.password:
            user_update.password = self._hash_password(user_update.password)

        return self.repository.update(user_id, user_update)

    def delete_user(self, user_id: int) -> bool:
        """사용자 삭제"""
        return self.repository.delete(user_id)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return pwd_context.verify(plain_password, hashed_password)

    def _hash_password(self, password: str) -> str:
        """비밀번호 해싱"""
        return pwd_context.hash(password)
