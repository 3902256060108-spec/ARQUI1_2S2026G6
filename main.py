"""
Punto de entrada del sistema de hardware.

Este archivo está pensado para ejecutarse en la Raspberry Pi.
No debe ejecutarse todavía desde Windows.
"""

import time

from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import load_rpi_gpio
from src.hardware.drivers.raspberry_pi.driver_factory import (
    create_raspberry_drivers,
)


def main():
    print("Iniciando sistema de hardware...")

    gpio_module = load_rpi_gpio()
    gpio_driver = GPIODriver(gpio_module)

    devices = None

    try:
        devices = create_raspberry_drivers(
            gpio_driver
        )

        print("Drivers GPIO inicializados correctamente.")

        # Por ahora NO iniciamos el ciclo de sensores.
        # Se habilitará después de realizar las pruebas
        # físicas individuales en la Raspberry.
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSistema detenido por el usuario.")

    finally:
        if devices is not None:
            devices["servo"].stop()

        gpio_driver.cleanup()

        print("GPIO liberados correctamente.")


if __name__ == "__main__":
    main()