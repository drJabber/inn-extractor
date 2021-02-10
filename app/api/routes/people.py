from fastapi.param_functions import Header
from app.models.domain.people import PersonInDB
from os import name, stat
from loguru import logger
from typing import List, Optional

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter,  Depends, HTTPException, status
# from starlette.responses import StreamingResponse
from app.resources import strings
from app.db.errors import EntityDoesNotExist

from app.db.repositories.people import PeopleRepository
from app.api.dependencies.database import get_repository
from app.models.renderers import JSONRenderer, CSVFileRenderer, render
from app.models.schemas.people  import (PersonIn,      
    PersonInResponse,
    PersonInCreate,
    PersonInUpdate,
)

router = APIRouter()

@router.get(
      "/by_task_id/{task_id}", 
    #   response_model=List[PersonInResponse], 
      name="people:get(task_id)"
    )
async def get_by_task_id(
    task_id: int,
    accept: Optional[str]=Header(default=None),
    people_repo: PeopleRepository = Depends(get_repository(PeopleRepository))
) -> List[PersonInResponse]:
    wrong_person_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_PERSON,
    )
    try:
        people = await people_repo.get_people_by_task_id(task_id)
    except EntityDoesNotExist as existence_error:
        raise wrong_person_error
    
    return render(
               jsonable_encoder(people), 
               accept, 
               200, 
               None,
               [JSONRenderer, CSVFileRenderer])

@router.get(
      "/good/by_task_id/{task_id}", 
      name="people:good(task_id)"
    )
async def get_good_people_by_task_id(
    task_id: int,
    accept: Optional[str]=Header(default=None),
    people_repo: PeopleRepository = Depends(get_repository(PeopleRepository))
) -> List[PersonInResponse]:
    wrong_person_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_PERSON,
    )
    try:
        people = await people_repo.get_good_people_by_task_id(task_id)
    except EntityDoesNotExist as existence_error:
        raise wrong_person_error
    
    return render(
               people, 
               accept, 
               200, 
               None,
               [JSONRenderer, CSVFileRenderer])
