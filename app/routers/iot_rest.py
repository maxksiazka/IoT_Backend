from fastapi import APIRouter,status,Request,HTTPException
from app.db.database import write_sensor_data
from app.schemas import SensorData
router = APIRouter()

@router.post("/data", status_code=status.HTTP_200_OK)
async def data_post(req: Request, sensor_data: SensorData):
    data_dict = sensor_data.model_dump()
    print(f"Received POST data: {data_dict}")
    req.app.state.latest_sensor_data[sensor_data.sensor_id] = data_dict
    await write_sensor_data(data_dict)
    print("written to InfluxDB")
    return {"status": "ok"}

@router.get("/live", status_code=status.HTTP_200_OK)
async def live_sensors(req: Request):
    return req.app.state.latest_sensor_data
