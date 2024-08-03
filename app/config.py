import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '../.env'), env_ignore_empty=True, extra='ignore'
    )
    URL_LIST_OF_CURRENCY: str = 'https://www.iban.ru/currency-codes'
    URL_RATES: str = 'https://www.finmarket.ru/currency/rates/'

    SQLALCHEMY_SQLITE_URL: str = "sqlite:///./main.db"
# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

settings = Settings()


