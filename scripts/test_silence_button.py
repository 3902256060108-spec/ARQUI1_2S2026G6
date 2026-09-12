import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import load_rpi_gpio
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.driver_factory import create_raspberry_drivers
from src.hardware.controls.buzzer_control import BuzzerControl


def main():
    gpio_driver = None
    devices = None

    try:
        gpio_module = load_rpi_gpio()
        gpio_driver = GPIODriver(gpio_module)
        devices = create_raspberry_drivers(gpio_driver)

        buzzer_control = BuzzerControl(
            button=devices["silence_button"],
            buzzer=devices["buzzer"],
        )

        print("=== PRUEBA BOTON SILENCIAR ===")
        print("El buzzer va a sonar.")
        print("Presiona el boton de SILENCIO BCM21.")
        print("Ctrl+C para salir.")
        print()

        buzzer_control.activate_alarm()

        while True:
            if devices["silence_button"].is_pressed:
                print("Boton SILENCIO detectado")
                buzzer_control.silence()

                print(
                    "Silenciado:",
                    buzzer_control.is_silenced,
                    "| Buzzer:",
                    devices["buzzer"].is_on,
                )

                time.sleep(0.3)

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if devices is not None:
            try:
                devices["buzzer"].turn_off()
            except Exception:
                pass

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("GPIO liberado.")


if __name__ == "__main__":
    main()