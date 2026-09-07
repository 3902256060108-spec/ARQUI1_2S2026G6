def load_dht_modules():
    """
    Carga las librerías necesarias para el DHT11.

    Estas librerías solamente estarán disponibles
    cuando el proyecto se ejecute en la Raspberry Pi.
    """

    try:
        import board
        import adafruit_dht

    except ImportError as exc:
        raise RuntimeError(
            "Las librerías del DHT11 no están disponibles. "
            "Instala las dependencias de requirements-rpi.txt "
            "en la Raspberry Pi."
        ) from exc

    return adafruit_dht, board