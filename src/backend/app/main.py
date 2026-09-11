from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.backend.app.database.mongodb import mongodb
from src.backend.app.mqtt.client import mqtt_client
from src.backend.app.routes.api import router as api_router


app = FastAPI(
    title="ARQUI1_2S2026G6 Backend",
    description="Backend para Raspberry Pi, MQTT, MongoDB y Dashboard",
    version="1.0.0"
)

app.include_router(api_router)
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/dashboard",
    StaticFiles(
        directory=BASE_DIR / "web",
        html=True
    ),
    name="dashboard"
)


@app.on_event("startup")
def startup():
    mongodb.connect()
    print("MongoDB conectado correctamente")

    mqtt_client.connect()
    print("MQTT conectado correctamente")


@app.on_event("shutdown")
def shutdown():
    mqtt_client.disconnect()
    print("MQTT desconectado")

    mongodb.close()
    print("MongoDB desconectado")


@app.get("/")
def root():
    return {
        "proyecto": "ARQUI1_2S2026G6",
        "mensaje": "Backend funcionando correctamente"
    }