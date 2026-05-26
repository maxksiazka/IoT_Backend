# pyright: basic
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from .routers import iot_rest
from .db.database import write_sensor_data
from contextlib import asynccontextmanager
import aiomqtt
import asyncio
import json


async def mqtt_subscriber():
    try:
        async with aiomqtt.Client("mqtt-broker", 1883) as client:
            await client.subscribe("iot/esp32/tempsensors")
            async for message in client.messages:
                payload_str = message.payload.decode()
                data = json.loads(payload_str)
                print(f"Received MQTT message: {payload_str}")
                device_id = data.get("device_id", "unknown")
                app.state.latest_sensor_data[device_id] = data
                await write_sensor_data(data)
                print("written to InfluxDB")
    except Exception as e:
        print(f"Error in MQTT subscriber: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting...")
    app.state.latest_sensor_data = {}
    mqtt_task = asyncio.create_task(mqtt_subscriber())
    yield
    mqtt_task.cancel()
    print("Byebye")


app = FastAPI(title="IoT-Backend", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(iot_rest.router, prefix="/api/v1/iot")

@app.get("/api/v1/hello", status_code=status.HTTP_200_OK)
async def healthcheck():
    return {"status": "ok"}
