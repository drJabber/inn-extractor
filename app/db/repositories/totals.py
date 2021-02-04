from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.schemas.status import TotalsInResponse, TotalsForTaskInResponse


class TotalsRepository(BaseRepository):
    async def get_totals(self) -> TotalsInResponse:
        totals_row = await queries.get_people_totals(
            self.connection,
        )
        if totals_row:
            return TotalsInResponse(**totals_row)
        else:
            return TotalsInResponse()    

    async def get_totals_for_task(self, *, task_id: int) -> TotalsForTaskInResponse:
        totals_row = await queries.get_people_for_task_totals(
            self.connection,
            task_id=task_id
        )
        if totals_row:
            return TotalsInResponse(**totals_row)
        else:
            return TotalsInResponse()    
