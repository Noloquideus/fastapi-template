from fastapi import Request
from fastapi.responses import JSONResponse
from src.application.domain.enums.status_code import StatusCode
from src.application.domain.exceptions import SealedClassError


async def sealed_class_error_handler(request: Request, exc: SealedClassError) -> JSONResponse:
    return JSONResponse(
        status_code=StatusCode.INTERNAL_SERVER_ERROR.value,
        content={'error': 'Error in data types', 'detail': str(exc)}
    )
