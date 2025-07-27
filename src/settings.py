from functools import lru_cache
from typing import Optional, List, Literal
from dotenv import load_dotenv, find_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


env_file = find_dotenv('.env')
if env_file:
    load_dotenv(env_file)


class Settings(BaseSettings):

    # ===== Database Settings =====
    DATABASE_HOST: str = Field(description="Database host")
    DATABASE_PORT: int = Field(default=5432, ge=1, le=65535, description="Database port")
    DATABASE_NAME: str = Field(description="Database name")
    DATABASE_USER: str = Field(description="Database user")
    DATABASE_PASSWORD: str = Field(description="Database password")

    DATABASE_POOL_SIZE: int = Field(default=10, description="Database pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Database max overflow")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, description="Database pool timeout")
    DATABASE_POOL_RECYCLE: int = Field(default=3600, description="Database pool recycle")
    DATABASE_ECHO: bool = Field(default=False, description="SQLAlchemy echo")

    # ===== Security Settings =====
    SECRET_KEY: str = Field(min_length=32, description="Secret key for JWT")
    ALGORITHM: str = Field(default='HS256', description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiration")

    DOCS_USERNAME: str = Field(description="Documentation username")
    DOCS_PASSWORD: str = Field(description="Documentation password")

    # ===== Redis =====
    REDIS_HOST: str = Field(default='localhost', description="Redis host")
    REDIS_PORT: int = Field(default=6379, ge=1, le=65535, description="Redis port")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_DB: int = Field(default=0, ge=0, description="Redis database")

    # ===== File Storage =====
    UPLOAD_DIR: str = Field(default='uploads', description="Upload directory")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024, description="Max file size")

    S3_ENDPOINT: Optional[str] = Field(default=None, description="S3 endpoint")
    S3_ACCESS_KEY: Optional[str] = Field(default=None, description="S3 access key")
    S3_SECRET_KEY: Optional[str] = Field(default=None, description="S3 secret key")
    S3_BUCKET_NAME: Optional[str] = Field(default=None, description="S3 bucket name")
    S3_REGION: str = Field(default='us-east-1', description="S3 region")

    # ===== External APIs =====
    SMTP_HOST: Optional[str] = Field(default=None, description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USERNAME: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    SMTP_TLS: bool = Field(default=True, description="SMTP TLS")

    # ===== Logging =====
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(
        default='INFO', description="Logging level"
    )
    LOG_FORMAT: Literal['JSON', 'TEXT'] = Field(default='TEXT', description="Log format")

    # ===== CORS =====
    CORS_ORIGINS: str = Field(
        default='http://localhost:3000,http://localhost:8000',
        description="CORS allowed origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="CORS allow credentials")

    # ===== Rate Limiting =====
    RATE_LIMIT_REQUESTS: int = Field(default=60, description="Rate limit requests per minute")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")

    # ===== Pydantic Settings Config =====
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        use_enum_values=True,
        extra='ignore'
    )

    # ===== Computed Properties =====
    @property
    def DATABASE_URL(self) -> str:
        """Get database URL"""
        return (
            f'postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}'
            f'@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}'
        )

    @property
    def REDIS_URL(self) -> str:
        """Get Redis URL"""
        auth = f':{self.REDIS_PASSWORD}@' if self.REDIS_PASSWORD else ''
        return f'redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'

    @property
    def EXCLUDED_PATHS(self) -> List[str]:
        """Get paths excluded from middleware"""
        return ['/docs', '/redoc', '/openapi.json', '/ping', '/health']

    @property
    def CORS(self) -> List[str]:
        """Get CORS origins as list"""
        if self.CORS_ORIGINS is not None and self.CORS_ORIGINS.strip():
            return [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin.strip()]
        return ['http://localhost:3000', 'http://localhost:8000']



@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
