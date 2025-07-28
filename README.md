# FastAPI Template

Modern FastAPI application template with Clean Architecture, ready for production use.

## 🏗️ Architecture

The project follows **Clean Architecture** principles and is divided into three main layers:

```
src/
├── application/      # Business logic and use cases
│   ├── abstractions/ # Repository interfaces
│   ├── contracts/    # Service interfaces
│   ├── domain/       # Domain objects and exceptions
│   └── services/     # Services
├── infrastructure/   # External dependencies and technical details
│   ├── database/     # ORM models and DB context
│   ├── logger/       # Custom logger with trace_id
│   └── utils/        # Utilities (retry, decorators)
└── presentation/     # Web layer and API
    ├── handlers/     # Exception handlers
    ├── middleware/   # Middleware (timing, trace_id)
    ├── routing/      # API routers
    └── schemas/      # Pydantic schemas
```

## 🚀 Features

- **Clean Architecture** - clear separation of concerns
- **PostgreSQL** - primary database with SQLAlchemy ORM
- **Alembic** - database migration management
- **Docker** - containerization and deployment
- **Custom Logger** - trace_id support for request tracing
- **Middleware** - automatic trace_id addition and request timing
- **Exception Handling** - centralized domain exception handling
- **Settings** - configuration management via Pydantic Settings
- **API Documentation** - Basic Auth protected documentation
- **Production Ready** - Docker, logging, monitoring

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.116+
- **Database**: PostgreSQL + SQLAlchemy 2.0 + Asyncpg
- **Migration**: Alembic
- **Validation**: Pydantic 2.0
- **Server**: Granian ASGI server
- **Containerization**: Docker & Docker Compose
- **Code Quality**: Ruff, MyPy, Bandit
- **Python**: 3.12+

## 📋 Prerequisites

- Python 3.12+
- Poetry (for dependency management)
- Docker & Docker Compose (optional)
- PostgreSQL (if running without Docker)

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Noloquideus/fastapi-template
```

### 2. Environment variables setup

Required variables:
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

### 3. Run with Docker Compose (recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### 4. Local development

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 API Documentation

After starting the application, documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/ping

> **Note**: Documentation is protected with Basic Auth. Use `DOCS_USERNAME` and `DOCS_PASSWORD` from .env file.

## 🗄️ Database

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Migration history
alembic history
```

### Database Connection

```bash
# Connect to PostgreSQL in Docker
docker-compose exec postgres psql -U $DATABASE_USER -d $DATABASE_NAME
```

## 🔧 Settings

All settings are managed through environment variables in `.env` file. Main setting groups:

### Database
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`
- `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW`, `DATABASE_POOL_TIMEOUT`

### Security
- `SECRET_KEY` - JWT key (minimum 32 characters)
- `ALGORITHM` - JWT algorithm (default HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- `DOCS_USERNAME`, `DOCS_PASSWORD` - for documentation access

### Logging
- `LOG_LEVEL` - logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FORMAT` - log format (JSON or TEXT)

### CORS
- `CORS_ORIGINS` - allowed origins (comma-separated)
- `CORS_ALLOW_CREDENTIALS` - allow credentials

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test
poetry run pytest tests/test_example.py::test_function
```

## 📊 Code Quality

The project is configured to maintain high code quality:

```bash
# Linting and formatting
poetry run ruff check src/
poetry run ruff format src/

# Type checking
poetry run mypy src/

# Security checking
poetry run bandit -r src/
```

## 🚀 Deployment

### Production with Docker

```bash
# Build image
docker build -t fastapi-template:latest .

# Run container
docker run -p 8000:8000 --env-file .env fastapi-template:latest
```

### Environment Variables for Production

```env
# Change to production values
LOG_LEVEL=INFO
LOG_FORMAT=JSON
DATABASE_ECHO=false
CORS_ORIGINS=https://yourdomain.com
```

## 📝 Logging

The application uses a custom logger with support for:

- **Trace ID** - unique identifier for request tracking
- **Structured Logging** - JSON format for production
- **Context Variables** - automatic trace_id addition to logs
- **Timing Measurement** - automatic logging of request execution time

Usage example:
```python
from src.infrastructure.logger import logger

logger.info("User created successfully")
logger.error("Database connection failed")
```

## 🛡️ Middleware

### TraceIDMiddleware
Automatically adds a unique trace_id to each request for tracing.

### TimingMiddleware
Measures and logs the execution time of each request.

## 🎯 Exception Handling

Centralized handling of domain exceptions:

- `ImmutableAttributeError` - attempt to modify immutable attribute
- `IncomparableObjectError` - attempt to compare incomparable objects
- `SealedClassError` - attempt to inherit from sealed class

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Noloquideus** - [daniilmanukian@gmail.com](mailto:daniilmanukian@gmail.com)

---

⭐ Star this project if you found it helpful!
