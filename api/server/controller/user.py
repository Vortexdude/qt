from api.server.database.users import UserData
from api.server.messages import USERS
from fastapi.encoders import jsonable_encoder
from api.server.models.users import ResponceModel, ErrorResponceModel

class User:

    @staticmethod
    def get_all_users() -> list:
        users = UserData.fetch_all_users()
        return users if users else {"error": USERS['fetch_error']}
    
    @staticmethod
    async def create_user(user):
        user = jsonable_encoder(user)
        new_user = await UserData.inser_record(user)
        if new_user['status']:
            return ResponceModel(new_user, USERS['inserted_success'])
        
        if not new_user['status'] and new_user['key'] == 'email':
            return ErrorResponceModel("Key Validation", 503, USERS['email_validation'])
        
        return ErrorResponceModel("Error", 503, "Other KeyError")

    @staticmethod
    async def patch_user(user_id: str, user):
        req = {k: v for k,v in user.model_dump().items() if v is not None}
        if user_id:
            user = await UserData.update_record(id=user_id, user_data=req)
            return user if user else None
