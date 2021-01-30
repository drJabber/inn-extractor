from fastapi import APIRouter

from app.api.routes import tasks
from app.api.routes import people
from app.api.routes import person

router = APIRouter()

router.include_router(tasks.router, tags=["tasks"], prefix="/honor/task")
router.include_router(people.router, tags=["people"], prefix="/honor/people")
router.include_router(person.router, tags=["people"], prefix="/honor/person")