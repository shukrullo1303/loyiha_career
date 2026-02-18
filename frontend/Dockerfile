FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Loyihani production uchun tayyorlaymiz
RUN npm run build

# Statik fayllarni xizmat ko'rsatish uchun 'serve' paketini o'rnatamiz
RUN npm install -g serve

# Railway portni o'zi beradi
EXPOSE $PORT

# 'dist' papkasini Railway bergan portda ishga tushiramiz
CMD ["sh", "-c", "serve -s dist -l $PORT"]