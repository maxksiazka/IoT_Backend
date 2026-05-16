from fastapi import APIRouter,status,Request
router = APIRouter()

db_for_real= []

@router.get("/data",status_code=status.HTTP_200_OK)
async def data_get(req: Request):
    return {"status": "ok", "message":str(db_for_real)}

@router.post("/data", status_code=status.HTTP_200_OK)
async def data_post(req: Request):
    body = await req.json()
    print(body)
    db_for_real.append(body)
    return {"status": "ok"}
