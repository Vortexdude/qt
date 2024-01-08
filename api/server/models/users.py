from typing import Optional, ForwardRef

from pydantic import BaseModel, Field, SecretStr


class UsersSchema(BaseModel):
    fname: str = Field(...)
    lname: str = Field(...)
    email: str = Field(...)
    password:  Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "fname": "nitin",
                "lname": "namdev",
                "email": "nitin.namdev@dev.de",
                "password": "superSecret",
            }
        }

class UpdateUserModel(BaseModel):
    fname: Optional[str]
    lname: Optional[str]
    email: Optional[str]
    password: SecretStr

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None
         }
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

def ErrorResponceModel(erro, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }