from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from api.server.database.users import UserData
from api.server.messages import USERS
from api.server.models.users import (
    UsersSchema,
    UpdateUserModel,
    ResponceModel,
    ErrorResponceModel
)


router = APIRouter()


@router.get("/", response_description=USERS['fetch_success'])
async def get_users() -> dict:
    """ Fetch all the users """

    users = await UserData.fetch_all_users()
    return users if users else {"error": USERS['fetch_error']}

@router.post("/",  response_description=USERS['inserted_success'])
async def create_user(user: UsersSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await UserData.inser_record(user)
    if new_user['status']:
        return ResponceModel(new_user, USERS['inserted_success'])
    
    if not new_user['status'] and new_user['Key'] == 'email':
        return ErrorResponceModel("Key Validation", 503, USERS['email_validation'])
    
    ErrorResponceModel("Error", 503, "Other KeyError")

@router.put("/{user_id}", response_description=USERS['updated_success'])
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    req = {k: v for k,v in user.model_dump().items() if v is not None}
    if user_id:
        user = await UserData.update_record(id=user_id, user_data=req)
        return user if user else None
