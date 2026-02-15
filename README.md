# Digital Service Platform

"Digital Service" – хизмат кўрсатиш соҳасида яширин иқтисодиётни аниқлаш, олдини олиш ва қисқартиришга қаратилган сунъий интеллектга асосланган рақамли платформа.

## Лойиҳа тавсифи

Платформа камералар ва сунъий интеллект технологиялари орқали:
- Мижозлар оқимини автоматик аниқлаш ва ҳисоблаш
- Ишчи ходимларни фейс-идентификация орқали аниқлаш
- Реал хизмат кўрсатиш ҳажмини солиқ ҳисоботлари билан солиштириш
- Яширин иқтисодиёт, "конверт" иш ҳақи ва нақд пул айланмасини қисқартириш

## Технологиялар

### Backend
- **FastAPI** - Python веб-фреймворк
- **PostgreSQL** - База маълумотлари
- **SQLAlchemy** - ORM
- **TensorFlow/PyTorch** - AI моделлар
- **OpenCV** - Видео таҳлил
- **Face Recognition** - Фейс-идентификация
- **ONVIF** - Камера интеграцияси

### Frontend
- **React** - UI библиотека
- **TypeScript** - Типлаш
- **Material-UI** - UI компонентлар
- **Recharts** - Графиклар
- **React Query** - Маълумотларни бошқариш

### Mobile
- **React Native** - Мобил илова
- **Expo** - Мобил платформа
- **React Navigation** - Навигация

## Урнатиш

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env файлни яратиш
cp .env.example .env
# .env файлни тўлдириш

# Базани яратиш
alembic upgrade head

# Серверни ишга тушириш
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Mobile

```bash
cd mobile
npm install
npm start
```

## Структура

```
.
├── backend/              # Backend кодлари
│   ├── app/
│   │   ├── api/         # API эндпоинтлари
│   │   ├── core/        # Асосий конфигурация
│   │   ├── models/      # База моделлари
│   │   ├── schemas/     # Pydantic схемалари
│   │   ├── services/    # Бизнес логика
│   │   └── main.py      # Асосий файл
│   └── requirements.txt
├── frontend/            # Frontend кодлари
│   ├── src/
│   │   ├── components/  # React компонентлар
│   │   ├── pages/       # Саҳифалар
│   │   ├── store/       # State management
│   │   └── api/         # API клиент
│   └── package.json
├── mobile/              # Мобил илова
│   ├── src/
│   │   ├── screens/     # Экраналар
│   │   └── store/       # State management
│   └── package.json
└── README.md
```

## API Эндпоинтлар

### Аутентификация
- `POST /api/v1/auth/login` - Кириш
- `POST /api/v1/auth/register` - Рўйхатдан ўтиш
- `GET /api/v1/auth/me` - Жорий фойдаланувчи

### Локациялар
- `GET /api/v1/locations/` - Рўйхат
- `POST /api/v1/locations/` - Яратиш
- `GET /api/v1/locations/{id}` - Маълумотлар
- `PUT /api/v1/locations/{id}` - Янгилаш

### Ходимлар
- `GET /api/v1/employees/` - Рўйхат
- `POST /api/v1/employees/` - Яратиш
- `POST /api/v1/employees/{id}/face` - Юз қўшиш

### Аналитика
- `GET /api/v1/analytics/locations/{id}` - Аналитика
- `GET /api/v1/analytics/locations/{id}/risk` - Риск баҳоси
- `GET /api/v1/analytics/locations/{id}/predictions` - Прогнозлар

### Камералар
- `GET /api/v1/cameras/` - Рўйхат
- `GET /api/v1/cameras/{id}/status` - Статус
- `POST /api/v1/cameras/{id}/analyze` - Таҳлил

## AI Модуллари

### 1. Person Detection (Инсонларни аниқлаш)
- Computer Vision орқали инсонларни аниқлаш
- Tracking (кузатиш) ва re-identification

### 2. Face Recognition (Юзни таниш)
- Ходимларни автоматик таниш
- Норасмий ишчиларни аниқлаш

### 3. Behavioral Analytics (Хулқ-атвор таҳлили)
- Мижозлар қолиш вақти
- Навбат узунлиги
- Хизмат тезлиги

### 4. Predictive Analytics (Прогнозлаш)
- Келгуси мижозлар прогнози
- Солиқ тушуми прогнози

### 5. Risk Scoring (Риск баҳолаш)
- Яширин иқтисодиёт эҳтимолини баҳолаш
- Риск индекси (0-100)

## Хавфсизлик

- JWT токенлар орқали аутентификация
- AES-256 шифрлаш
- Фейс маълумотлари шифрланади
- HTTPS/TLS алоқа
- GDPR/ISO 27001 принциплари

## Интеграция

- Солиқ қўмитаси API
- ККТ (онлайн касса) API
- MyGov API

## Лицензия

Давлат лойиҳаси

## Алоқа

Давлат органи номи
# loyiha_career
