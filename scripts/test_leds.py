import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba de LEDs")
    print("Se encenderán uno por uno.")
    print("Presiona Ctrl+C para salir.\n")

    led_names = [
        "normal_led",
        "warning_led",
        "emergency_led",
        "light_1",
        "light_2",
    ]

    try:
        gpio_driver, devices = create_raspberry_hardware()

        while True:
            for name in led_names:
                print(f"Encendiendo: {name}")

                for led_name in led_names:
                    devices[led_name].turn_off()

                devices[name].turn_on()
                time.sleep(1)

            print("Apagando todos los LEDs\n")

            for name in led_names:
                devices[name].turn_off()

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if devices is not None:
            for name in led_names:
                led = devices.get(name)

                if led is not None:
                    led.turn_off()

        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()