from passlib.context import CryptContext
from passlib.exc import UnknownHashError

# pbkdf2_sha256 avoids bcrypt backend/version conflicts and works reliably across platforms.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (UnknownHashError, ValueError, TypeError):
        return False