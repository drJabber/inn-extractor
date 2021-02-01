from typing import Optional
from app.models.common import IDModelMixin
from app.models.domain.rwmodel import RWModel


class Person(RWModel):
    pass

class PersonInDB(IDModelMixin,Person):
    task_id: int
    bdate: str
    family: str
    name: str
    patronimic_name: Optional[str]
    docser: str
    docno: str
    docdt: str
    snils: str
    inn: Optional[str]
    status: str
