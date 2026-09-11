from enum import Enum


class SystemState(Enum):
    NORMAL = "NORMAL"
    WARNING = "ADVERTENCIA"
    EMERGENCY = "EMERGENCIA"


def determine_system_state(
    temperature,
    humidity,
    gas_alert,
    temp_max,
    humidity_min,
    humidity_max,
):
    # Gas siempre tiene prioridad máxima.
    if gas_alert:
        return SystemState.EMERGENCY

    # Si hay temperatura válida, se evalúa.
    if temperature is not None:
        if temperature > temp_max:
            return SystemState.WARNING

    # Si hay humedad válida, se evalúa.
    if humidity is not None:
        if humidity < humidity_min or humidity > humidity_max:
            return SystemState.WARNING

    # Si DHT no entrega datos, el resto del sistema
    # puede continuar funcionando.
    return SystemState.NORMAL