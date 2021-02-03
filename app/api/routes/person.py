from fastapi.encoders import jsonable_encoder
from starlette.responses import Response
from app.models.domain.people import PersonInDB
from os import name, stat
from loguru import logger
from typing import List

from fastapi import APIRouter, Body

from app.resources import strings
from app.db.errors import EntityDoesNotExist

from app.db.repositories.people import PeopleRepository
from fastapi import APIRouter,  Depends, HTTPException, status
from app.api.dependencies.database import get_repository
from app.models.schemas.people  import (PersonIn,      
    PersonInResponse,
    PersonInUpdate,
)

from app.models.schemas.status import StatusInResponse

router = APIRouter()

@router.get("/{id}", response_model=PersonInResponse, name="person:get")
async def find_person(
    id: int,
    people_repo: PeopleRepository = Depends(get_repository(PeopleRepository))
) -> PersonInResponse:
    wrong_person_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_PERSON,
    )
    try:
        person = await people_repo.get_person_by_id(person_id=id)
    except EntityDoesNotExist as existence_error:
        raise wrong_person_error
    
    return PersonInResponse(
             person=PersonInDB(
                id = person.id_,
                family = person.family,
                name = person.name,
                patronimic_name=person.patronimic_name,
                bdate=person.bdate,
                docser=person.docser,
                docno=person.docno,
                docdt=person.docdt,
                snils=person.snils,
                inn=person.inn,
                task_id=person.task_id,
                status=person.status
             )
    )

@router.get("/todo/by_task_id/{task_id}", response_model=PersonInResponse, name="person:todo")
async def find_person_for_work_by_task_id(
    task_id: int,
    people_repo: PeopleRepository = Depends(get_repository(PeopleRepository))
) -> PersonInResponse:
    wrong_person_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_PERSON,
    )
    try:
        person = await people_repo.get_person_for_work_by_task_id(task_id=task_id)
    except EntityDoesNotExist as existence_error:
        return Response(
            content=jsonable_encoder(
                    StatusInResponse(
                        status="done", 
                        message=f"task {task_id} done or not found"
                    )
                ),
            status_code=200
        )
    
    return PersonInResponse(
             person=PersonInDB(
                id = person.id_,
                family = person.family,
                name = person.name,
                patronimic_name=person.patronimic_name,
                bdate=person.bdate,
                docser=person.docser,
                docno=person.docno,
                docdt=person.docdt,
                snils=person.snils,
                inn=person.inn,
                task_id=person.task_id,
                status=person.status
             )
    )


@router.put("/{person_id}", response_model=PersonInResponse, name="person:update")
async def update_person(
    person_id: int,
    person_in: PersonInUpdate=Body(..., embed='true', alias='person'),
    people_repo: PeopleRepository = Depends(get_repository(PeopleRepository))
) -> PersonInResponse:
    wrong_person_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_PERSON,
    )
    try:
        person = await people_repo.update_person_inn_and_state(person_id=person_id, inn=person_in.inn, status=person_in.status)
    except EntityDoesNotExist as existence_error:
        raise wrong_person_error
    
    return PersonInResponse(
             person=PersonInDB(
                id = person.id_,
                family = person.family,
                name = person.name,
                patronimic_name=person.patronimic_name,
                bdate=person.bdate,
                docser=person.docser,
                docno=person.docno,
                docdt=person.docdt,
                snils=person.snils,
                inn=person.inn,
                task_id=person.task_id,
                status=person.status
             )
    )

