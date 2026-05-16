#pyright: basic
from fastapi import FastAPI, status
from .routers import iot_rest
from contextlib import asynccontextmanager
import aiomqtt
import asyncio

async def mqtt_subscriber():
    try:
        async with aiomqtt.Client("mqtt-broker",1883) as client:
            await client.subscribe("iot/esp32/tempsensors")
            async for message in client.messages:
                payload_str = message.payload.decode()
                print(f"Received MQTT message: {payload_str}")
                #db logic here
    except Exception as e:
        print(f"Error in MQTT subscriber: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    mqtt_task = asyncio.create_task(mqtt_subscriber())
    yield
    mqtt_task.cancel()
    print("Shutting down the application...")


app = FastAPI(title="IoT-Backend",lifespan=lifespan)
app.include_router(iot_rest.router,
                   prefix="/api/v1/iot"
                   )

@app.get("/api/v1/hello", status_code=status.HTTP_200_OK)
async def healthcheck():
    return {"status": "ok"}

