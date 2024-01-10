from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.server.routes.users import router as UserRouter
from api.server.routes.compnies import router as CompanyRouter
from api.server.routes.netflix import router as NetflixData
# from api.server.routes.auth import router as AuthRouter

app = FastAPI()
# app.include_router(AuthRouter ,tags=["Authentication"], prefix="/auth")
app.include_router(UserRouter ,tags=["Users"], prefix="/user")
app.include_router(CompanyRouter ,tags=["Companies"], prefix="/company")
app.include_router(NetflixData ,tags=["NTFlix"], prefix="/netflix")

@app.get("/", tags=["root"])
async def read_root():
    data = jsonable_encoder({"message": "Hello There!"})
    return JSONResponse(content = data)
