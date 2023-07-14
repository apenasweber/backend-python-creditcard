from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.credit_card import CreditCardCreate, CreditCard
from app.models.credit_card import CreditCard as CreditCardModel
from app.services.crypto_service import CryptoService

router = APIRouter()

@router.post("/credit-card", response_model=CreditCard)
def create_credit_card(card: CreditCardCreate, db: Session = Depends(get_db), crypto_service: CryptoService = Depends()):
    encrypted_number = crypto_service.encrypt(card.number)
    db_card = CreditCardModel(**card.dict(), number=encrypted_number)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/credit-card", response_model=List[CreditCard])
def read_credit_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CreditCardModel).offset(skip).limit(limit).all()

@router.get("/credit-card/{card_id}", response_model=CreditCard)
def read_credit_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(CreditCardModel).filter(CreditCardModel.id == card_id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card
