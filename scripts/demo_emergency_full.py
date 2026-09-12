import sys
import time
import select
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.hardware.core.system import HardwareSystem
from src.hardware.core.thresholds import (
    TEMP_MAX,
    HUMIDITY_MIN,
    HUMIDITY_MAX,
)

from src.hardware.drivers.raspberry_pi.rpi_gpio_adapter import load_rpi_gpio
from src.hardware.drivers.raspberry_pi.gpio_driver import GPIODriver
from src.hardware.drivers.raspberry_pi.driver_factory import (
    create_raspberry_drivers,
)

from src.hardware.controls.door_control import DoorControl
from src.hardware.controls.lighting_mode_control import LightingModeControl
from src.hardware.controls.reset_control import ResetControl
from src.hardware.controls.button_manager import ButtonManager
from src.hardware.controls.button_actions import ButtonActions


def main():
    gpio_driver = None
    devices = None

    try:
        # -------------------------------------------------
        # GPIO Y DISPOSITIVOS REALES
        # -------------------------------------------------
        gpio_module = load_rpi_gpio()
        gpio_driver = GPIODriver(gpio_module)
        devices = create_raspberry_drivers(gpio_driver)

        # -------------------------------------------------
        # SISTEMA COMPLETO
        # -------------------------------------------------
        system = HardwareSystem(
            hardware=devices,
            sensors={},
        )

        # -------------------------------------------------
        # CONTROLES FISICOS
        # -------------------------------------------------
        door_control = DoorControl(
            button=devices["door_button"],
            servo=devices["servo"],
        )

        lighting_mode_control = LightingModeControl(
            button=devices["light_mode_button"],
            lighting_controller=system.lighting_controller,
        )

        # El BuzzerControl ya fue creado dentro de HardwareSystem
        buzzer_control = system.buzzer_control

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

        # -------------------------------------------------
        # VALORES SIMULADOS SEGUROS
        # -------------------------------------------------
        temperature = TEMP_MAX - 1.0
        humidity = (HUMIDITY_MIN + HUMIDITY_MAX) / 2

        # Comienza simulando gas detectado
        gas_alert = True

        print()
        print("==============================================")
        print("   DEMO COMPLETA DE EMERGENCIA")
        print("==============================================")
        print()
        print("Se simulara una alerta de gas.")
        print()
        print("Botones fisicos disponibles:")
        print("  PUERTA     = BCM16")
        print("  LUZ/MODO   = BCM20")
        print("  SILENCIO   = BCM21")
        print("  RESET      = BCM12")
        print()
        print("Controles desde teclado:")
        print("  ENTER = eliminar peligro / gas")
        print("  E     = provocar una nueva emergencia")
        print("  Q     = salir")
        print()
        print("IMPORTANTE:")
        print("- RESET no debe eliminar una emergencia activa.")
        print("- SILENCIO solo debe apagar el buzzer.")
        print("- La puerta debe permanecer abierta en emergencia.")
        print()
        print("INICIANDO...")
        print()

        last_print = 0

        while True:

            # -------------------------------------------------
            # 1. ACTUALIZAR ESTADO GLOBAL
            # -------------------------------------------------
            state = system.update(
                temperature=temperature,
                humidity=humidity,
                gas_alert=gas_alert,
                distance_cm=100.0,
            )

            # -------------------------------------------------
            # 2. LEER BOTONES FISICOS
            # -------------------------------------------------
            pressed_buttons = button_manager.read_pressed()

            if pressed_buttons:
                results = button_actions.process(
                    pressed_buttons,
                    danger_active=gas_alert,
                )

                print()
                print("BOTON DETECTADO:", pressed_buttons)
                print("RESULTADO:", results)
                print()

            # -------------------------------------------------
            # 3. MOSTRAR ESTADO PERIODICAMENTE
            # -------------------------------------------------
            now = time.monotonic()

            if now - last_print >= 1.0:
                print(
                    f"ESTADO={state.value} | "
                    f"GAS={'PELIGRO' if gas_alert else 'OK'} | "
                    f"ROJO={'ON' if devices['emergency_led'].is_on else 'OFF'} | "
                    f"AMARILLO={'ON' if devices['warning_led'].is_on else 'OFF'} | "
                    f"VERDE={'ON' if devices['normal_led'].is_on else 'OFF'} | "
                    f"BUZZER={'ON' if devices['buzzer'].is_on else 'OFF'} | "
                    f"SILENCIADO={buzzer_control.is_silenced} | "
                    f"FAN={'ON' if devices['fan'].is_on else 'OFF'} | "
                    f"PUERTA={devices['servo'].door_state.value} | "
                    f"MODO_LUZ={system.lighting_controller.mode.value}"
                )

                last_print = now

            # -------------------------------------------------
            # 4. COMANDOS DE TECLADO
            # -------------------------------------------------
            readable, _, _ = select.select(
                [sys.stdin],
                [],
                [],
                0,
            )

            if readable:
                command = sys.stdin.readline().strip().upper()

                # ENTER = eliminar peligro
                if command == "":
                    gas_alert = False

                    print()
                    print("==============================================")
                    print("PELIGRO ELIMINADO")
                    print("gas_alert = False")
                    print("Ahora puede presionar RESET.")
                    print("==============================================")
                    print()

                # E = nueva emergencia
                elif command == "E":
                    gas_alert = True

                    print()
                    print("==============================================")
                    print("NUEVA EMERGENCIA SIMULADA")
                    print("gas_alert = True")
                    print("==============================================")
                    print()

                # Q = salir
                elif command == "Q":
                    print("Saliendo de la demostracion...")
                    break

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nDemo finalizada con Ctrl+C.")

    finally:
        print()
        print("Restaurando actuadores...")

        if devices is not None:

            try:
                devices["buzzer"].turn_off()
            except Exception:
                pass

            try:
                devices["fan"].turn_off()
            except Exception:
                pass

            try:
                devices["normal_led"].turn_off()
                devices["warning_led"].turn_off()
                devices["emergency_led"].turn_off()
            except Exception:
                pass

            try:
                devices["light_1"].turn_off()
                devices["light_2"].turn_off()
            except Exception:
                pass

            try:
                devices["servo"].close_door()
                devices["servo"].stop()
            except Exception:
                pass

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("GPIO liberado correctamente.")


if __name__ == "__main__":
    main()