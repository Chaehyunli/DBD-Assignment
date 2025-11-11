"""
데이터베이스 연결 테스트 스크립트
"""
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import text
from app.src.db.base import engine, SessionLocal
from app.src.core.config import settings


def test_database_connection():
    """데이터베이스 연결 테스트"""
    print("=" * 50)
    print("데이터베이스 연결 테스트")
    print("=" * 50)

    # 설정 정보 출력
    print("\n[데이터베이스 설정]")
    print(f"Host: {settings.POSTGRES_HOST}")
    print(f"Port: {settings.POSTGRES_PORT}")
    print(f"Database: {settings.POSTGRES_DB}")
    print(f"User: {settings.POSTGRES_USER}")
    print(f"Database URL: {settings.DATABASE_URL.replace(settings.POSTGRES_PASSWORD, '****')}")

    try:
        # 엔진으로 연결 테스트
        print("\n[연결 테스트 1: Engine]")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✓ 연결 성공!")
            print(f"PostgreSQL 버전: {version}")

        # 세션으로 연결 테스트
        print("\n[연결 테스트 2: Session]")
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT current_database(), current_user;"))
            db_name, user = result.fetchone()
            print(f"✓ 세션 연결 성공!")
            print(f"현재 데이터베이스: {db_name}")
            print(f"현재 사용자: {user}")

            # 테이블 목록 조회
            result = db.execute(text("""
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename;
            """))
            tables = result.fetchall()

            print(f"\n[테이블 목록]")
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (테이블이 없습니다)")

        finally:
            db.close()

        print("\n" + "=" * 50)
        print("✓ 모든 연결 테스트 통과!")
        print("=" * 50)
        return True

    except Exception as e:
        print("\n" + "=" * 50)
        print("✗ 연결 실패!")
        print("=" * 50)
        print(f"\n에러 타입: {type(e).__name__}")
        print(f"에러 메시지: {str(e)}")
        print("\n해결 방법:")
        print("1. PostgreSQL이 실행 중인지 확인하세요")
        print("2. .env 파일의 데이터베이스 설정을 확인하세요")
        print("3. 데이터베이스 사용자 권한을 확인하세요")
        return False


if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
