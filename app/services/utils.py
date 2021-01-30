import os
import random
from fastapi import UploadFile, Depends
import aiofiles
from aiocsv import AsyncDictReader
from csv import QUOTE_MINIMAL as CSV_QUOTE_MINIMAL
from app.core.config import STORAGE_PATH
from app.db.repositories.people import PeopleRepository
from app.api.dependencies.database import get_repository


async def store_tmp_file(source: UploadFile) -> str:
    fpath = os.path.join(
        STORAGE_PATH, f'{random.randint(0, 5000)}_{source.filename}'
    )
    async with aiofiles.open(fpath, 'wb') as f:
        while True:
            chunk=await source.read(1024)
            if chunk:
                await f.write(chunk)
            else:
                f.close()
                break 

    return fpath

async def process_csv_file(
        fpath: str, 
        task_id: int, 
        people_repo: PeopleRepository
    ):
    people = []
    async with aiofiles.open(fpath, mode="r", encoding="utf-8", newline="") as afp:
        async with people_repo.connection.transaction() as t:
            async for row in AsyncDictReader(
                        afp, 
                        fieldnames=['id', 'family', 'name', 'patronimic_name', 'bdate', 'docser', 'docno', 'docdt', 'snils', 'inn', 'status'], 
                        restkey='rk',
                        restval='',
                        delimiter=';', 
                        quotechar="\"", 
                        lineterminator='\n', 
                        quoting=CSV_QUOTE_MINIMAL):
                new_row={k:v for k,v in row.items() if k!='id'}
                await people_repo.create_new_person(t, task_id, **new_row)
