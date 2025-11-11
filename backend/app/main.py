from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.src.core.config import settings
from app.src.domain.user.controller import router as user_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(user_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Welcome to DBD Assignment API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
