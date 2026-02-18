FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# 1. Loyihani build qilish
RUN npm run build

# 2. Statik fayllarni ishga tushirish uchun 'serve'ni o'rnatish
RUN npm install -g serve

# 3. Railway bergan portda 'dist' papkasini ishga tushirish
CMD ["sh", "-c", "serve -s dist -l $PORT"]