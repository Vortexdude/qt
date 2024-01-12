from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRATION: int = 30

class JWT:
    @staticmethod
    def create_access_token(data: dict, expiration_time: timedelta | None = None):
        to_encode = data.copy()
        if expiration_time:
            expire = datetime.utcnow() + expiration_time
        else:
            expire = datetime.utcnow() | timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
