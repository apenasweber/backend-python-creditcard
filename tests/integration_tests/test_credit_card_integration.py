# File: tests/integration/test_credit_card_integration.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.core.settings import settings

@pytest.fixture(scope="module")
def token(client):
    response = client.post(f"api/v1/login?username={settings.DB_USER}&password={settings.DB_PASSWORD}")
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def db_session():
    session = get_db()
    yield session
    session.close()

class TestCreditCardIntegration:
    def test_full_user_flow(self, client, token, db_session):
        card_data = {
            "exp_date": "2024-07-01",
            "holder": "John Doe",
            "number": "4539578763621486",
            "cvv": "123",
        }
        headers = {"Authorization": f"Bearer {token}"}

        # Test create operation
        response = client.post("/credit-card", headers=headers, json=card_data)
        assert response.status_code == 200
        created_card = response.json()

        # Test read operation
        response = client.get(f"/credit-card/{created_card['id']}", headers=headers)
        assert response.status_code == 200
        assert response.json() == created_card

        # Test update operation
        update_data = {"holder": "Jane Doe"}
        response = client.put(f"/credit-card/{created_card['id']}", headers=headers, json=update_data)
        assert response.status_code == 200
        created_card.update(update_data)
        assert response.json() == created_card

        # Test delete operation
        response = client.delete(f"/credit-card/{created_card['id']}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Credit card deleted successfully"}

        # Confirm deletion
        response = client.get(f"/credit-card/{created_card['id']}", headers=headers)
        assert response.status_code == 404
