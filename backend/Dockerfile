FROM python:3.11-slim

# dlib va boshqa kutubxonalar uchun kerakli paketlar
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Konteyner ichida asosiy papka
WORKDIR /app

# Kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pymysql bcrypt==4.0.1 passlib[bcrypt]==1.7.4 uvicorn

# 3. KODNI KO'CHIRISH
# Railway-da Root Directory /backend bo'lsa, bu backend ichidagilarni /app ga tashlaydi
COPY . .

# 4. PYTHONPATH ni to'g'irlash
# Konteyner ichida hamma narsani /app va uning ichidagi app papkasidan qidirishga majburlaymiz
ENV PYTHONPATH=/app:/app/app

# 5. PORT (Railway o'zi port beradi, shuning uchun o'zgaruvchi ishlatamiz)
ENV PORT=8080

# 6. Ishga tushirish (main:app emas, app.main:app bo'lishi kerak, chunki papka nomi app)
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}

