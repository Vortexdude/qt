from typing import Optional
from pydantic import BaseModel, Field, SecretStr, field_serializer, validator
from api.utils import ensure_email

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
    def validate_email(cls, v):
        return ensure_email(email=v)

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