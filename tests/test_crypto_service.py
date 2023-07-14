from app.services.crypto_service import CryptoService


def test_crypto_service():
    crypto_service = CryptoService()
    encrypted_text = crypto_service.encrypt("plaintext")
    assert encrypted_text != "plaintext"
    assert crypto_service.decrypt(encrypted_text) == "plaintext"
