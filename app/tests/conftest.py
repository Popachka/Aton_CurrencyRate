import os
import pytest
from sqlalchemy import create_engine
from app.db import SessionLocal, Base

SQLALCHEMY_DB_URL = 'sqlite:///./test.db'

def db_prep():
    print('Удаляем старую тестировочную базу')
    if os.path.exists('./test.db'):
        os.remove('./test.db')
    
    print('Создаем тестовую базу')
    engine = create_engine(SQLALCHEMY_DB_URL)
    Base.metadata.create_all(engine)
    print('Тестовая база создана')

@pytest.fixture(scope="session", autouse=True)
def fake_db():
    db_prep()
    print(f"Initializing test.db …")
    
    engine = create_engine(SQLALCHEMY_DB_URL)
    db = SessionLocal()
    
    print(f"test.db ready to rock!")
    
    try:
        yield db
    finally:
        db.close()
        os.remove('test.db')
