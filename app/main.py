from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Any
import datetime
from .deps import check_urls, get_db
from .config import logger, settings
from .utils import fetch_html, parse_currency_page
from sqlalchemy.orm import Session
from app.crud import all_create_currency
from app.shemas import CurrencyCreate
from app.db import init_db
from app.structure_data.cache import Cache
from app.deps import SessionDep
app = FastAPI()
cache = Cache()
init_db()


app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/pages')


@app.get('/', response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/api/upload')
async def upload_info(request: Request,
                      #   start_date: str = Form(...),
                      #   end_date: str = Form(...),
                      session: SessionDep,
                      _=Depends(check_urls)) -> Any:
    # logger.info(f'StartDate - {start_date}, EndDate - {end_date}')
    try:
        # start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        # end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # if start_date_obj >= end_date_obj:
        # raise HTTPException(status_code=400, detail='Дата начала не может быть больше даты конца')

        # delta = end_date_obj - start_date_obj
        # if delta.days > 730:
        # raise HTTPException(status_code=400, detail="Диапазон дат не может превышать 2 года")
        html_currency = await fetch_html(settings.URL_LIST_OF_CURRENCY)
        if html_currency:
            currency_data, country_data = parse_currency_page(html_currency, cache)
            currency_create_data = [CurrencyCreate(**currency) for currency in currency_data]
            all_create_currency(session=session, currency_data=currency_create_data)
            logger.info(f'Полученные данные о валютах: ')
        else:
            logger.error('Не удалось получить HTML-страницу с курсами валют')

        return
        # return templates.TemplateResponse('index.html', {'request': request, 'message': f"Вы выбрали диапазон: с {start_date} по {end_date}"})
    except HTTPException as e:
        return templates.TemplateResponse('index.html', {'request': request, 'message': e.detail})
    except ValueError as e:
        return templates.TemplateResponse('index.html', {'request': request, 'message': f'Ошибка в формате данных {e}'})
