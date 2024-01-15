from datetime import datetime, timedelta
from typing import Annotated
import typing_extensions
from api.server.database.users import UserData
from api.utils import Hasher
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from api.server.models.auth import User
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlow


from typing import Optional, Dict, Any, cast
from typing_extensions import Doc
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from pydantic import BaseModel
SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRATION: int = 30


# --> https://stackoverflow.com/questions/67307159/what-is-the-actual-use-of-oauth2passwordbearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Will return this - {"access_token": access_token, "token_type":"bearer"}
# so whenever you use this the responce should be like this


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



# async def get_current_user(token: str = Annotated(str, Depends[OAuth2PasswordBearer(tokenUrl="token")])):
#     credential_exception = HTTPException(
#         status_code = status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials!",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         fname: str = payload['user']
#         if fname is None:
#             raise credential_exception
#     except JWTError:
#         raise credential_exception
#     user =  await UserData.find_by_fname(fname)
#     if not user['status']:
#         raise credential_exception
#     return user

# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

class Auth:

    @staticmethod
    async def login(login_data):
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




from fastapi.security import OAuth2

class OAuth2BearerToken(OAuth2):
    def __init__(
        self,
        scheme_name: str = None,
        description: str = None,
        auto_error: bool = True,
    ):
        flows = {"bearer": {"tokenUrl": None}}
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )


# class OAuthFlowAuthorizationCode(OAuthFlow):
#     authorizationUrl: str
#     tokenUrl: str

# class OAuthFlows(BaseModel):
#     authorizationCode: Optional[OAuthFlowAuthorizationCode] = None
#     class Config:
#         extra = "allow"

# class OAuth2Token(OAuth2):
#     """
#     OAuth2 flow for authentication using a bearer token obtained from the header.
#     An instance of it would be used as a dependency.
#     """

#     def __init__(
#         self,
#         tokenUrl: Annotated[str, Doc("The URL to obtain the OAuth2 token.")],
#         scheme_name: Annotated[Optional[str], Doc("Security scheme name.")] = None,
#         scopes: Annotated[Optional[Dict[str, str]], Doc("The OAuth2 scopes.")] = None,
#         description: Annotated[Optional[str], Doc("Security scheme description.")] = None,
#         auto_error: Annotated[bool, Doc("Whether to auto error on missing token.")] = True,
#     ):
#         if not scopes:
#             scopes = {}
#         flows = OAuthFlows(
#             authorizationCode=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})
#         )
#         super().__init__(
#             flows=flows,
#             scheme_name=scheme_name,
#             description=description,
#             auto_error=auto_error,
#         )
