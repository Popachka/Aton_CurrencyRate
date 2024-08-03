from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List
from app.shemas import CurrencyCreate, Currency, CountryCreate
from app.models import Currency, Country
from app.config import logger

def all_create_currency(*, session: Session, currency_data: List[CurrencyCreate]) -> None:
    new_currencies = []
    existing_codes = {c.code for c in session.query(Currency.code).all()}
    logger.info(f'Найдено {len(existing_codes)} существующих кодов валют.')
    for data in currency_data: 
        if data.code not in existing_codes:
            new_currency = Currency(
                name=data.name,
                code=data.code,
                number=data.number
            )
            new_currencies.append(new_currency)
        else:
            logger.debug(f'Валюта с кодом {data.code} уже существует.')
    if new_currencies:
        session.bulk_save_objects(new_currencies)
        session.commit()
        logger.info(f'Добавлено {len(new_currencies)} новых валют.')
    else:
        logger.info('Не найдено новых валют для добавления.')

def all_create_country(*, session: Session, country_data: List[CountryCreate]) -> None:
    existing_countries = {c.name for c in session.query(Country).all()}
    existing_codes = {c.code for c in session.query(Currency.code).all()}

    new_countries = []

    for data in country_data:
        if data.name not in existing_countries:
            if data.currency_code in existing_codes:
                currency = session.query(Currency).filter_by(code = data.currency_code).one()
                new_country = Country(name = data.name, currency = currency)
                new_countries.append(new_country)
            else:
                logger.warning(f'Код валюты {data.currency_code} не найден для страны {data.name}.')
    if new_countries:
        session.add_all(new_countries)
        session.commit()
        logger.info(f'Добавлено {len(new_countries)} новых стран.')
    else:
        logger.info('Не найдено новых стран для добавления.')


def get_all_countries(session: Session) -> List[Country]:
    return session.query(Country).all()
def get_all_currencies_by_ids(session: Session, currency_ids: List[int]) -> List[str]:
    currency_numbers = session.query(Currency.number).filter(Currency.id.in_(currency_ids)).all()
    currency_numbers = [result[0] for result in currency_numbers]
    return currency_numbers
