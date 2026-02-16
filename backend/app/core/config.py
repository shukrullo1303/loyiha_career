"""
Конфигурация файли
Барча настройкаларни бир жойда сақлайди
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Асосий настройкалар"""
    
    # Лойиҳа
    PROJECT_NAME: str = "Digital Service Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # База
    DATABASE_URL: str = "mysql+pymysql://root:Admin7700@localhost:3306/loyiha"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "7e9f8a2b5c1d4e3f6a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # AI Моделлар
    AI_MODEL_PATH: str = "./models"
    FACE_RECOGNITION_MODEL: str = "./models/face_recognition_model.h5"
    PERSON_DETECTION_MODEL: str = "./models/person_detection_model.onnx"
    BEHAVIORAL_MODEL: str = "./models/behavioral_model.pkl"
    PREDICTIVE_MODEL: str = "./models/predictive_model.pkl"
    RISK_SCORING_MODEL: str = "./models/risk_scoring_model.pkl"
    
    # Камера
    ONVIF_USERNAME: str = "admin"
    ONVIF_PASSWORD: str = "admin"
    CAMERA_TIMEOUT: int = 30
    MAX_CAMERAS_PER_LOCATION: int = 10
    
    # Файл сақлаш
    UPLOAD_DIR: str = "./uploads"
    VIDEO_STORAGE_DIR: str = "./storage/videos"
    FACE_STORAGE_DIR: str = "./storage/faces"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Ташқи API
    TAX_API_URL: str = "https://api.tax.uz"
    TAX_API_KEY: str = ""
    MYGOV_API_URL: str = "https://api.mygov.uz"
    MYGOV_API_KEY: str = ""
    KKT_API_URL: str = "https://api.kkt.uz"
    KKT_API_KEY: str = ""
    
    # Хавфсизлик
    ENCRYPTION_KEY: str = "mZ9vS3pX6rB2nQ5tW8yU1iO4aD7fG0hJkL3mN6bV9cC"
    # ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    ALLOWED_ORIGINS: List[str] = ["*"]  # Production'да махсус доменлар
    
    # Логирование
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # Видео таҳлил
    VIDEO_FPS: int = 30
    VIDEO_RESOLUTION: tuple = (1920, 1080)
    DETECTION_CONFIDENCE: float = 0.7
    FACE_RECOGNITION_CONFIDENCE: float = 0.8
    
    # Статистика
    STATISTICS_UPDATE_INTERVAL: int = 60  # секунд
    HEATMAP_GRID_SIZE: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Настройкаларни яратиш
settings = Settings()

# Директорияларни яратиш
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VIDEO_STORAGE_DIR, exist_ok=True)
os.makedirs(settings.FACE_STORAGE_DIR, exist_ok=True)
os.makedirs(settings.AI_MODEL_PATH, exist_ok=True)
os.makedirs(Path(settings.LOG_FILE).parent, exist_ok=True)
