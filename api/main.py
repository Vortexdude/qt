from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from routes import users_route

app = FastAPI()

@app.get("/")
async def root():
    data = jsonable_encoder({"message": "Hello There!"})
    return JSONResponse(content = data)

app.include_router(users_route)
