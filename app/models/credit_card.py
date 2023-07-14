from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    exp_date = Column(Date, index=True)
    holder = Column(String, index=True)
    number = Column(String, index=True)
    cvv = Column(String, index=True)
