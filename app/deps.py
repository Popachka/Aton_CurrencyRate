from fastapi import HTTPException, Depends
import httpx
from .config import logger, settings
from .db import SessionLocal, init_db
from typing import Annotated
from sqlalchemy.orm import Session
async def check_url_availability(url: str) -> None:
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f'Проверка доступности URL: {url}')
            response = await client.get(url)
            response.raise_for_status()
            logger.info(f'URL {url} доступен')
        except httpx.HTTPStatusError:
            logger.error(f'URL {url} недоступен (HTTPStatusError)')
            raise HTTPException(status_code=503, detail=f'URL {url} недоступен')
        except httpx.RequestError:
            logger.error(f'Ошибка запроса к {url} (RequestError)')
            raise HTTPException(status_code=503, detail=f'Ошибка запроса к {url}')

async def check_urls() -> None:
    logger.info('Начало проверки URL-ов')
    await check_url_availability(settings.URL_LIST_OF_CURRENCY)
    await check_url_availability(settings.URL_RATES)
    logger.info('Проверка URL-ов завершена')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]