from pydantic import BaseModel, validator
from api.utils import ensure_email

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    fname: str | None = None

class LoginSchema(BaseModel):
    email: str
    password: str

    @validator('email')
    def vlaidate_email(cls, v):
        return ensure_email(v)

class User(BaseModel):
    fname: str
    lname: str 
    email: str 
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str
