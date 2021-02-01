from loguru import logger

from typing import List
from fastapi import APIRouter, Form, File, Body, UploadFile, Depends, HTTPException, status
from app.resources import strings
from app.db.errors import EntityDoesNotExist

from app.resources import strings
from app.api.dependencies.database import get_repository

from app.db.repositories.tasks import TasksRepository
from app.db.repositories.people import PeopleRepository

from app.models.domain.tasks  import Task

from app.models.schemas.tasks  import (TaskIn,      
    TaskInResponse,
    TaskInCreate,
    TaskInUpdate,
)

from app.services.utils import process_csv_file, store_tmp_file

router = APIRouter()

@router.get("/by_id/{task_id}", response_model=TaskInResponse, name="task:get")
async def find_task(
    task_id: int,
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> TaskInResponse:
    wrong_task_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_TASK,
    )
    try:
        task = await tasks_repo.get_task_by_id(task_id=task_id)
    except EntityDoesNotExist as existence_error:
        raise wrong_task_error
    
    return TaskInResponse(task=
             Task(
                    id_=task.id_, 
                    dt=task.dt,
                    state=task.state
                )
            )

@router.get("/todo", response_model=List[TaskInResponse], name="task:todo")
async def find_task_for_work(
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> List[TaskInResponse]:
    wrong_task_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_TASK,
    )
    try:
        tasks = await tasks_repo.get_tasks_for_work()
    except EntityDoesNotExist as existence_error:
        raise wrong_task_error
    
    return tasks

@router.get("/done/{dt}", response_model=List[TaskInResponse], name="task:done[dt]")
async def find_task_for_work(
    dt: str,
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> List[TaskInResponse]:
    wrong_task_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_TASK,
    )
    try:
        tasks = await tasks_repo.get_tasks_done_by_date(dt)
    except EntityDoesNotExist as existence_error:
        raise wrong_task_error
    
    return tasks


@router.post("/", response_model=TaskInResponse, name="task:create")
async def create(
    dt: str = Form(...),
    state: str = Form(...),
    file: UploadFile = File(...),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
    people_repo: PeopleRepository = Depends(get_repository(PeopleRepository)),
) -> TaskInResponse:
    task = await tasks_repo.create_new_task(state=state, dt=dt)

    fpath = await store_tmp_file(file)
    people = await process_csv_file(fpath, task.id,people_repo)
        
    logger.info(f'file uploaded: {file.filename}')


    return TaskInResponse(task=
             Task(
                    id=task.id, 
                    dt=task.dt,
                    state=task.state
                )
            )

@router.put("/{task_id}", response_model=TaskInResponse, name="task:update")
async def update(
    task_id: int,
    task_in: TaskInUpdate=Body(..., embed='true', alias='task'),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository))
) -> TaskInResponse:
    wrong_task_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_TASK,
    )
    try:
        task = await tasks_repo.update_task_state(task_id=task_id, state=task_in.state)
    except EntityDoesNotExist as existence_error:
        raise wrong_task_error
    
    return TaskInResponse(task=
             Task(
                    id=task_id, 
                    dt=task.dt,
                    state=task.state
                )
            )
