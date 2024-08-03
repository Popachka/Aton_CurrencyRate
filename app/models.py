from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    number = Column(String, unique=True, nullable=False)
    
    countries = relationship('Country', back_populates='currency')
    
class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    currency_code = Column(String, ForeignKey('currencies.code'))
    currency = relationship('Currency', back_populates='countries')