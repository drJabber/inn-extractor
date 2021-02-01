from typing import Optional, List, Any
from fastapi import UploadFile
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.schemas.tasks import TaskInResponse
from app.models.domain.tasks import Task, TaskInDB


class TasksRepository(BaseRepository):
    async def get_task_by_id(self, *, task_id: int) -> TaskInDB:
        task_row = await queries.get_task_by_id(
            self.connection,
            task_id=task_id,
        )
        if task_row:
            return TaskInDB(**task_row)

        raise EntityDoesNotExist(
            "task with id {0} does not exist".format(task_id),
        )

    async def _get_task_from_db_record(self, task_row: Any):
        return TaskInResponse(
            task=Task(
                id_ = task_row["id"],
                dt = task_row["dt"],
                state = task_row["state"]
            )
            # file = task_row["file"]
        )


    async def get_tasks_for_work(self) -> List[TaskInDB]:
        tasks = await queries.get_tasks_for_work(
            self.connection
        )
        if tasks:
            return [
                await self._get_task_from_db_record(
                    task_row,
                )
                for task_row in tasks
            ]
        else:
            return []

    async def get_tasks_done_by_date(self, dt: Any) -> List[TaskInDB]:
        tasks = await queries.get_tasks_done_by_date(
            self.connection, dt=dt,
        )
        if tasks:
            return [
                await self._get_task_from_db_record(
                    task_row,
                )
                for task_row in tasks
            ]
        else:
            return []

    async def get_all_tasks(self) -> List[TaskInDB]:
        tasks = await queries.get_all_tasks(
            self.connection
        ).fetchall()
        return [
            await self._get_task_from_db_record(
                task_row,
            )
            for task_row in tasks
        ]                    

    async def create_new_task(
        self,
        *,
        dt: str,
        state: str,
        # file: UploadFile,
    ) -> TaskInDB:
        task = TaskInDB(
                dt=dt, state=state,  \
            )

        async with self.connection.transaction() as t:
            task_row = await queries.create_new_task(
                self.connection,
                dt=task.dt,
                state=task.state,
                # file=task.file,
            )

        return task.copy(update=dict(task_row))

    async def update_task_state( 
        self,
        *,
        task_id: int,
        state: Optional[str] = None,
    ) -> TaskInDB:
        task_in_db = await self.get_task_by_id(task_id=task_id)

        task_in_db.state = state or task_in_db.state

        async with self.connection.transaction():
            task_in_db.updated_at = await queries.update_task_state(
                self.connection,
                task_id=task_id,
                new_state=task_in_db.state,
            )

        return task_in_db
