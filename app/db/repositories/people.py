from typing import Optional, List, Any
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.people import Person, PersonInDB
from app.models.schemas.people import PersonInResponse


class PeopleRepository(BaseRepository):
    async def get_person_by_id(self, *, person_id: int) -> PersonInDB:
        person_row = await queries.get_person_by_id(
            self.connection,
            person_id=person_id,
        )
        if person_row:
            return PersonInDB(**person_row)

        raise EntityDoesNotExist(
            "person with id {0} does not exist".format(person_id),
        )


    async def _get_person_from_db_record(self, *, person_row: Any):
        return PersonInResponse(
            person=person_row
        )


    async def get_people_by_task_id(
          self, 
          task_id : int
          ) -> List[PersonInResponse]:
        people = await queries.get_people_by_task_id(
            self.connection,
            task_id=task_id
        )
        if people:
            return [
                await self._get_person_from_db_record(
                    person_row=person_row,
                )
                for person_row in people
            ]
        else:
            return []    

    async def get_good_people_by_task_id(
          self, 
          task_id : int
          ) -> List[PersonInResponse]:
        people = await queries.get_good_people_by_task_id(
            self.connection,
            task_id=task_id
        )
        if people:
            return [
                await self._get_person_from_db_record(
                    person_row=person_row,
                )
                for person_row in people
            ]
        else:
            return []    

    async def get_people_for_work_by_task_id(
          self, 
          task_id : int
          ) -> List[PersonInDB]:
        people = await queries.get_people_for_work_by_task_id(
            self.connection,
            task_id
        ).fetchall()
        return [
            await self._get_person_from_db_record(
                person_row,
            )
            for person_row in people
        ]

    async def create_people(self, people):
        for person in people:
            pass

    async def create_new_person(
        self,
        transaction,
        task_id: int,
        *,
        family: str,
        name: str,
        patronimic_name: Optional[str],
        bdate: str,
        docser: str,
        docno: str,
        docdt: str,
        snils: str,
        inn: Optional[str]='0',
        status: Optional[str]='new',
    ) -> PersonInDB:
        person = PersonInDB(
                    task_id=task_id, 
                    bdate=bdate, 
                    family=family, 
                    name=name, 
                    patronimic_name=patronimic_name,
                    docser=docser, 
                    docno=docno, 
                    docdt=docdt,
                    snils=snils, 
                    inn=inn, 
                    status=status,
                   )
        if transaction:
            person_row = await queries.create_new_person(
                self.connection,
                family=person.family,
                name=person.name,
                patronimic_name=person.patronimic_name,
                bdate=person.bdate,
                docser=person.docser,
                docno=person.bdate,
                docdt=person.docdt,
                snils=person.snils,
                inn=person.inn,
                status=person.status,
                task_id=person.task_id
            )
        else:    
            async with self.connection.transaction():
                person_row = await queries.create_new_person(
                    self.connection,
                    family=person.family,
                    name=person.name,
                    patronimic_name=person.patronimic_name,
                    bdate=person.bdate,
                    docser=person.docser,
                    docno=person.bdate,
                    docdt=person.docdt,
                    snils=person.snils,
                    inn=person.inn,
                    status=person.status,
                    task_id=person.task_id
                )

        return person.copy(update=dict(person_row))

    async def update_person_inn_and_state( 
        self,
        *,
        person_id: int,
        inn: str,
        status: str,
    ) -> PersonInDB:
        person_in_db = await self.get_person_by_id(person_id=person_id)

        person_in_db.status = status or person_in_db.status
        person_in_db.inn = inn or person_in_db.inn

        async with self.connection.transaction():
            await queries.update_person_inn_and_status(
                self.connection,
                person_id=person_id,
                new_inn=person_in_db.inn,
                new_status=person_in_db.status,
            )

        return person_in_db
