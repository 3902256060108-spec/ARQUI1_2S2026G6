import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.hardware.core.system import HardwareSystem
from src.hardware.core.thresholds import (
    TEMP_MAX,
    HUMIDITY_MIN,
    HUMIDITY_MAX,
)
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import load_rpi_gpio
from src.hardware.drivers.raspberry_pi.driver_factory import (
    create_raspberry_drivers,
)


def main():
    gpio_driver = None
    devices = None

    try:
        print("=== DEMOSTRACION: ESTADO EMERGENCIA ===")

        # Inicializar GPIO real
        gpio_module = load_rpi_gpio()
        gpio_driver = GPIODriver(gpio_module)

        # Crear dispositivos fisicos reales
        devices = create_raspberry_drivers(gpio_driver)

        # Construir el sistema usando hardware real
        system = HardwareSystem(
            hardware=devices,
            sensors={},
        )

        # Temperatura y humedad dentro del rango normal.
        # La emergencia sera provocada exclusivamente
        # simulando una alerta digital del sensor de gas.
        temperature = TEMP_MAX - 1.0
        humidity = (HUMIDITY_MIN + HUMIDITY_MAX) / 2

        print(f"Temperatura simulada: {temperature}")
        print(f"Humedad simulada: {humidity}")
        print("Alerta de gas simulada: TRUE")
        print()
        print("Forzando estado EMERGENCIA...")
        print("Presione Ctrl+C para finalizar la demostracion.")
        print()

        while True:
            state = system.system_controller.update_state(
                temperature=temperature,
                humidity=humidity,
                gas_alert=True,
            )

            print(
                f"ESTADO={state.value} | "
                f"LED_ROJO={'ON' if devices['emergency_led'].is_on else 'OFF'} | "
                f"VENTILADOR={'ON' if devices['fan'].is_on else 'OFF'} | "
                f"BUZZER={'ON' if devices['buzzer'].is_on else 'OFF'} | "
                f"PUERTA={devices['servo'].door_state.value}"
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDemostracion de emergencia finalizada.")

    finally:
        print("Restaurando actuadores y liberando recursos...")

        if devices is not None:
            try:
                devices["buzzer"].turn_off()
                devices["fan"].turn_off()

                devices["normal_led"].turn_off()
                devices["warning_led"].turn_off()
                devices["emergency_led"].turn_off()

                devices["light_1"].turn_off()
                devices["light_2"].turn_off()

                # Dejar la puerta en una posicion segura
                # antes de abandonar la demostracion.
                devices["servo"].close_door()

            except Exception:
                pass

            try:
                devices["servo"].stop()
            except Exception:
                pass

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("Recursos liberados correctamente.")


if __name__ == "__main__":
    main()