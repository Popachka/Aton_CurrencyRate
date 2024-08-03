from fastapi import FastAPI, Form, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Any, List
import datetime
from .config import logger, settings
from .utils import fetch_html, parse_currency_page
from app.crud import all_create_currency, all_create_country, get_all_countries, get_all_currencies_by_ids
from app.shemas import CurrencyCreate, CountryCreate
from app.db import init_db
from app.structure_data.cache import Cache
from sqlalchemy.exc import SQLAlchemyError
from app.deps import SessionDep
from app.utils import convert_number_to_id, generate_urls

app = FastAPI()
cache = Cache()
init_db()


app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/pages')


@app.get('/', response_class=HTMLResponse)
def read_root(request: Request, session: SessionDep):
    countries = get_all_countries(session)
    if countries:
        return templates.TemplateResponse('index.html', {
            'request': request,
            'countries': countries
        })
    return templates.TemplateResponse('upload.html', {'request': request})


@app.post('/api/selectRate')
def select_rate(request: Request, session: SessionDep,
                start_date: str = Form(...),
                end_date: str = Form(...),
                currency_ids: List[int] = Form(...)
                ) -> Any:
    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    if (end_date_obj - start_date_obj).days > 730:  # 730 дней ≈ 2 года
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Разница между датами не может превышать 2 года."
    )

    try:
        currency_numbers = get_all_currencies_by_ids(session=session, currency_ids = currency_ids)
        ids = convert_number_to_id(currency_numbers)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла непредвиденная ошибка."
        ) from e
    except Exception as e:
        # Обработка других возможных исключений
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла непредвиденная ошибка."
        ) from e

    start_year, start_month, start_day = start_date.split('-')
    end_year, end_month, end_day = end_date.split('-')

    suffix_url_date = f'&bd={start_day}&bm={start_month}&by={start_year}&ed={end_day}&em={end_month}&ey={end_year}'
    urls = generate_urls(ids, suffix_url_date)
    return urls


@app.post('/api/upload')
async def upload_info(request: Request,
                      session: SessionDep,
                      ) -> Any:
    try:

        html_currency = await fetch_html(settings.URL_LIST_OF_CURRENCY)
        if html_currency:
            currency_data, country_data = parse_currency_page(
                html_currency, cache)
            currency_create_data = [CurrencyCreate(
                **currency) for currency in currency_data]
            all_create_currency(
                session=session, currency_data=currency_create_data)
            country_create_data = [CountryCreate(
                **country) for country in country_data]
            all_create_country(
                session=session, country_data=country_create_data)

            return RedirectResponse(url='/', status_code=302)
        else:
            logger.error('Не удалось получить HTML-страницу с курсами валют')
            return templates.TemplateResponse('upload.html', {'request': request, 'message': 'Не удалось получить данные с сайта.'})
        return
    except ValueError as e:
        return templates.TemplateResponse('upload.html', {'request': request, 'message': f'Ошибка в формате данных {e}'})
