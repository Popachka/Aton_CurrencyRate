from typing import Optional
import httpx
from bs4 import BeautifulSoup
from .config import logger
import re
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

def parse_currency_page(html: str) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('tr')

    for tr in table[1:]:
        tr = str(tr)
        tr = re.sub(r"<[^>]+>", "", tr).split()
        logger.info(f'tr - {tr}')