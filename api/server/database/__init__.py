from motor import motor_asyncio

host = "database"
MONGO_DB = "trasactions"
MONGO_USER = "admin"
MONGO_PASS = "admin"
port = 27017
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db = client.Global_users  # <--- database name

