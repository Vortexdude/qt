# from fastapi import APIRouter
# from passlib.context import CryptContext
# from pydantic import BaseModel
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from api.server.models.auth import Token, TokenData, User, UserInDB

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# pwd_context = CryptContext(schemes=['bcrypt'], depricated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# def verify_pasword(plain_paaword, hashed_password):
#     return pwd_context.verify(plain_paaword, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)







# router = APIRouter()

# @router.post('/')
# async def login(login_data: dict):
#     return {"message": "login Success!"}
