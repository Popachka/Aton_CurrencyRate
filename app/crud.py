from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List
from app.shemas import CurrencyCreate, Currency
from app.models import Currency, Country


def all_create_currency(*, session: Session, currency_data: List[CurrencyCreate]) -> None:
    new_currencies = []
    existing_codes = {c.code for c in session.query(Currency.code).all()}
    for data in currency_data: 
        if data.code not in existing_codes:
            new_currency = Currency(
                name=data.name,
                code=data.code,
                number=data.number
            )
            new_currencies.append(new_currency)
    if new_currencies:
        session.bulk_save_objects(new_currencies)
        session.commit()