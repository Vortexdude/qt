from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def fetch_all_compnies():
    return {"compnies": []}

@router.get("/{global_key}")
async def fetch_single_compnie():
    return {"compnies": []}

@router.post("/")
async def create_company():
    return {"compnies": []}

@router.put("/{global_key}")
async def update_company():
    return {"compnies": []}
