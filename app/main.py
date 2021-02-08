from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import (ALLOWED_HOSTS, API_PREFIX_V1, DEBUG,
    PROJECT_NAME, VERSION, OPENAPI_DOCS_PATH, 
    OPENAPI_JSON_URL, OPENAPI_REDOC_PATH,
)

from app.core.events import create_start_app_handler, create_stop_app_handler

from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, 
          openapi_url=OPENAPI_JSON_URL, docs_url=OPENAPI_DOCS_PATH, redoc_url=OPENAPI_REDOC_PATH)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX_V1)

    application.mount(path='/static', app=StaticFiles(directory='app/static'), name='static')

    return application


templates = Jinja2Templates(directory="app/static/templates")

app = get_application()

@app.get("/", response_class=HTMLResponse, include_in_schema=False, name="index")
async def main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/load.html", response_class=HTMLResponse, include_in_schema=False, name="load")
async def main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("load.html", {"request": request})