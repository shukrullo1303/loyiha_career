"""
Digital Service Platform - Main Application
Асосий FastAPI илова
"""
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import logging
from datetime import datetime
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.core.security import get_current_user
from app.api.v1 import api_router
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.security_middleware import SecurityMiddleware

# Логированиени сўнлаш
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Илова ишга тушганда ва тўхтаганда ишлайди"""
    # Ишга тушганда
    logger.info("Digital Service Platform ишга тушмоқда...")
    
    # Базани яратиш
    Base.metadata.create_all(bind=engine)
    logger.info("База яратилди")
    
    yield
    
    # Тўхтаганда
    logger.info("Digital Service Platform тўхтамоқда...")


app = FastAPI(
    title="Digital Service Platform",
    description="Яширин иқтисодиётни аниқлаш ва олдини олиш платформаси",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS мидлвар
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host мидлвар
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Production'да махсус хостлар
)

# Логирование мидлвар
app.add_middleware(LoggingMiddleware)

# Хавфсизлик мидлвар
app.add_middleware(SecurityMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобал хатоликларни қайта ишлаш"""
    logger.error(f"Хатолик: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Ички сервер хатолиги",
            "detail": str(exc) if settings.DEBUG else "Хатолик юз берди"
        }
    )


@app.get("/")
async def root():
    """Асосий эндпоинт"""
    return {
        "message": "Digital Service Platform API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check():
    """Сервер саломатлигини текшириш"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# API роутерларини улаш
app.include_router(api_router, prefix="/api/v1")


# Frontend build (Vite) ni serve qilish
FRONTEND_DIST = os.getenv("FRONTEND_DIST", "frontend_dist")

# Vite build ichidagi assets katalogini statik qilib ulaymiz
if os.path.isdir(os.path.join(FRONTEND_DIST, "assets")):
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")),
        name="assets",
    )


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Frontend SPA uchun index.html ni qaytarish"""
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    # Agar build topilmasa, eski root javobini бериш
    return {
        "message": "Digital Service Platform API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
