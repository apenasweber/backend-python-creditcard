from datetime import date
from typing import Optional

from pydantic import BaseModel


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
