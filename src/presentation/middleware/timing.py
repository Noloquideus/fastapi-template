import time
from typing import Callable, Awaitable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.applications import Starlette
from fastapi import Request, Response
from src.infrastructure.logger import Logger


class TimingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Starlette, logger: Logger) -> None:
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start_time) * 1000  # milliseconds

        self.logger.debug(
            f'{request.method} {request.url.path} '
            f'=> {response.status_code} of {duration:.2f} мс'
        )
        return response
