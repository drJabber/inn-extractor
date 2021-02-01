from typing import Optional

from starlette.datastructures import UploadFile
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class Task(IDModelMixin, RWModel):
    dt : str
    state: str

class TaskInDB(DateTimeModelMixin, Task):
    file: Optional[bytes]
