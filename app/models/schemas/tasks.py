import datetime

from typing import Optional

from pydantic import BaseModel
from fastapi import UploadFile, File

from app.models.domain.tasks import Task
from app.models.schemas.rwschema import RWSchema

class TaskIn(RWSchema):
    id: int

class TaskInCreate(RWSchema):
    dt: str
    state: str
    file: Optional[bytes]

class TaskInUpdate(RWSchema):
    state: str

class TaskInResponse(BaseModel):
    task: Task
