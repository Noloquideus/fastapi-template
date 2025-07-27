import traceback
import inspect
import sys
import json
from datetime import datetime
from typing import Callable, Optional, Dict, Any
from uuid import uuid4
from contextvars import ContextVar
from src.infrastructure.logger import LogFormat
from src.infrastructure.logger.log_levels import LogLevel


trace_id_var: ContextVar[str] = ContextVar('trace_id', default='N/A')


class Logger:
    """
    Synchronous custom logger with ContextVar support for trace_id.
    Supports JSON and text logging formats.
    Singleton pattern.
    """

    _instance = None
    __default_format = LogFormat.TEXT

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        log_format: LogFormat = __default_format,
        min_level: LogLevel = LogLevel.INFO,
        id_generator: Optional[Callable[[], str]] = lambda: str(uuid4()),
    ):
        self.log_format = log_format
        self.min_level = min_level
        self.id_generator = id_generator

    def set_format(self, log_format: LogFormat):
        """Set log format using LogFormat enum"""
        if not isinstance(log_format, LogFormat):
            raise ValueError('Log format must be an instance of LogFormat enum')

        self.log_format = log_format

    def set_min_level(self, level: LogLevel):
        self.min_level = level

    def new_trace_id(self) -> str:
        """Create and set new trace_id in context"""
        trace_id = self.id_generator()
        trace_id_var.set(trace_id)
        return trace_id

    def set_trace_id(self, trace_id: str):
        """Set existing trace_id in context"""
        trace_id_var.set(trace_id)

    def get_trace_id(self) -> str:
        return trace_id_var.get()

    def clear_trace_id(self):
        """Clear the trace_id in the context"""
        trace_id_var.set('N/A')

    def _prepare_log_data(self, level: LogLevel, message: str) -> Dict[str, Any]:
        frame = inspect.currentframe().f_back.f_back.f_back
        filename = frame.f_code.co_filename
        line_number = frame.f_lineno

        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level.name,
            'file': filename,
            'line': line_number,
            'trace_id': trace_id_var.get(),
            'message': message,
        }

        if level == LogLevel.EXCEPTION:
            log_data['exception'] = traceback.format_exc()

        return log_data

    def _log(self, level: LogLevel, message: str):
        if level >= self.min_level:
            log_data = self._prepare_log_data(level, message)

            if self.log_format == LogFormat.JSON:
                log_message = json.dumps(log_data, ensure_ascii=False)
            else:
                # Default text format
                log_message = (
                    f"{log_data['timestamp']} - {log_data['level']} - "
                    f"{log_data['trace_id']} - {log_data['file']}:{log_data['line']} - "
                    f"{log_data['message']}"
                )
                if 'exception' in log_data:
                    log_message += f"\nTraceback:\n{log_data['exception']}"

            self._write(log_message)

    def _write(self, message: str):
        sys.stdout.write(message + "\n")

    def debug(self, message: str):
        self._log(LogLevel.DEBUG, message)

    def info(self, message: str):
        self._log(LogLevel.INFO, message)

    def warning(self, message: str):
        self._log(LogLevel.WARNING, message)

    def error(self, message: str):
        self._log(LogLevel.ERROR, message)

    def critical(self, message: str):
        self._log(LogLevel.CRITICAL, message)

    def exception(self, message: str):
        self._log(LogLevel.EXCEPTION, message)
