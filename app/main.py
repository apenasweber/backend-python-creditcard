from fastapi import FastAPI
from app.api.v1.endpoints.credit_card import router as credit_card_router

app = FastAPI()

app.include_router(credit_card_router, prefix="/api/v1")
