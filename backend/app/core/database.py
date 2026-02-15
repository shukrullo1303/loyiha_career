"""
База маълумотлари конфигурацияси
PostgreSQL база билан ишлаш
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# База движок
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# Сессия фабрикаси
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс
Base = declarative_base()


def get_db():
    """База сессиясини олиш (dependency)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
