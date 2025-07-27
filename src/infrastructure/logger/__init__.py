from src.infrastructure.logger.log_format import LogFormat
from src.infrastructure.logger.log_levels import LogLevel
from src.infrastructure.logger.logger import Logger
from src.settings import settings


log_levels = {
    'DEBUG': LogLevel.DEBUG,
    'INFO': LogLevel.INFO,
    'WARNING': LogLevel.WARNING,
    'ERROR': LogLevel.ERROR,
    'CRITICAL': LogLevel.CRITICAL,
    'EXCEPTION': LogLevel.EXCEPTION,
}

log_formats = {
    'JSON': LogFormat.JSON,
    'TEXT': LogFormat.TEXT,
}

logger = Logger(min_level=log_levels.get(settings.LOG_LEVEL, LogLevel.INFO), log_format=log_formats.get(settings.LOG_FORMAT, LogFormat.JSON))


async def get_logger() -> Logger:
    return logger
