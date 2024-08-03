from pydantic import BaseModel
class CurrencyBase(BaseModel):
    name: str
    code: str
    number: str

class CurrencyCreate(CurrencyBase):
    pass
class Currency(CurrencyBase):
    id: int
    class Config:
        orm_mode = True

class CountryBase(BaseModel):
    name: str
    currency_code: CurrencyBase
