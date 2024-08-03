import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.db import Base, engine
from sqlalchemy import text
# Тестовый класс или функция
def test_database_connection(fake_db):
    # Проверяем, что сессия была успешно создана
    assert fake_db is not None, "Не удалось создать сессию базы данных"

    # Создаем таблицы
    try:
        Base.metadata.create_all(engine)
    except OperationalError as e:
        pytest.fail(f"Не удалось создать таблицы: {e}")
    
    # Пробуем сделать запрос к базе данных
    try:
        # Используем `fake_db` как сессию
        result = fake_db.execute(text('SELECT 1'))
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Не удалось выполнить запрос к базе данных: {e}")
