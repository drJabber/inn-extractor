import logging
import sys
from typing import List, cast

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

API_PREFIX_V1 = "/api/v1"

VERSION = "0.1.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
STORAGE_PATH: str=config("STORAGE_PATH", cast=str, default="/tmp") 

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=1)
HTTP_PROXY: str=config("HTTP_PROXY", cast=str, default=None) 
HTTPS_PROXY: str=config("HTTP_PROXY", cast=str, default=None) 

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="Secret")

PROJECT_NAME: str = config("PROJECT_NAME", default="Honor INN")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)


# openapi config
OPENAPI_JSON_URL: str = config("OPENAPI_JSON_URL", cast=str, default="/openapi.json")
OPENAPI_DOCS_PATH: str = config("OPENAPI_DOCS_PATH", cast=str, default="/docs")
OPENAPI_REDOC_PATH: str = config("OPENAPI_REDOC_PATH", cast=str, default="/redoc")

#taxru
TAXRU_SERVICE_URL: str = config("TAXRU_SERVICE_URL", cast=str, default="https://service.nalog.ru")
TAXRU_SERVICE_API: str = config("TAXRU_INN_API", cast=str, default="/inn-proc.do")
TAXRU_CAPTCHA_API: str = config("TAXRU_CAPTCH_API", cast=str, default="/static/captcha.html")
# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

