# DBD Assignment

데이터베이스 설계 프로젝트

## 기술 스택

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Python 3.10+

### Frontend
- React
- Vite

## 프로젝트 구조

```
DBD-Assignment/
├── backend/
│   ├── app/
│   │   ├── src/
│   │   │   ├── core/            # 설정 및 보안
│   │   │   ├── db/              # 데이터베이스 연결
│   │   │   └── domain/          # 도메인별 모듈
│   │   │       └── user/        # User 도메인 (예시)
│   │   │           ├── controller.py   # API 엔드포인트
│   │   │           ├── service.py      # 비즈니스 로직
│   │   │           ├── repository.py   # 데이터베이스 작업
│   │   │           ├── schema.py       # Pydantic 스키마
│   │   │           └── model.py        # SQLAlchemy 모델
│   │   └── main.py          # FastAPI 앱
│   ├── alembic/             # 데이터베이스 마이그레이션
│   ├── tests/               # 테스트
│   ├── .env                 # 환경 변수 (gitignore)
│   ├── requirements.txt     # Python 의존성
│   ├── setup_env.bat        # Windows용 환경 설정 스크립트
│   ├── test_db.bat          # Windows용 DB 연결 테스트
│   └── test_db_connection.py  # DB 연결 테스트 스크립트
└── frontend/                # React 프론트엔드
```

## 설치 및 실행

### 사전 요구사항

- Python 3.10 이상
- PostgreSQL (별도 레포지토리에서 관리)
- Node.js 18 이상 (Frontend)

### 1. 환경 변수 설정

**데이터베이스는 별도 레포지토리에서 관리됩니다.**

`backend/` 폴더에 `.env` 파일을 생성하고 데이터베이스 정보를 설정하세요:

```bash
cd backend
```

**중요**: 실제 데이터베이스 정보로 `.env` 파일을 생성하세요. 예시는 루트의 `.env.example` 파일을 참고하세요.

`.env` 파일 예시 (실제 값으로 변경 필요):
```env
# Database Configuration
DATABASE_URL=postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost:5432/YOUR_DB_NAME
POSTGRES_USER=YOUR_DB_USER
POSTGRES_PASSWORD=YOUR_DB_PASSWORD
POSTGRES_DB=YOUR_DB_NAME
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Backend Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Server
BACKEND_PORT=8000
```

**보안 주의사항**:
- `.env` 파일은 Git에 커밋하지 마세요 (이미 .gitignore에 포함됨)
- 프로덕션 환경에서는 반드시 강력한 SECRET_KEY 사용

### 2. Backend 설정 및 실행

#### 방법 1: Windows 배치 파일 사용

```cmd
cd backend

# 가상환경 생성 및 패키지 설치
setup_env.bat

# 가상환경 활성화
venv\Scripts\activate

# DB 연결 테스트
test_db.bat

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

#### 방법 2: 수동 설치 (Windows) (추천)

```cmd
cd backend

# 가상환경 생성 (py 런처 사용)
py -m venv venv

# 가상환경 활성화 (CMD)
venv\Scripts\activate.bat
# 또는 PowerShell
venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt

# DB 연결 테스트 (선택사항)
python test_db_connection.py

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

#### 방법 3: Mac/Linux

```bash
cd backend

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# DB 연결 테스트 (선택사항)
python test_db_connection.py

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

**접속 URL:**
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

### 3. Frontend 설정 및 실행

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

Frontend: http://localhost:5173

## 데이터베이스 연결 테스트

데이터베이스가 정상적으로 연결되는지 확인:

```bash
cd backend
python test_db_connection.py
```

성공 시 다음과 같은 메시지가 출력됩니다:
```
==================================================
✓ 모든 연결 테스트 통과!
==================================================
```

## 데이터베이스 마이그레이션

### 새로운 마이그레이션 생성
```bash
cd backend
alembic revision --autogenerate -m "마이그레이션 메시지"
```

### 마이그레이션 적용
```bash
alembic upgrade head
```

### 마이그레이션 롤백
```bash
alembic downgrade -1
```

### 현재 마이그레이션 상태 확인
```bash
alembic current
```

## 도메인 구조

이 프로젝트는 도메인 주도 설계(Domain-Driven Design)를 따릅니다. 각 도메인은 다음 계층으로 구성됩니다:

- **Controller**: API 엔드포인트 정의 (라우팅)
- **Service**: 비즈니스 로직 처리
- **Repository**: 데이터베이스 CRUD 작업
- **Schema**: 요청/응답 데이터 검증 (Pydantic)
- **Model**: 데이터베이스 테이블 정의 (SQLAlchemy)

새로운 도메인을 추가할 때는 `app/src/domain/` 하위에 도메인 이름으로 폴더를 만들고 위 파일들을 생성하세요.

## API 엔드포인트

### 기본
- `GET /` - 루트 엔드포인트
- `GET /health` - 헬스 체크

### Users (예시)
- `GET /api/v1/users` - 사용자 목록 조회
- `GET /api/v1/users/{user_id}` - 특정 사용자 조회
- `POST /api/v1/users` - 새 사용자 생성
- `PUT /api/v1/users/{user_id}` - 사용자 정보 수정
- `DELETE /api/v1/users/{user_id}` - 사용자 삭제

## 테스트

```bash
cd backend
pytest
```

## 트러블슈팅

### Windows PowerShell 실행 정책 오류

PowerShell에서 가상환경 활성화 시 오류가 발생하면:

```powershell
# 관리자 권한으로 실행
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

또는 CMD(명령 프롬프트)를 사용하세요:
```cmd
venv\Scripts\activate.bat
```

### Python 명령어가 작동하지 않는 경우

Windows Store Python 대신 [python.org](https://www.python.org/downloads/)에서 Python을 직접 설치하세요.
설치 시 **"Add Python to PATH"** 옵션을 체크하세요.

### email-validator 모듈 오류

```bash
pip install email-validator
```

### 데이터베이스 연결 오류

1. PostgreSQL 컨테이너가 실행 중인지 확인
2. `.env` 파일의 데이터베이스 정보 확인
3. 포트 5432가 사용 중인지 확인

```bash
# DB 연결 테스트
python test_db_connection.py
```

## 개발 도구

### 코드 포맷팅
```bash
black app/
```

### Linting
```bash
flake8 app/
```

### Type Checking
```bash
mypy app/
```

## 주요 파일 및 경로

- **Backend 설정**: `backend/.env`
- **Database 설정**: `backend/app/src/core/config.py`
- **Database 연결**: `backend/app/src/db/base.py`
- **도메인 모듈**: `backend/app/src/domain/`
- **마이그레이션**: `backend/alembic/versions/`

## 라이선스

MIT
