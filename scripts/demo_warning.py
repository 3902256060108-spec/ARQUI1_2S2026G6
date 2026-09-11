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
        print("=== DEMOSTRACION: ESTADO ADVERTENCIA ===")

        # Inicializar GPIO real
        gpio_module = load_rpi_gpio()
        gpio_driver = GPIODriver(gpio_module)

        # Crear dispositivos físicos reales
        devices = create_raspberry_drivers(gpio_driver)

        # Construir sistema usando el hardware real
        system = HardwareSystem(
            hardware=devices,
            sensors={},
        )

        # Valores que garantizan ADVERTENCIA
        temperature = TEMP_MAX + 5.0
        humidity = (HUMIDITY_MIN + HUMIDITY_MAX) / 2

        print(f"TEMP_MAX configurada: {TEMP_MAX}")
        print(f"Temperatura simulada: {temperature}")
        print(f"Humedad simulada: {humidity}")
        print()
        print("Forzando estado ADVERTENCIA...")
        print("Presione Ctrl+C para finalizar la demostracion.")
        print()

        while True:
            state = system.system_controller.update_state(
                temperature=temperature,
                humidity=humidity,
                gas_alert=False,
            )

            print(
                f"ESTADO={state.value} | "
                f"VENTILADOR={'ON' if devices['fan'].is_on else 'OFF'} | "
                f"LED_AMARILLO={'ON' if devices['warning_led'].is_on else 'OFF'} | "
                f"BUZZER={'ON' if devices['buzzer'].is_on else 'OFF'}"
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDemostracion finalizada por el usuario.")

    finally:
        print("Liberando recursos...")

        if devices is not None:
            try:
                devices["buzzer"].turn_off()
                devices["fan"].turn_off()

                devices["normal_led"].turn_off()
                devices["warning_led"].turn_off()
                devices["emergency_led"].turn_off()

                devices["light_1"].turn_off()
                devices["light_2"].turn_off()
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