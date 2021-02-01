import datetime

from typing import Optional

from pydantic import BaseModel

from app.models.domain.people import PersonInDB
from app.models.schemas.rwschema import RWSchema

class PersonIn(RWSchema):
    id: int

class PersonInCreate(PersonIn):
    family: str
    name: str
    patronimic_name: Optional[str]
    bdate: str
    docser: str
    docno: str
    docdt: str
    snils: str
    inn: Optional[str]
    status: str
    task_id: int

class PersonInUpdate(RWSchema):
    inn: str
    status: str

class PersonInResponse(BaseModel):
    person: PersonInDB
