from fastapi import Request
from fastapi.responses import JSONResponse
from src.application.domain.enums.status_code import StatusCode
from src.application.domain.exceptions import IncomparableObjectError


async def incomparable_object_error_handler(request: Request, exc: IncomparableObjectError) -> JSONResponse:
    return JSONResponse(
        status_code=StatusCode.INTERNAL_SERVER_ERROR.value,
        content={'error': 'Error in data types', 'detail': str(exc)}
    )
