from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.db.repositories.tasks import TasksRepository
from app.api.dependencies.database import get_repository
from app.db.errors import EntityDoesNotExist
from app.resources import strings

router = APIRouter()
templates = Jinja2Templates(directory="app/static/templates")

@router.get("/", response_class=HTMLResponse, include_in_schema=False, name="index")
async def main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/load.html", response_class=HTMLResponse, include_in_schema=False, name="load")
async def load(request: Request,
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository))

) -> HTMLResponse:
    wrong_task_error = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=strings.WRONG_TASK,
    )
    try:
        tasks = await tasks_repo.get_tasks_for_work()
    except EntityDoesNotExist as existence_error:
        raise wrong_task_error
    
    return templates.TemplateResponse("load.html", {"request": request})

