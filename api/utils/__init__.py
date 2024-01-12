from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hasher:
    @staticmethod
    def verify_password(plain_passowrd: str, hashed_password: str):
        return pwd_context.verify(plain_passowrd, hashed_password)
    
    @staticmethod
    def generate_password_hash(passowrd: str) -> str:
        return pwd_context.hash(passowrd)


def ensure_email(email:str) -> str | None:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not (re.fullmatch(regex, email)):
        raise ValueError('Invalid email')
    return email
