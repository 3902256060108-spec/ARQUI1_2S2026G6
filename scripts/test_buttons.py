import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba de botones")
    print("Presiona cada botón para verificar su lectura.")
    print("Presiona Ctrl+C para salir.\n")

    buttons = {
        "door_button": devices["door_button"] if devices else None,
        "light_mode_button": devices["light_mode_button"] if devices else None,
        "silence_button": devices["silence_button"] if devices else None,
        "reset_button": devices["reset_button"] if devices else None,
    }

    previous_states = {}

    try:
        gpio_driver, devices = create_raspberry_hardware()

        buttons = {
            "door_button": devices["door_button"],
            "light_mode_button": devices["light_mode_button"],
            "silence_button": devices["silence_button"],
            "reset_button": devices["reset_button"],
        }

        previous_states = {
            name: False
            for name in buttons
        }

        while True:
            for name, button in buttons.items():
                current = button.is_pressed

                if current and not previous_states[name]:
                    print(f"PRESIONADO: {name}")

                previous_states[name] = current

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()