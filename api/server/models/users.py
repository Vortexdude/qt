from typing import Optional
import re
from pydantic import BaseModel, Field, SecretStr, field_serializer, validator

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class Model(BaseModel):
    password: SecretStr

    @field_serializer('password', when_used='always')
    def dump_secret(self, v):
        return v.get_secret_value()

class UsersSchema(Model):
    fname: str = Field(...)
    lname: str = Field(...)
    email: str = Field(...)

    @validator('email')
    def ensure_email(cls, v):
        if not (re.fullmatch(regex, v)):
            raise ValueError('Invalid email')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "fname": "nitin",
                "lname": "namdev",
                "email": "nitin.namdev@dev.de",
                "password": "superSecret",
            }
        }

class UpdateUserModel(Model):
    fname: Optional[str]
    lname: Optional[str]
    email: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "fname": "Raj",
                "lname": "kundra",
                "email": "raj.kundra@ullu.com",
                "password": "softP**n"

            }
        }

def ResponceModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "messge": message
    }

def ErrorResponceModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }