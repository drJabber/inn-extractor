import time
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from aiohttp import ClientSession, TCPConnector
from app.core import config

router = APIRouter()

class Utils:
    @staticmethod
    def get_headers():
        return {
            "User-Agent": "android/2.1.10/SomePhone",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Accept": "text/plain",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "https://service.nalog.ru/inn.do"
        }


@router.get("/", response_class=PlainTextResponse, name="token:get")
async def get_token(
) -> PlainTextResponse:
    headers = Utils.get_headers()
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        params = {'r': time.time()}
        async with session.get(
            config.TAXRU_SERVICE_URL+config.TAXRU_CAPTCHA_API, 
            params=params, 
            headers=headers
        ) as response:
            content = await response.text()
            return PlainTextResponse(content=content)
