from loguru import logger

from fastapi import APIRouter

from app.models.schemas.people  import (PersonIn,      
    PersonInResponse,
    PersonInCreate,
    PersonInUpdate,
)

router = APIRouter()

