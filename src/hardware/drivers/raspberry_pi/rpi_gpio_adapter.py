def load_rpi_gpio():
    """
    Carga RPi.GPIO únicamente cuando el programa
    se ejecuta realmente en una Raspberry Pi.

    Esto evita que Windows necesite tener instalada
    la librería RPi.GPIO.
    """

    try:
        import RPi.GPIO as GPIO
    except ImportError as exc:
        raise RuntimeError(
            "RPi.GPIO no está disponible. "
            "Este módulo debe ejecutarse en una Raspberry Pi."
        ) from exc

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    return GPIO