from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.credit_card import CreditCardSchema, CreditCardCreateSchema, CreditCardUpdateSchema
from app.services.crypto_service import CryptoService
from datetime import datetime
from creditcard import CreditCard
from app.models.credit_card import CreditCardModel
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/credit-card", response_model=CreditCardSchema, tags=["Cartões de Crédito"])
def create_credit_card(
    card: CreditCardCreateSchema,
    db: Session = Depends(get_db),
    crypto_service: CryptoService = Depends(),
    current_user: User = Depends(get_current_user)
):
    try:
        exp_date_str = card.exp_date.strftime("%m/%Y")
        exp_date = datetime.strptime(exp_date_str, "%m/%Y")
        if exp_date < datetime.now():
            raise HTTPException(status_code=400, detail="Data de expiração inválida")
    except ValueError:
        raise HTTPException(status_code=400, detail="Data de expiração inválida")

    if not card.holder or len(card.holder) < 3:
        raise HTTPException(status_code=400, detail="Titular inválido")

    cc = CreditCard(card.number)
    if not cc.is_valid():
        raise HTTPException(status_code=400, detail="Número de cartão inválido")

    encrypted_number = crypto_service.encrypt(card.number)

    if card.cvv and (len(card.cvv) < 3 or len(card.cvv) > 4):
        raise HTTPException(status_code=400, detail="CVV inválido")

    card_data = card.dict()
    card_data["number"] = encrypted_number

    db_card = CreditCardModel(**card_data)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@router.get("/credit-card", response_model=List[CreditCardSchema],tags=["Cartões de Crédito"])
def read_credit_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CreditCardModel).offset(skip).limit(limit).all()

@router.get("/credit-card/{card_id}", response_model=CreditCardSchema,tags=["Cartões de Crédito"])
def read_credit_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(CreditCardModel).filter(CreditCardModel.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.put("/credit-card/{id}", response_model=CreditCardSchema,tags=["Cartões de Crédito"])
def update_credit_card(
    id: int,
    card_update: CreditCardUpdateSchema,
    db: Session = Depends(get_db),
    crypto_service: CryptoService = Depends(),
):
    card = db.query(CreditCardModel).filter(CreditCardModel.id == id).first()

    if not card:
        raise HTTPException(status_code=404, detail="Cartão de crédito não encontrado")

    card.exp_date = card_update.exp_date
    card.holder = card_update.holder
    card.cvv = card_update.cvv

    db.commit()
    return card
