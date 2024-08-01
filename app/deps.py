from fastapi import HTTPException
import httpx
from .config import logger, URL_LIST_OF_CURRENCY, URL_RATES  

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
    await check_url_availability(URL_LIST_OF_CURRENCY)
    await check_url_availability(URL_RATES)
    logger.info('Проверка URL-ов завершена')
