from fastapi import FastAPI, status
from .routers import iot_rest

app = FastAPI(title="Iot test")
app.include_router(iot_rest.router,
                   prefix="/api/v1/iot"
                   )

@app.get("/api/v1/hello", status_code=status.HTTP_200_OK)
async def healthcheck():
    return {"status": "ok"}

