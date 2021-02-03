from typing import Optional

from app.models.schemas.rwschema import RWSchema

class StatusInResponse(RWSchema):
    status: str
    message: Optional[str]
