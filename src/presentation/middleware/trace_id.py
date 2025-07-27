import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.infrastructure.logger import Logger
from src.settings import settings


class TraceIDMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger: Logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):

        if request.url.path in settings.EXCLUDED_PATHS:
            return await call_next(request)

        x_trace_id = request.headers.get('X-Trace-ID', None)

        if not x_trace_id:
            x_trace_id = str(uuid.uuid4())

        self.logger.set_trace_id(x_trace_id)

        self.logger.info(f'Request started: {request.method} {request.url} - TraceID: {x_trace_id}')

        response = await call_next(request)

        self.logger.info(f'Request finished: {request.method} {request.url} - TraceID: {x_trace_id} - Status: {response.status_code}')

        return response
