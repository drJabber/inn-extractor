from fastapi.encoders import jsonable_encoder
from starlette.responses import Response
from app.models.domain.people import PersonInDB
from os import name, stat
from loguru import logger
from typing import List

from fastapi import APIRouter, Body

from app.resources import strings
from app.db.errors import EntityDoesNotExist
from app.services.taxru import Taxru
from app.db.repositories.people import PeopleRepository
from app.db.repositories.tasks import TasksRepository
from app.db.repositories.totals import TotalsRepository
from fastapi import APIRouter,  Depends, HTTPException, status
from app.api.dependencies.database import get_repository
from app.models.schemas.people  import (PersonIn,      
    PersonInResponse,
    PersonInUpdate,
)
from app.models.schemas.status  import (InnInResponse,StatusInResponse, TotalsForTaskInResponse
)

from app.models.schemas.status import StatusInResponse

router = APIRouter()

taxru=Taxru()

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

@router.get("/todo/by_task_id/{task_id}",  name="person:todo")
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
        return StatusInResponse(
                        status="done", 
                        message=f"task {task_id} done or not found"
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


@router.put("/by_captcha/{captcha}/{token}",  name="person:captcha")
async def update_person_inn_by_token(
    captcha: str,
    token: str,
    people_repo: PeopleRepository = Depends(get_repository(PeopleRepository)),
    tasks_repo: TasksRepository = Depends(get_repository(TasksRepository)),
    totals_repo: TotalsRepository = Depends(get_repository(TotalsRepository))
) -> InnInResponse:
    wrong_person_error = HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=strings.WRONG_PERSON,
    )
    try:
        tasks = await tasks_repo.get_tasks_for_work()
        if tasks:
            task_id = tasks[0].id_
            person = await people_repo.get_person_for_work_by_task_id(task_id=task_id)
            inn_resp = taxru.get_inn(person, captcha, token) 
            if inn_resp.status.status != 'captcha':
                person.status=inn_resp.status.status
                if person.status == 'ok':
                    person.inn = inn_resp.inn
                people_repo.update_person_inn_and_state(person_id=person.id_, status=person.status, inn=person.inn)
            
            totals = totals_repo.get_totals()
            totals_for_task=totals_repo.get_totals_for_task(task_id)

            inn_resp.totals=totals
            inn_resp.totals_for_task=totals_for_task

            return inn_resp
        else:
            raise EntityDoesNotExist()    
    except EntityDoesNotExist as existence_error:
        return InnInResponse(
                        status=StatusInResponse(
                            status="done", 
                            message="все задания завершены"),
                        inn='0',    
                        totals=totals_repo.get_totals(),
                        totals_for_task=TotalsForTaskInResponse()
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

