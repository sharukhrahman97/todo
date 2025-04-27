import hashlib
import os
import hmac
from typing import Tuple
from dotenv import load_dotenv
import os
from ..core.config import settings

load_dotenv()

# Get the pepper from environment variables
PEPPER = settings.PEPPER

def generate_salt(length: int = 128) -> str:
    return os.urandom(length).hex()

def hash_password(password: str, salt: str) -> Tuple[str, str]:
    password_with_pepper = (password + PEPPER).encode('utf-8')

    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',  # Algorithm
        password_with_pepper,
        bytes.fromhex(salt),  # Salt as bytes
        100000  # Iterations
    )
    hashed_password = hash_obj.hex()
    return salt, hashed_password

def verify_password(password: str, stored_salt: str, stored_hashed_password: str) -> bool:
    _, computed_hashed_password = hash_password(password, stored_salt)
    return hmac.compare_digest(computed_hashed_password, stored_hashed_password)
