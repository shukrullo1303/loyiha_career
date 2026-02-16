FROM python:3.11-slim

# dlib build qilish uchun kerakli paketlar
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pymysql bcrypt==4.0.1 passlib[bcrypt]==1.7.4

# 4. Kodlarni ko'chirish
COPY . .

# 5. MUHIM: Portni ochish (Shunda Docker Desktopda Port bo'limi chiqadi)
EXPOSE 8000

# 6. MUHIM: O'zgaruvchilarni Dockerfile ichida qotirib yozish (Localhost uchun)
ENV PYTHONPATH=/app
ENV PORT=8000
# Localhostdagi MySQL uchun (parolingizni root123 deb faraz qildim)
ENV DATABASE_URL=mysql+pymysql://root:Admin7700@host.docker.internal:3306/loyiha


# 7. Ishga tushirish
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# python -m uvicorn app.main:app --host 0.0.0.0 --port 8000