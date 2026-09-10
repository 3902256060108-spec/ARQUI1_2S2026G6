"""
Punto de entrada del sistema de hardware.

Este archivo está diseñado para ejecutarse
directamente en la Raspberry Pi 4.
"""

import time
from src.hardware.core.system import HardwareSystem
from src.hardware.core.runtime import HardwareRuntime
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.controls.button_manager import ButtonManager
from src.hardware.controls.button_actions import ButtonActions
from src.hardware.controls.door_control import DoorControl
from src.hardware.controls.lighting_mode_control import LightingModeControl
from src.hardware.controls.buzzer_control import BuzzerControl
from src.hardware.controls.reset_control import ResetControl
from src.hardware.mqtt.mqtt_adapter import (
    load_mqtt_module,
)
from src.hardware.mqtt.mqtt_client import (
    RaspberryMQTTClient,
)
from src.hardware.mqtt.publisher import (
    MQTTPublisher,
)
from src.hardware.mqtt.subscriber import (
    MQTTSubscriber,
)
from src.hardware.mqtt.remote_control import (
    RemoteControlHandler,
)
from src.hardware.mqtt.config import (
    MQTT_HOST,
    MQTT_PORT,
    MQTT_KEEPALIVE,
)
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
    mqtt_client = None
    mqtt_publisher = None

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

        door_control = DoorControl(
            button=devices["door_button"],
            servo=devices["servo"],
        )

        lighting_mode_control = LightingModeControl(
            button=devices["light_mode_button"],
            lighting_controller=system.lighting_controller,
        )

        buzzer_control = system.buzzer_control

        # ------------------------------------------
        # MQTT
        # ------------------------------------------
        try:
            mqtt_module = load_mqtt_module()

            mqtt_client = RaspberryMQTTClient(
                mqtt_module=mqtt_module,
                host=MQTT_HOST,
                port=MQTT_PORT,
                keepalive=MQTT_KEEPALIVE,
            )

            mqtt_publisher = MQTTPublisher(
                client=mqtt_client,
            )

            mqtt_subscriber = MQTTSubscriber(
                client=mqtt_client,
                servo=devices["servo"],
                lighting_controller=system.lighting_controller,
                fan=devices["fan"],
                buzzer_control=buzzer_control,
            )

            remote_control = RemoteControlHandler(
                subscriber=mqtt_subscriber,
                publisher=mqtt_publisher,
            )

            mqtt_client.set_message_handler(
                remote_control.process
            )

            mqtt_client.connect()
            mqtt_subscriber.subscribe()
            mqtt_client.start()

            print(
                f"MQTT conectado a "
                f"{MQTT_HOST}:{MQTT_PORT}"
            )

        except Exception as exc:
            print(
                "MQTT no disponible. "
                "El sistema continuará funcionando "
                f"localmente: {exc}"
            )

            mqtt_client = None
            mqtt_publisher = None

        reset_control = ResetControl(
            button=devices["reset_button"],
            buzzer_control=buzzer_control,
        )

        button_manager = ButtonManager(
            door_button=devices["door_button"],
            light_mode_button=devices["light_mode_button"],
            silence_button=devices["silence_button"],
            reset_button=devices["reset_button"],
        )

        button_actions = ButtonActions(
            door_control=door_control,
            lighting_mode_control=lighting_mode_control,
            buzzer_control=buzzer_control,
            reset_control=reset_control,
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

                if mqtt_publisher is not None:
                    try:
                        mqtt_publisher.publish_snapshot(
                            snapshot
                        )
                    except Exception as exc:
                        print(
                            f"Error publicando MQTT: {exc}"
                        )

                pressed_buttons = button_manager.read_pressed()
                danger_active = (
                    snapshot["state"].value == "EMERGENCIA"
                )

                button_results = button_actions.process(
                    pressed_buttons,
                    danger_active=danger_active,
                )

                if button_results:
                    print(
                        "Acciones de botones:",
                        button_results,
                    )

                arm64_ready = temperature_arm64.add_temperature(
                    snapshot["temperature"]
                )

                if arm64_ready:
                    try:
                        arm64_output = (
                            temperature_arm64.process_collected()
                        )

                        print(
                            "Resultados ARM64:",
                            arm64_output["results"],
                        )

                        if mqtt_publisher is not None:
                            try:
                                mqtt_publisher.publish_arm64_results(
                                    arm64_output["results"]
                                )
                            except Exception as exc:
                                print(
                                    f"Error publicando resultados ARM64 "
                                    f"por MQTT: {exc}"
                                )

                    except (
                        FileNotFoundError,
                        RuntimeError,
                        ValueError,
                    ) as exc:
                        print(
                            f"Error ejecutando ARM64: {exc}"
                        )

                temperature_text = (
                    f"{snapshot['temperature']:.1f}C"
                    if snapshot["temperature"] is not None
                    else "N/A"
                )

                humidity_text = (
                    f"{snapshot['humidity']:.1f}%"
                    if snapshot["humidity"] is not None
                    else "N/A"
                )

                distance_text = (
                    f"{snapshot['distance_cm']:.1f}cm"
                    if snapshot["distance_cm"] is not None
                    else "N/A"
                )

                print(
                    f"T={temperature_text} | "
                    f"H={humidity_text} | "
                    f"GAS={snapshot['gas_alert']} | "
                    f"OSCURO={snapshot['is_dark']} | "
                    f"DIST={distance_text} | "
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

        if mqtt_client is not None:
            try:
                mqtt_client.stop()
                mqtt_client.disconnect()
            except Exception:
                pass

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("Recursos liberados correctamente.")


if __name__ == "__main__":
    main()