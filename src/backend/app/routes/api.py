from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.backend.app.database.repository import repository
from src.backend.app.mqtt.client import mqtt_client

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/sensores")
def obtener_sensores():
    return repository.get_latest_sensor_readings()


@router.get("/estado")
def obtener_estado():
    return repository.get_latest_system_status()


@router.get("/actuadores")
def obtener_actuadores():
    return repository.get_latest_actuator_statuses()


@router.get("/sensores/historial")
def obtener_historial_sensores(limit: int = 20):
    return repository.get_sensor_history(limit)


@router.get("/eventos")
def obtener_eventos(limit: int = 20):
    return repository.get_event_history(limit)


@router.get("/arm64")
def obtener_arm64():
    return repository.get_latest_arm64_result()


@router.get("/comandos")
def obtener_comandos(limit: int = 20):
    return repository.get_command_history(limit)

class RemoteCommand(BaseModel):
    dispositivo: str
    accion: str


@router.post("/comandos")
def enviar_comando(comando: RemoteCommand):
    try:
        mqtt_client.publish_command(
            comando.dispositivo,
            comando.accion
        )

        return {
            "mensaje": "Comando enviado correctamente",
            "dispositivo": comando.dispositivo,
            "accion": comando.accion
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )