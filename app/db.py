from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from app.config import settings

engine = create_engine(settings.SQLALCHEMY_SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)
def init_db():
    Base.metadata.create_all(bind=engine)