from datetime import datetime
from typing import Optional

from pypika import Parameter as CommonParameter, Query, Table


class Parameter(CommonParameter):
    def __init__(self, count: int) -> None:
        super().__init__("${0}".format(count))


class TypedTable(Table):
    __table__ = ""

    def __init__(
        self,
        name: Optional[str] = None,
        schema: Optional[str] = None,
        alias: Optional[str] = None,
        query_cls: Optional[Query] = None,
    ) -> None:
        if name is None:
            if self.__table__:
                name = self.__table__
            else:
                name = self.__class__.__name__

        super().__init__(name, schema, alias, query_cls)


class Tasks(TypedTable):
    __table__ = "tasks"

    id: int
    dt: str
    state: str
    file: bytes

class People(TypedTable):
    __table__ = "people"

    id: int
    family: str
    name: str
    patronimic_name: str
    bdate: str
    docser: str
    docno: str
    docdt: str
    snis: str
    inn: str
    status: str


tasks = Tasks()
people = People()
