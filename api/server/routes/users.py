from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from api.server.tags import users_tag
from api.server.models.users import UsersSchema, UpdateUserModel
from api.server.database import (
    add_user,
    retrieve_users
)


router = APIRouter()

# @user_route.get("/users", status_code=200, tags=users_tag)
# async def get_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/",  response_description="User data added into the database")
async def create_user(user: UsersSchema = Body(...)):
    return {"user_fname": user.fname, "user_id": user_id}

# @user_route.put("/user/{user_id}", tags=users_tag)
# async def update_user(user_id: str, user: UpdateUserModel):
#     return {"user_fname": user.fname, "user_id": user_id}


# @users_route.put("/")
