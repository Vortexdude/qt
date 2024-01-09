from bson.objectid import ObjectId
from motor import motor_asyncio
import pymongo

host = "database"
MONGO_DB = "trasactions"
MONGO_USER = "admin"
MONGO_PASS = "admin"
port = 27017
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.Global_users  # <--- database name

user_collection = database.get_collection("user_collection")  #<--- collection name

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fname": user["fname"],
        "lname": user["lname"],
        "email": user["email"],
        "password": user["password"]
    }


# get all the user details
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    try:
        user = await user_collection.insert_one(user_data)
        new_user = await user_collection.find_one({"_id": user.inserted_id})
        return user_helper(new_user)
    except pymongo.errors.DuplicateKeyError:
        return {"error": "Duplicate Key"}


async def update_user_details(id: str, user_data: dict) -> dict:
    if len(user_data) < 1:
        return {"status": False, "message": "Please provide the data first"}
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": user_data}
        )
        if updated_user:
            return {"status": True, "message": "Data Updated Successfully!"}
        return {"status": False, "message": "There are some missmatch in the data field"}
    return {"status": False, "message": "id is not correct or not present in the database"}
