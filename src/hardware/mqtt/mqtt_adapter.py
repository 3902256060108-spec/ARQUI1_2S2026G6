def load_mqtt_module():
    """
    Importa paho-mqtt solamente cuando se ejecuta
    el sistema real.
    """

    try:
        import paho.mqtt.client as mqtt
    except ImportError as exc:
        raise RuntimeError(
            "paho-mqtt no está instalado. "
            "Instala requirements-rpi.txt."
        ) from exc

    return mqtt