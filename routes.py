from fastapi import APIRouter, status
from pydantic import BaseModel

# user namespace 
users_route = APIRouter()
@users_route.get("/users", status_code=status.HTTP_201_CREATED)
async def _users():
    return [{"username": "Rick"}, {"username": "Morty"}]
    # return user
