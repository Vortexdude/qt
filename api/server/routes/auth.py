from fastapi import APIRouter, Depends
from api.server.models.auth import LoginSchema
from api.server.controller.auth import Auth, OAuth2BearerToken
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from api.server.models.auth import User
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/")

@router.post('/')
async def login(login_data: LoginSchema):
    """ Login endpoint """

    return await Auth.login(login_data)


@router.get('/me')
async def me(current_user: Annotated[User, Depends(oauth2_scheme)]):
    return {"status": current_user}
