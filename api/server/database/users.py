from bson.objectid import ObjectId
from api.server.database import db
from pymongo import errors

COLLECTION = "user_collection"

user_collection = db.get_collection(COLLECTION)  #<--- collection name

class UserData:
    
    @classmethod
    def to_json(cls, user: object) -> dict:
        """Ensure the ID is converted into the string"""

        return {
            "id": str(user["_id"]),
            "fname": user["fname"],
            "lname": user["lname"],
            "email": user["email"]
        }

    @classmethod
    async def fetch_all_users(cls) -> list:
        """"Class method allow to fetch all the users"""

        users = []
        async for user in user_collection.find():
            users.append(cls.to_json(user))
        return {"users": users}

    @classmethod
    async def inser_record(cls, user_data: dict) -> dict:
        """class method allow to insert the data in the user table """

        try:
            user = await user_collection.insert_one(user_data)
            new_user = await user_collection.find_one({"_id": user.inserted_id})
            new_user_json = cls.to_json(new_user)
            new_user_json['status'] = True
            return new_user_json

        except errors.DuplicateKeyError as E:
            if "email" in vars(E)['_OperationFailure__details']['keyPattern']:
                return {"status": False, "Key": "email"}
            else:
                return {"status": False, "key": vars(E)['_OperationFailure__details']['keyPattern']}

        finally:
            return {"status": False, "error": "Unknown Error with the database"}

    @staticmethod
    async def update_record(id: str, user_data: dict) -> dict:
        """Class method to update the record in the database"""

        user = await user_collection.find_one({"_id": ObjectId(id)})
        if user:
            updated_user = await user_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": user_data}
            )
            if updated_user:
                return {"status": True, "message": "Data Updated Successfully!"}
            return {"status": False, "message": "There are some missmatch in the data field"}
        return {"status": False, "message": "id is not correct or not present in the database"}    

