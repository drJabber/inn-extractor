from typing import Optional

from starlette.datastructures import UploadFile
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel


class Task(RWModel,IDModelMixin):
    dt : str
    state: str

class TaskInDB(Task, DateTimeModelMixin):
    file: Optional[bytes]
