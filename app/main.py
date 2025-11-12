from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.src.core.config import settings

# Jinja2 템플릿 설정
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

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
# 예시: app.include_router(router, prefix=f"{settings.API_V1_STR}/endpoint", tags=["tag"])


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    메인 페이지 - Jinja2 템플릿으로 HTML 반환
    """
    context = {
        "request": request,
        "data_from_backend": "백엔드에서 보낸 데이터입니다! 🚀"
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
