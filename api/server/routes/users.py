from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from api.server.models.users import (
    UsersSchema,
    UpdateUserModel,
    ResponceModel,
    ErrorResponceModel
)

from api.server.database import (
    add_user,
    retrieve_users,
    update_user_details
)


router = APIRouter()


@router.get("/", response_description="Data Fetched successfully !")
async def get_users():
    users = await retrieve_users() 
    return users if users else {"error": "cant get details"}

@router.post("/",  response_description="User data added into the database")
async def create_user(user: UsersSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    if "error" in new_user:
        return ErrorResponceModel(new_user['error'], 503, "Email Key should be unique")
    else:
        return ResponceModel(new_user, "User data added into the database")

@router.put("/{user_id}", response_description="Data Updated succesfully!")
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    req = {k: v for k,v in user.model_dump().items() if v is not None}
    if user_id:
        user = await update_user_details(id=user_id, user_data=req)
        if user:
            return user
