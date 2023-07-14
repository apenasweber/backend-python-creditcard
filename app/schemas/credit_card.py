from datetime import date
from pydantic import BaseModel
from typing import Optional

class CreditCardBase(BaseModel):
    exp_date: date
    holder: str
    cvv: Optional[str] = None

class CreditCardCreate(CreditCardBase):
    number: str

class CreditCard(CreditCardBase):
    id: int
    number: str  # this will be the encrypted number

    class Config:
        orm_mode = True
