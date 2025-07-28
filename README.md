# FastAPI Template

Современный шаблон FastAPI приложения с Clean Architecture, готовый к production использованию.

## 🏗️ Архитектура

Проект следует принципам **Clean Architecture** и разделен на три основных слоя:

```
src/
├── application/      # Бизнес-логика и сценарии использования
│   ├── abstractions/ # Интерфейсы репозиториев
│   ├── contracts/    # Интерфейсы сервисов
│   ├── domain/       # Доменные объекты и исключения
│   └── services/     # Cервисы
├── infrastructure/   # Внешние зависимости и технические детали
│   ├── database/     # ORM модели и контекст БД
│   ├── logger/       # Кастомный логгер с trace_id
│   └── utils/        # Утилиты (retry, декораторы)
└── presentation/     # Веб-слой и API
    ├── handlers/     # Обработчики исключений
    ├── middleware/   # Middleware (timing, trace_id)
    ├── routing/      # Роутеры API
    └── schemas/      # Pydantic схемы
```

## 🚀 Особенности

- **Clean Architecture** - четкое разделение ответственности
- **PostgreSQL** - основная база данных с SQLAlchemy ORM
- **Alembic** - управление миграциями БД
- **Docker** - контейнеризация и развертывание
- **Кастомный логгер** - поддержка trace_id для трассировки запросов
- **Middleware** - автоматическое добавление trace_id и измерение времени запросов
- **Обработка исключений** - централизованная обработка доменных исключений
- **Настройки** - управление конфигурацией через Pydantic Settings
- **Документация API** - защищенная Basic Auth документация
- **Готовность к production** - Docker, logging, мониторинг

## 🛠️ Технологический стек

- **Framework**: FastAPI 0.116+
- **Database**: PostgreSQL + SQLAlchemy 2.0 + Asyncpg
- **Migration**: Alembic
- **Validation**: Pydantic 2.0
- **Server**: Granian ASGI server
- **Containerization**: Docker & Docker Compose
- **Code Quality**: Ruff, MyPy, Bandit
- **Python**: 3.12+

## 📋 Предварительные требования

- Python 3.12+
- Poetry (для управления зависимостями)
- Docker & Docker Compose (опционально)
- PostgreSQL (если запуск без Docker)

## ⚡ Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/Noloquideus/fastapi-template
```

### 2. Настройка переменных окружения

Обязательные переменные:
```env
# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password

# Security
SECRET_KEY=your-secret-key-min-32-chars
DOCS_USERNAME=admin
DOCS_PASSWORD=password

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=TEXT
```

### 3. Запуск с Docker Compose (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f api

# Остановка
docker-compose down
```

### 4. Локальная разработка

```bash
# Установка зависимостей
poetry install

# Активация виртуального окружения
poetry shell

# Запуск миграций
alembic upgrade head

# Запуск сервера разработки
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 API Документация

После запуска приложения документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/ping

> **Примечание**: Документация защищена Basic Auth. Используйте `DOCS_USERNAME` и `DOCS_PASSWORD` из .env файла.

## 🗄️ База данных

### Миграции

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Add new table"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# История миграций
alembic history
```

### Подключение к БД

```bash
# Подключение к PostgreSQL в Docker
docker-compose exec postgres psql -U $DATABASE_USER -d $DATABASE_NAME
```

## 🔧 Настройки

Все настройки управляются через переменные окружения в файле `.env`. Основные группы настроек:

### База данных
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`
- `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW`, `DATABASE_POOL_TIMEOUT`

### Безопасность
- `SECRET_KEY` - ключ для JWT (минимум 32 символа)
- `ALGORITHM` - алгоритм JWT (по умолчанию HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- `DOCS_USERNAME`, `DOCS_PASSWORD` - для доступа к документации

### Логирование
- `LOG_LEVEL` - уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FORMAT` - формат логов (JSON или TEXT)

### CORS
- `CORS_ORIGINS` - разрешенные источники (через запятую)
- `CORS_ALLOW_CREDENTIALS` - разрешить credentials

## 🧪 Тестирование

```bash
# Запуск всех тестов
poetry run pytest

# Запуск с покрытием
poetry run pytest --cov=src

# Запуск конкретного теста
poetry run pytest tests/test_example.py::test_function
```

## 📊 Качество кода

Проект настроен для поддержания высокого качества кода:

```bash
# Линтинг и форматирование
poetry run ruff check src/
poetry run ruff format src/

# Проверка типов
poetry run mypy src/

# Проверка безопасности
poetry run bandit -r src/
```

## 🚀 Развертывание

### Production с Docker

```bash
# Сборка образа
docker build -t fastapi-template:latest .

# Запуск контейнера
docker run -p 8000:8000 --env-file .env fastapi-template:latest
```

### Environment Variables для Production

```env
# Изменить на production значения
LOG_LEVEL=INFO
LOG_FORMAT=JSON
DATABASE_ECHO=false
CORS_ORIGINS=https://yourdomain.com
```

## 📝 Логирование

Приложение использует кастомный логгер с поддержкой:

- **Trace ID** - уникальный идентификатор для отслеживания запросов
- **Структурированное логирование** - JSON формат для production
- **Контекстные переменные** - автоматическое добавление trace_id в логи
- **Измерение времени** - автоматическое логирование времени выполнения запросов

Пример использования:
```python
from src.infrastructure.logger import logger

logger.info("User created successfully")
logger.error("Database connection failed")
```

## 🛡️ Middleware

### TraceIDMiddleware
Автоматически добавляет уникальный trace_id к каждому запросу для трассировки.

### TimingMiddleware
Измеряет и логирует время выполнения каждого запроса.

## 🎯 Обработка исключений

Централизованная обработка доменных исключений:

- `ImmutableAttributeError` - попытка изменения неизменяемого атрибута
- `IncomparableObjectError` - попытка сравнения несравнимых объектов
- `SealedClassError` - попытка наследования от sealed класса

## 🤝 Вклад в проект

1. Создайте форк проекта
2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)
3. Сделайте коммит изменений (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 👨‍💻 Автор

**Noloquideus** - [daniilmanukian@gmail.com](mailto:daniilmanukian@gmail.com)

---

⭐ Поставьте звезду, если проект был полезен!
