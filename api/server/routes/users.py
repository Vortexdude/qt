from fastapi import APIRouter, Body
from api.server.messages import USERS
from api.server.models.users import UsersSchema, UpdateUserModel
from api.server.controller.user import User

router = APIRouter()


@router.get("/", response_description=USERS['fetch_success'])
async def get_users() -> dict:
    """ Fetch all the users """

    return await User.get_all_users()


@router.post("/",  response_description=USERS['inserted_success'])
async def create_user(user: UsersSchema = Body(...)):
    """ Create new User in the database """

    return await User.create_user(user)

@router.put("/{user_id}", response_description=USERS['updated_success'])
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    """" Update the user if needed """
    
    return await User.patch_user(user_id, user)
