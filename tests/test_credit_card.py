from datetime import date
import pytest
from app.models.credit_card import CreditCardModel
from app.main import app
from app.core.database import get_db
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def db_session():
    session = get_db()
    yield session
    session.close()

class TestCreditCardModel:
    def test_exp_date_valid(self):
        # Valid and future expiration date
        exp_date = date.today().replace(year=date.today().year + 1)
        cc = CreditCardModel(exp_date=exp_date)
        assert cc.is_exp_date_valid()

    def test_exp_date_invalid(self):
        # Invalid expiration date
        exp_date = "2022-13-01"  # Invalid month
        cc = CreditCardModel(exp_date=exp_date)
        assert not cc.is_exp_date_valid()

        # Expiration date in the past
        exp_date = date.today().replace(year=date.today().year - 1)
        cc = CreditCardModel(exp_date=exp_date)
        assert not cc.is_exp_date_valid()

    def test_holder_valid(self):
        # Holder with more than 2 characters
        holder = "John Doe"
        cc = CreditCardModel(holder=holder)
        assert cc.is_holder_valid()

    def test_holder_invalid(self):
        # Empty holder
        holder = ""
        cc = CreditCardModel(holder=holder)
        assert not cc.is_holder_valid()

        # Holder with less than 2 characters
        holder = "A"
        cc = CreditCardModel(holder=holder)
        assert not cc.is_holder_valid()

    def test_number_valid(self):
        # Valid card number
        number = "4539578763621486"  # Valid Visa card number
        cc = CreditCardModel(number=number)
        assert cc.is_number_valid()

    def test_number_invalid(self):
        # Invalid card number
        number = "1111111111111111"
        cc = CreditCardModel(number=number)
        assert not cc.is_number_valid()

    def test_cvv_valid(self):
        # CVV with 3 characters
        cvv = "123"
        cc = CreditCardModel(cvv=cvv)
        assert cc.is_cvv_valid()

        # CVV with 4 characters
        cvv = "1234"
        cc = CreditCardModel(cvv=cvv)
        assert cc.is_cvv_valid()

    def test_cvv_invalid(self):
        # CVV with less than 3 characters
        cvv = "12"
        cc = CreditCardModel(cvv=cvv)
        assert not cc.is_cvv_valid()

        # CVV with more than 4 characters
        cvv = "12345"
        cc = CreditCardModel(cvv=cvv)
        assert not cc.is_cvv_valid()

    @pytest.mark.parametrize(
        "exp_date, holder, number, cvv, is_valid",
        [
            # Valid case
            (date.today().replace(year=date.today().year + 1), "John Doe", "4539578763621486", "123", True),
            # Invalid case: Invalid expiration date
            ("2022-13-01", "John Doe", "4539578763621486", "123", False),
            # Invalid case: Invalid holder
            (date.today().replace(year=date.today().year + 1), "", "4539578763621486", "123", False),
            # Invalid case: Invalid card number
            (date.today().replace(year=date.today().year + 1), "John Doe", "1111111111111111", "123", False),
            # Invalid case: Invalid CVV
            (date.today().replace(year=date.today().year + 1), "John Doe", "4539578763621486", "12345", False),
        ]
    )
    def test_credit_card_validation(self, exp_date, holder, number, cvv, is_valid):
        cc = CreditCardModel(exp_date=exp_date, holder=holder, number=number, cvv=cvv)
        assert cc.is_valid() == is_valid

class TestCreditCardCreateOperations:
    def test_create_credit_card_valid(self, client):  
        card_data = {
            "exp_date": "2024-07-01",
            "holder": "John Doe",
            "number": "4539578763621486",
            "cvv": "123",
        }
        response = client.post("/credit-card", json=card_data)
        assert response.status_code == 200
        assert response.json()["holder"] == "John Doe"
        

    def test_create_credit_card_invalid(self, client):  
        card_data = {
            "exp_date": "2022-13-01",
            "holder": "",
            "number": "1111111111111111",
            "cvv": "12345",
        }
        response = client.post("/credit-card", json=card_data)
        assert response.status_code == 400

        
        db_card = db_session.query(CreditCardModel).filter_by(holder="").first()
        assert db_card is None

class TestCreditCardReadOperations:
    pass

class TestCreditCardUpdateOperations:
    pass

class TestCreditCardDeleteOperations:
    def test_delete_credit_card_valid(self, client, db_session):  
        card_data = {
            "exp_date": "2024-07-01",
            "holder": "John Doe",
            "number": "4539578763621486",
            "cvv": "123",
        }
        response = client.post("/credit-card", json=card_data)
        assert response.status_code == 200
        created_card = response.json()

        response = client.delete(f"/credit-card/{created_card['id']}")
        assert response.status_code == 200
        assert response.json() == {"message": "Credit card deleted successfully"}

        db_card = db_session.query(CreditCardModel).filter_by(id=created_card['id']).first()
        assert db_card is None

    def test_delete_credit_card_invalid(self, client):  
        response = client.delete("/credit-card/99999999")  
        assert response.status_code == 404


class TestCreditCardEndpoints:
    pass

