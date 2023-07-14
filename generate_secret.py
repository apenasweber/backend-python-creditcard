import os

from cryptography.fernet import Fernet
from dotenv import find_dotenv, load_dotenv, set_key

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    key = Fernet.generate_key()
    SECRET_KEY = key.decode()
    print(f"Generated secret key: {SECRET_KEY}")
    # Salva a nova chave no arquivo .env
    set_key(find_dotenv(), "SECRET_KEY", SECRET_KEY)
else:
    print("Using existing secret key.")
