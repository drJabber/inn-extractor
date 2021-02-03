from typing import Optional
from app.models.common import IDModelMixin
from app.models.domain.rwmodel import RWModel


class Person(RWModel):
    pass

class PersonInDB(IDModelMixin,Person):
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
