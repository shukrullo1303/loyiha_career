FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Tizim drayverlari
RUN apt-get update && apt-get install -y \
    gcc libmariadb-dev-compat pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pymysql bcrypt==4.0.1 passlib[bcrypt]==1.7.4

COPY . .

# Importlar ishlashi uchun yo'l
# PYTHONPATH ni nuqta (.) qilib belgilash joriy papkani paket sifatida ko'rsatadi
ENV PYTHONPATH=/app

# CMD buyrug'ini modul ko'rinishida yozamiz
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]