from locust import HttpUser, task, between


class CreditCardUser(HttpUser):
    wait_time = between(1, 2)
    auth_token = None

    def on_start(self):
        payload = {
            "username": "username",
            "password": "password"
        }
        response = self.client.post("/api/v1/login", json=payload)
        if response.status_code == 200:
            self.auth_token = response.json()["access_token"]
        else:
            raise Exception("Failed to authenticate")

    @task
    def create_credit_card(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {
            "number": "1234567890123456",
            "exp_date": "12/2024",
            "holder": "John Doe",
            "cvv": "123"
        }
        self.client.post("/api/v1/credit-card", json=payload, headers=headers)

    @task
    def get_credit_cards(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        self.client.get("/api/v1/credit-card", headers=headers)

    @task
    def get_credit_card(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        self.client.get("/api/v1/credit-card/1", headers=headers)

    @task
    def update_credit_card(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        payload = {
            "exp_date": "12/2025",
            "holder": "John Smith",
            "cvv": "456"
        }
        self.client.put("/api/v1/credit-card/1", json=payload, headers=headers)

    @task
    def delete_credit_card(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        self.client.delete("/api/v1/credit-card/1", headers=headers)
