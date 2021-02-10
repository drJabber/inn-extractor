
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
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "https://service.nalog.ru/inn.do"
        }

class Taxru:
    def __init_(self):
        pass
    
    async def get_inn(pself, person: PersonInDB, captcha: str, token: str) -> InnInResponse:

        headers = Utils.get_headers()
        proxy = None
        if config.HTTPS_PROXY:
            proxy = config.HTTPS_PROXY


        state=StatusInResponse(status='none', message='')

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
                config.TAXRU_SERVICE_URL+config.TAXRU_SERVICE_API, 
                data=data, 
                headers=headers,
                proxy = proxy
            ) as response:
                resp = await response.json()
                if resp:
                    state.status = 'unknown'
                    state.message = 'неизвестная ошибка'
                    if response.status == status.HTTP_200_OK:
                        if resp['code'] == 0:
                            state.status='no data'
                            state.message = 'информация об ИНН не найдена'
                        elif resp['code'] == 1:
                            state.status='ok'
                            state.message = 'ok'
                            inn = resp['inn']
                        elif resp['code'] == 2:
                            state.status='unknown'
                            state.message = 'неизвестная ошибка'
                        elif resp['code'] == 3:
                            state.status='not identified by egrn'
                            state.message = 'ФЛ не идетнифицировано ЕГРН'
                        elif resp['code'] == 99:
                            state.status='timeout'
                            state.message = 'Время запроса к nalog.ru превысило 180 секунд'
                    else:
                        if 'ERRORS' in resp:
                            errors=resp['ERRORS']
                            if 'captcha' in errors:
                                if errors['captcha']:
                                    state.status = 'captcha'
                                    state.message = 'неверная капча'
                                else:
                                    state.status = json.dumps(errors)
                                    state.message = 'неверные данные ФЛ'
                            else:
                                state.status = errors
                                state.message = 'неверные данные ФЛ'
                        elif 'ERROR' in resp:
                            state.status = resp['ERROR']
                            state.message = 'ошибка запроса к сервису nalog.ru'
                        else:
                            state.status = 'taxru error'
                            state.message = 'ошибка запроса к сервису nalog.ru'
        return  InnInResponse(inn=inn, status=state)

