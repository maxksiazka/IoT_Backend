from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client.client.write.point import Point
import os
from datetime import datetime
#pyright: basic
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

async def write_sensor_data(data):
    if not INFLUX_BUCKET:
        print("ERROR: Missing INFLUX_BUCKET environment variable!")
        return

    async with InfluxDBClientAsync.from_env_properties() as client:
        point = (
            Point("weather_data")
            .tag("device_id", data["device_id"])
            .field("temperature", float(data["temperature"]))
            .field("pressure", float(data["pressure"]))
            .field("altitude", float(data["altitude"]))
            .field("uptime_ms", int(data["uptime_ms"]))
        )
        esp_time_str: str = data.get("timestamp")
        try:
            dt = datetime.fromisoformat(esp_time_str.replace("Z", "+00:00"))
            if dt.year > 2000:
                point.time(dt)
            else:
                print(f"WARNING: Invalid timestamp '{esp_time_str}' - using server time.")
        except Exception as e:
            print(f"WARNING: Invalid timestamp '{esp_time_str}' - using server time. Error: {e}")

        write_api = client.write_api()
        await write_api.write(bucket=INFLUX_BUCKET, record=point)
