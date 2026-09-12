import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import load_rpi_gpio
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.driver_factory import create_raspberry_drivers
from src.hardware.controls.door_control import DoorControl


def main():
    gpio_driver = None
    devices = None

    try:
        gpio_module = load_rpi_gpio()
        gpio_driver = GPIODriver(gpio_module)
        devices = create_raspberry_drivers(gpio_driver)

        door_control = DoorControl(
            button=devices["door_button"],
            servo=devices["servo"],
        )

        print("=== PRUEBA BOTON DE PUERTA ===")
        print("Boton BCM16")
        print("Presiona una vez para cambiar el estado de la puerta.")
        print("Ctrl+C para salir.")
        print()

        previous_pressed = False

        while True:
            current_pressed = devices["door_button"].is_pressed

            if current_pressed and not previous_pressed:
                result = door_control.handle_press()

                print(
                    "Boton detectado | "
                    f"Estado puerta: {devices['servo'].door_state.value}"
                )

            previous_pressed = current_pressed

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if devices is not None:
            try:
                devices["servo"].stop()
            except Exception:
                pass

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("GPIO liberado.")


if __name__ == "__main__":
    main()