from app.models.people_csv import get_field_names
import os
import io
import random
from typing import Any, List, Dict, OrderedDict
from fastapi import UploadFile
import aiofiles
import xlrd
from aiocsv import AsyncDictReader
from csv import DictWriter, QUOTE_MINIMAL as CSV_QUOTE_MINIMAL
from app.core.config import STORAGE_PATH
from app.db.repositories.people import PeopleRepository


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

async def process_excel_file(fpath: str, task_id: int, people_repo: PeopleRepository):
    people = []
    fieldnames=get_field_names()
    # NON ASYNCHRONOUS
    wbook = xlrd.open_workbook(fpath)
    sheet = wbook.sheet_by_index(0)
    async with people_repo.connection.transaction() as t:
        for rx in range(1, sheet.nrows):
            new_row = OrderedDict()
            cx = 0
            row = sheet.row(rx)
            for fn in fieldnames:
                if fn!='id':
                    new_row[fn] = row[cx]
                cx += 1
            await people_repo.create_new_person(t, task_id, new_row) 


async def process_csv_file(
        fpath: str, 
        task_id: int, 
        people_repo: PeopleRepository
    ):
    people = []
    fieldnames=get_field_names()
    async with aiofiles.open(fpath, mode="r", newline="") as afp:
        async with people_repo.connection.transaction() as t:
            reader = AsyncDictReader(
                        afp, 
                        fieldnames=fieldnames, 
                        restkey='rk',
                        restval='',
                        delimiter=';', 
                        quotechar="\"", 
                        lineterminator='\n', 
                        quoting=CSV_QUOTE_MINIMAL)
            await reader.__anext__()
            async for row in reader:
                new_row=OrderedDict()
                for fn in fieldnames:
                    if fn!='id':
                        new_row[fn]=row[fn]
                await people_repo.create_new_person(t, task_id, **new_row)

def data_to_csv(
    data: List[Dict[str, str]],
    **kwargs) -> Any:

    def get_header(data, **kwargs):
        header = kwargs.get('csv_header', None)
        if not header:
            header = list(data.keys())
        return header

    def get_writer(out, data):
        return  DictWriter(
                    out, 
                    fieldnames=list(data.keys()), 
                    quoting=CSV_QUOTE_MINIMAL,
                    restval='',
                    delimiter=';',
                    quotechar="\"",
                    lineterminator='\n'
                )

    out = io.StringIO()
    if data == None:
        return None
    elif data == []:
        return ''
    elif isinstance(data, dict):
        writer=get_writer(out, data)
        writer.writer.writerow(get_header(data, kwargs))                
        writer.writerow(data)
        return out
    elif isinstance(data, list):
        if isinstance(data[0],dict):
            v = list(data[0].values())[0]
            if len(data[0])<=1 and isinstance(v, dict):
                writer = get_writer(out, v)
                writer.writer.writerow(get_header(data, **kwargs))
                for item in data:
                    writer.writerow(list(item.values())[0])
                return out.getvalue()
            elif len(data[0])>1:    
                writer = get_writer(out, data[0])
                writer.writer.writerow(get_header(data, **kwargs))                
                for item in data:
                    writer.writerow(item)
                return out.getvalue()
            else:
                return ''
