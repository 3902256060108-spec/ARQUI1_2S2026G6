"""
Punto de entrada del sistema de hardware.

Este archivo está diseñado para ejecutarse
directamente en la Raspberry Pi 4.
"""

import time
from src.hardware.core.system import HardwareSystem
from src.hardware.core.runtime import HardwareRuntime
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import (
    load_rpi_gpio,
)
from src.hardware.drivers.raspberry_pi.driver_factory import (
    create_raspberry_drivers,
)
from src.hardware.drivers.raspberry_pi.dht_adapter import (
    load_dht_modules,
)
from src.hardware.drivers.raspberry_pi.dht_factory import (
    create_dht_sensor,
)
from src.hardware.integration.temperature_arm64 import (
    TemperatureARM64,
)


def main():
    print("Iniciando sistema de hardware...")

    gpio_driver = None
    devices = None
    dht_sensor = None

    try:
        # ------------------------------------------
        # 1. Inicializar GPIO
        # ------------------------------------------
        gpio_module = load_rpi_gpio()
        gpio_driver = GPIODriver(gpio_module)

        print("GPIO inicializado correctamente.")

        # ------------------------------------------
        # 2. Crear dispositivos GPIO
        # ------------------------------------------
        devices = create_raspberry_drivers(
            gpio_driver
        )

        print("Drivers GPIO inicializados correctamente.")

        # ------------------------------------------
        # 3. Inicializar LCD
        # ------------------------------------------
        devices["lcd"].initialize()

        devices["lcd"].show(
            "Smart Home",
            "Iniciando...",
        )

        print("LCD inicializado correctamente.")

        # ------------------------------------------
        # 4. Inicializar DHT11
        # ------------------------------------------
        dht_module, board_module = load_dht_modules()

        dht_sensor = create_dht_sensor(
            dht_module,
            board_module,
        )

        # ------------------------------------------
        # 5. Construir sistema con hardware real
        # ------------------------------------------
        sensors = {
            "dht": dht_sensor,
            "gas": devices["gas_sensor"],
            "light": devices["light_sensor"],
            "ultrasonic": devices["ultrasonic"],
        }

        system = HardwareSystem(
            hardware=devices,
            sensors=sensors,
        )

        runtime = HardwareRuntime(
            system=system,
            dht_sensor=dht_sensor,
            gas_sensor=devices["gas_sensor"],
            light_sensor=devices["light_sensor"],
            ultrasonic_sensor=devices["ultrasonic"],
        )

        temperature_arm64 = TemperatureARM64(
            dht_sensor=dht_sensor,
            sample_count=20,
        )

        print("Sistema lógico conectado al hardware.")

        print("DHT11 inicializado correctamente.")

        # ------------------------------------------
        # 5. Sistema listo
        # ------------------------------------------
        devices["lcd"].show(
            "Sistema listo",
            "Esperando...",
        )

        print("Hardware listo.")

        # Por ahora mantenemos vivo el programa.
        # En el siguiente paso conectaremos aquí
        # HardwareRuntime.
        # ------------------------------------------
        # 6. Ciclo principal
        # ------------------------------------------
        while True:
            try:
                snapshot = runtime.run_once()

                print(
                    f"T={snapshot['temperature']:.1f}C | "
                    f"H={snapshot['humidity']:.1f}% | "
                    f"GAS={snapshot['gas_alert']} | "
                    f"OSCURO={snapshot['is_dark']} | "
                    f"DIST={snapshot['distance_cm']:.1f}cm | "
                    f"ESTADO={snapshot['state'].value}"
                )

            except (RuntimeError, TimeoutError) as exc:
                print(
                    f"Error temporal de sensor: {exc}"
                )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSistema detenido por el usuario.")

    finally:
        print("Liberando recursos...")

        if devices is not None:
            try:
                devices["lcd"].clear()
            except Exception:
                pass

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

        if dht_sensor is not None:
            device = getattr(
                dht_sensor,
                "device",
                None,
            )

            if device is not None:
                exit_method = getattr(
                    device,
                    "exit",
                    None,
                )

                if callable(exit_method):
                    exit_method()

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("Recursos liberados correctamente.")


if __name__ == "__main__":
    main()