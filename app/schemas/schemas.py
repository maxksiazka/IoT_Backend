from pydantic import BaseModel
class SensorReading(BaseModel):
    device_id: str
    timestamp: str
    temperature: float
    pressure: float
    altitude: float
    uptime_ms: int
