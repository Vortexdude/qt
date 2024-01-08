from bason.objectid import ObjectId
from motor import motor_asyncio

host = "database"
MONGO_DB = "trasactions"
MONGO_USER = "admin"
MONGO_PASS = "admin"

MONGO_DETAILS = "mongodb://database:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.transations

user_collection = database.get_collection("user_collection")

def user_helper(user) -> dict:
    return {
        "id": str(user["id"]),
        "fname": user["fname"],
        "lname": user["lname"],
        "email": user["email"],
        "password": user["password"]
    }


# get all the user details
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper[user])
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"id": user.inserted_id})
    return student_helper(new_user)
