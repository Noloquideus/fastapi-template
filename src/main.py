from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.application.domain.exceptions import ImmutableAttributeError, IncomparableObjectError, SealedClassError
from src.infrastructure.logger import logger
from src.presentation.handlers import immutable_attribute_error_handler, incomparable_object_error_handler, sealed_class_error_handler
from src.presentation.middleware.timing import TimingMiddleware
from src.presentation.middleware.trace_id import TraceIDMiddleware
from src.settings import settings


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    logger.info('API Started')
    yield
    logger.info('API Stopped')


app: FastAPI = FastAPI(
    redoc_url=None,
    docs_url=None,
    lifespan=lifespan,
    title='FastAPI Template',
    version='1.0.0',
    description='',
    license_info={
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT',
    }
)

# Initialize HTTP Basic authentication
security = HTTPBasic(description='Basic Authentication')

# Function to verify user credentials
async def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """
    Validates the user's credentials using a hashed password.
    """
    correct_username = settings.DOCS_USERNAME  # Username
    correct_password = settings.DOCS_PASSWORD  # Password hash

    if credentials.username != correct_username or not credentials.password == correct_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

app_router = APIRouter(prefix='/v1')
app.include_router(app_router)

# Added middleware
app.add_middleware(TraceIDMiddleware, logger=logger)
app.add_middleware(TimingMiddleware, logger=logger)

# Added exception handlers
app.add_exception_handler(ImmutableAttributeError, immutable_attribute_error_handler)
app.add_exception_handler(IncomparableObjectError, incomparable_object_error_handler)
app.add_exception_handler(SealedClassError, sealed_class_error_handler)


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html(_credentials: HTTPBasicCredentials = Depends(verify_credentials)) -> HTMLResponse:
    """
    Custom Swagger documentation, protected with basic authentication.
    """
    return get_swagger_ui_html(
        openapi_url=getattr(app, 'openapi_url', '/openapi.json'),
        title=getattr(app, 'title', 'FastAPI') + ' - Swagger UI',
        oauth2_redirect_url=getattr(app, 'swagger_ui_oauth2_redirect_url', None),
        swagger_js_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js',
        swagger_css_url='https://unpkg.com/swagger-ui-dist@5/swagger-ui.css',
    )

@app.get('/redoc', include_in_schema=False)
async def custom_redoc_html(_credentials: HTTPBasicCredentials = Depends(verify_credentials)) -> HTMLResponse:
    """
    Custom ReDoc documentation, protected with basic authentication.
    """
    return get_redoc_html(
        openapi_url=getattr(app, 'openapi_url', '/openapi.json'),
        title=getattr(app, 'title', 'FastAPI') + ' - ReDoc',
        redoc_js_url='https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js',
    )

@app.get('/ping')
async def ping() -> dict[str, str]:
    """
    Health check endpoint to verify API is running.
    """
    return {'message': 'pong', 'status': 'ok'}
