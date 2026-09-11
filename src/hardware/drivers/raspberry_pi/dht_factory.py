from src.hardware.config import pins
from src.hardware.drivers.raspberry_pi.dht_driver import RaspberryDHT


def create_dht_sensor(dht_module, board_module):
    """
    Crea el DHT11 físico.

    dht_module:
        Módulo adafruit_dht.

    board_module:
        Módulo board de CircuitPython.

    Ambos se inyectan para poder probar esta función
    desde Windows sin instalar librerías de Raspberry.
    """

    board_pin = getattr(
        board_module,
        f"D{pins.DHT_PIN}",
    )

    device = dht_module.DHT11(
        board_pin,
        use_pulseio=False,
    )

    return RaspberryDHT(
        pin=pins.DHT_PIN,
        dht_device=device,
    )