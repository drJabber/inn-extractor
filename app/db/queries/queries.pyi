"""Typings for queries generated by aiosql"""

from typing import Optional, List
# import datetime
from asyncpg import Connection, Record

class TaskQueriesMixin:
    async def get_task_by_id(
        self, conn: Connection, *, task_id: int
    ) -> Record: ...

    async def get_tasks_for_work(
        self, conn: Connection
    ) -> List[Record]: ...

    async def get_tasks_done_by_date(
        self, conn: Connection, *, dt: str
    ) -> List[Record]: ...

    async def get_all_tasks(
        self, conn: Connection
    ) -> Record: ...

    async def create_new_task(
        self, conn: Connection,
        *,
        dt: str,
        state: str,
        # file: bytes
    ) -> Record: ...
    
    async def update_task_state(
        self, conn: Connection,
        *,
        task_id: int,
        new_state: str,
    ) -> Record: ...
    
class PersonQueriesMixin:
    async def get_person_by_id(
        self, conn: Connection, *, person_id: int
    ) -> Record: ...

    async def get_people_by_task_id(
        self, conn: Connection, *, task_id: int
    ) -> Record: ...

    async def get_good_people_by_task_id(
        self, conn: Connection, *, task_id: int
    ) -> Record: ...

    async def get_person_for_work_by_task_id(
        self, conn: Connection, *, task_id: int
    ) -> Record: ...

    async def create_new_person(
        self, conn: Connection,
        *,
        family: str,
        name: str,
        patronimic_name: Optional[str],
        bdate: str,
        docser: str,
        docno: str,
        docdt: str,
        snils: str,
        inn: Optional[str] = '0',
        status: str,
        task_id: int,
    ) -> Record: ...
    
    async def update_person_inn_and_status(
        self, conn: Connection,
        *,
        person_id: int,
        new_inn: str,
        new_status: str,
    ) -> Record: ...

class TotalsQueriesMixin:
    async def get_people_totals(
        self, conn: Connection
    ) -> Record: ...

    async def get_people_totals_for_task(
        self, conn: Connection,
        *, 
        task_id: int
    ) -> Record: ...

class Queries(
    TaskQueriesMixin,
    PersonQueriesMixin,
    TotalsQueriesMixin,
): ...

queries: Queries
