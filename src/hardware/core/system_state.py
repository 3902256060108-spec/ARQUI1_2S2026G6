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
    humidity_max
):
    """
    Determina el estado global del edificio según las
    lecturas obtenidas por los sensores.

    Prioridad:
    1. EMERGENCIA
    2. ADVERTENCIA
    3. NORMAL
    """

    # Gas o humo detectado tiene máxima prioridad.
    if gas_alert:
        return SystemState.EMERGENCY

    # Temperatura elevada.
    if temperature > temp_max:
        return SystemState.WARNING

    # Humedad fuera del rango permitido.
    if humidity < humidity_min or humidity > humidity_max:
        return SystemState.WARNING

    return SystemState.NORMAL