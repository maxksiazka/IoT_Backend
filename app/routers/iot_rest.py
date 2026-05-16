from fastapi import APIRouter,status,Request
from app.db.database import write_sensor_data
router = APIRouter()
#pyright: basic

@router.post("/data", status_code=status.HTTP_200_OK)
async def data_post(req: Request):
    body = await req.json()
    print(f"Received POST data: {body}")
    await write_sensor_data(body)
    print("written to InfluxDB")
    return {"status": "ok"}
