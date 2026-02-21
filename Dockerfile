# Multi-stage build: frontend (Vite) + backend (FastAPI)

# 1‑bosqich: FRONTEND build
FROM node:18-alpine AS frontend-build
WORKDIR /frontend

# Faqat package fayllarni copy qilish (kesh uchun)
COPY frontend/package*.json ./
RUN npm install

# Qolgan frontend kodini copy qilib, build qilamiz
COPY frontend ./
RUN npm run build   # natija: /frontend/dist


# 2‑bosqich: BACKEND + statik frontend
FROM python:3.11-slim

# dlib va boshqa kutubxonalar uchun kerakli paketlar
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pymysql bcrypt==4.0.1 passlib[bcrypt]==1.7.4 uvicorn

# Backend kodini copy qilamiz
COPY backend ./

# Frontend buildni backend image ichiga ko'chiramiz
COPY --from=frontend-build /frontend/dist ./frontend_dist

# PYTHONPATH va FRONTEND_DIST ni sozlaymiz
ENV PYTHONPATH=/app:/app/app
ENV FRONTEND_DIST=/app/frontend_dist
ENV PORT=8000

# Railway portni ENV orqali uzatadi, shell form CMD env ni ko'radi
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
