FROM node:18-alpine

WORKDIR /app

# Avval faqat package fayllarni ko'chiramiz (keshdan foydalanish uchun)
COPY package*.json ./
RUN npm install

# Qolgan barcha fayllarni ko'chiramiz
COPY . .

# Vite yoki React porti (odatda 5173 yoki 3000)
EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]