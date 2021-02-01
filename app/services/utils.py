import os
import io
import random
from typing import Any, List, Dict
from fastapi import UploadFile, Depends
import aiofiles
from aiocsv import AsyncDictReader
from csv import DictWriter, QUOTE_MINIMAL as CSV_QUOTE_MINIMAL
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

def data_to_csv(data: List[Dict[str, str]]) -> Any:

    def get_writer(out, data):
        return  DictWriter(
                    out, 
                    fieldnames=data.keys(), 
                    quoting=CSV_QUOTE_MINIMAL,
                    restval='',
                    delimiter=';',
                    quotechar="\"",
                    lineterminator='\n'
                )

    out = io.BytesIO()
    if data == None:
        return None
    elif data == []:
        return ''
    elif isinstance(data, dict):
        writer=get_writer(out, data)
        writer.writerow(data)
        return out
    elif isinstance(data, list):
        if isinstance(data[0],dict):
            v = data[0].values()[0]
            if len(data[0])<=1 and isinstance(v, dict):
                writer = get_writer(out, v)
                for item in data:
                    writer.writerow(item[1])
                return out
            elif len(data[0])>1:    
                writer = get_writer(out, data[0])
                for item in data:
                    writer.writerow(item)
                return out
            else:
                return ''


        writer=get_writer(out, data)
        for item in data:
            writer.writerow(item)
        return out
