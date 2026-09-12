import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import load_rpi_gpio
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.driver_factory import create_raspberry_drivers
from src.hardware.core.lighting_controller import LightingController
from src.hardware.controls.lighting_mode_control import LightingModeControl


def main():
    gpio_driver = None
    devices = None

    try:
        gpio_driver = GPIODriver(load_rpi_gpio())
        devices = create_raspberry_drivers(gpio_driver)

        controller = LightingController(
            [
                devices["light_1"],
                devices["light_2"],
            ],
            light_threshold=500,
        )

        mode_control = LightingModeControl(
            button=devices["light_mode_button"],
            lighting_controller=controller,
        )

        previous = False

        print("=== PRUEBA BOTON MODO DE LUZ ===")
        print("BCM20")
        print("Modo inicial:", controller.mode.value)
        print("Presiona el boton UNA vez.")
        print("Ctrl+C para salir.")
        print()

        while True:
            current = devices["light_mode_button"].is_pressed

            if current and not previous:
                new_mode = mode_control.handle_press()
                print("PULSACION DETECTADA ->", new_mode.value)

            previous = current
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nPrueba terminada.")

    finally:
        if devices is not None:
            devices["light_1"].turn_off()
            devices["light_2"].turn_off()

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("GPIO liberado.")


if __name__ == "__main__":
    main()