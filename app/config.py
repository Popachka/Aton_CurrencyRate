import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


URL_LIST_OF_CURRENCY = 'https://www.iban.ru/currency-codes'
URL_RATES = 'https://www.finmarket.ru/currency/rates/'
