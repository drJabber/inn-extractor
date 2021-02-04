
import json
from aiohttp import TCPConnector, ClientSession
from typing import Tuple
from fastapi import status
from starlette.status import HTTP_200_OK
from app.core import config
from app.models.domain.people import PersonInDB
from app.models.schemas.status import InnInResponse, StatusInResponse


class Utils:
    @staticmethod
    def get_headers():
        return {
            "User-Agent": "android/2.1.10/SomePhone",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

class Taxru:
    def __init_(self):
        pass
    
    async def get_inn(person: PersonInDB, captcha: str, token: str) -> InnInResponse:

        headers = Utils.get_headers()

        state=StatusInResponse()
        state.status='none' 

        docnum = person.docser
        if ' ' not in docnum:
            docnum = docnum[:2] + ' ' + docnum[2:]
        docnum = docnum + ' ' + person.docno

        inn=person.inn

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            data={
                'c': 'innMy',
                'fam': person.family,
                'nam': person.name,
                'otch': person.patronimic_name,
                'bdate': person.bdate,
                'bplace': '',
                'doctype': '21',
                'docno': docnum,
                'docdt': person.docdt,
                'captcha': captcha,
                'captchaToken': token

            }
            async with session.post(
                config.TAXRU_SERVICE_URL+config.TAXRU_INN_API, 
                data=json.dumps(data), 
                headers=headers
            ) as response:
                if response:
                    state.status = 'unknown'
                    state.message = 'неизвестная ошибка'
                    if response.status == status.HTTP_200_OK:
                        if response['code'] == '0':
                            state.status='no data'
                            state.message = 'неизвестная ошибка'
                        elif response['code'] == '1':
                            state.status='ok'
                            state.message = 'ok'
                            inn = response['inn']
                        elif response['code'] == '2':
                            state.status='unknown'
                            state.message = 'неизвестная ошибка'
                        if response['code'] == '3':
                            state.status='not identified by egrn'
                            state.message = 'ФЛ не идетнифицировано ЕГРН'
                    else:
                        if 'ERRORS' in response:
                            errors=response['ERRORS']
                            if 'captcha' in errors:
                                if errors['captcha']:
                                    state.status = 'captcha'
                                    state.message = 'неверная капча'
                                else:
                                    state.status = json.dumps(errors)
                                    state.message = 'неверные данные ФЛ'
                            else:
                                state.status = json.dumps(errors)
                                state.message = 'неверные данные ФЛ'
                        else:
                            state.status = 'taxru error'
                            state.message = 'ошибка запроса к сервису nalog.ru'
        return  InnInResponse(inn=inn, status=state)

