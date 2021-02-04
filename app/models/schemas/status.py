from typing import Optional

from app.models.schemas.rwschema import RWSchema

class StatusInResponse(RWSchema):
    status: str
    message: Optional[str]

class TotalsInResponse(RWSchema):
    has_inn: Optional[int]
    no_inn: Optional[int]
    processed: Optional[int]
    to_process: Optional[int]
    total: Optional[int]

class TotalsForTaskInResponse(RWSchema):
    task_id: int
    has_inn: Optional[int]
    no_inn: Optional[int]
    processed: Optional[int]
    to_process: Optional[int]
    total: Optional[int]


class InnInResponse(RWSchema):
    inn: Optional[str]
    status: Optional[StatusInResponse]
    totals: Optional[TotalsInResponse]
    totals_for_task: Optional[TotalsForTaskInResponse]
