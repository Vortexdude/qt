from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.server.routes.users import router as UserRouter

app = FastAPI()
app.include_router(UserRouter ,tags=["Users"], prefix="/user")

@app.get("/", tags=["root"])
async def read_root():
    data = jsonable_encoder({"message": "Hello There!"})
    return JSONResponse(content = data)


# addding the users route
