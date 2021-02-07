from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
# templates = Jinja2Templates(directory="app/static/templates")

# @router.get("/.*", response_class=HTMLResponse, include_in_schema=False, name="index")
# async def main(request: Request) -> HTMLResponse:
#     return templates.TemplateResponse("index.html", {"request": request})