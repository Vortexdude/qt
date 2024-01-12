from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from api.utils import Hasher
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.server.models.auth import LoginSchema
from api.server.database.users import UserData
from datetime import datetime, timedelta
from jose import JWTError, jwt
router = APIRouter()
SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRATION: int = 30

# --> https://stackoverflow.com/questions/67307159/what-is-the-actual-use-of-oauth2passwordbearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')



async def authenticate_user(email: str, password: str):
    user = await UserData.user_validation(email)
    if not user[0]:
        return False
    if not Hasher.verify_password(password, user[1]['hashed_password']):
        return False
    return user[1]

def create_access_token(data: dict, expiration_time: timedelta | None = None):
    to_encode = data.copy()
    if expiration_time:
        expire = datetime.utcnow() + expiration_time
    else:
        expire = datetime.utcnow() | timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/')
async def login(login_data: LoginSchema):
    # generate token and after the user validaation
    _is_user = await authenticate_user(login_data.email, login_data.password)
    if not _is_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    access_token = create_access_token(data={'user': _is_user['fname']}, expiration_time=token_expiration)
    return {"acces_token": access_token, "token_type": "bearer"}
