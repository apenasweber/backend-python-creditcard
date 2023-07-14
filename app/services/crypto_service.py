from cryptography.fernet import Fernet

from app.core.config import settings


class CryptoService:
    def __init__(self):
        self.fernet = Fernet(settings.SECRET_KEY)

    def encrypt(self, message: str) -> str:
        return self.fernet.encrypt(message.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self.fernet.decrypt(token.encode()).decode()
