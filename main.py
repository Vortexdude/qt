from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    data = jsonable_encoder({"message": "Hello There!"})
    return JSONResponse(content = data)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
