from typing import Optional, List
import httpx
from bs4 import BeautifulSoup
from .config import logger
import re
from app.structure_data.cache import Cache
from app.config import settings

async def fetch_html(url: str) -> Optional[str]:
    """Получение HTML-страницы по URL"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError:
            return None
        except httpx.RequestError:
            return None


def get_new_currencies(cache: Cache, currency_data: list[dict]) -> list[dict]:
    codes = set(cache.currency_cache.keys())
    if not codes:
        return currency_data
    new_currencies = [
        currency for currency in currency_data if currency['code'] not in codes]
    return new_currencies


def get_new_countries(cache: Cache, country_data: list[dict]) -> list[dict]:
    names = set(cache.country_cache.keys())
    if not names:
        return country_data
    new_countries = [
        country for country in country_data if country['name'] not in names]
    return new_countries


def parse_currency_page(html: str, cache: Cache) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('tr')
    currency_data = []
    country_data = []
    seen_codes = set()
    for tr in table[1:]:
        tr = str(tr)
        matches = re.findall(r'<td>(.*?)<\/td>', tr)
        if matches and len(matches) == 4:
            country_name, currency_name, code, number = matches
            if number not in settings.countries_numbers_to_currencies:
                continue
            if code not in seen_codes:
                currency = {
                    'name': currency_name,
                    'code': code,
                    'number': number
                }
                currency_data.append(currency)
            seen_codes.add(code)
            country = {
                'name': country_name,
                'currency_code': code
            }
            country_data.append(country)
        else:
            logger.error(f'Неверный формат строки - строка: {tr}')

    codes = [currency['code'] for currency in currency_data]
    unique_codes = set(codes)
    logger.info(f'{len(codes) == len(unique_codes)} - Все ли уникальны коды в массиве?')
    if len(codes) != len(unique_codes):
        logger.error(f'Коды не уникальны в массиве! Останавливаем выполнение.')
        return None

    new_currencies = get_new_currencies(cache, currency_data)
    new_countries = get_new_countries(cache, country_data)

    for currency in new_currencies:
        cache.set_currency(currency['code'], currency)

    for country in new_countries:
        cache.set_country(country['name'], country['currency_code'])
    logger.info(f'Валюты: {len(cache.currency_cache)} и Стран: {len(cache.country_cache)} было закешировано')
    

    return new_currencies, new_countries

def convert_number_to_id(currency_numbers: List[str]) -> List[str]:
    print(currency_numbers)
    numbers = set(currency_numbers)
    numbers_to_id_dict = settings.countries_numbers_to_currencies
    ids = [numbers_to_id_dict[number] for number in numbers if number in numbers_to_id_dict]
    if len(ids) == 0:
        raise 
    return ids
def generate_urls(ids: List[str], suffix_url_date: str) -> List[str]:
    urls = []
    for id_from_site in ids:
        s = ''
        s += f"id=10148&pv=1&cur={id_from_site}" + suffix_url_date
        urls.append(s)
    return urls