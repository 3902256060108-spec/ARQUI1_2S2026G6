import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba LDR")
    print("Presiona Ctrl+C para salir.\n")

    try:
        gpio_driver, devices = create_raspberry_hardware()

        light_sensor = devices["light_sensor"]

        while True:
            is_dark = light_sensor.is_dark()

            if is_dark:
                print("LUZ: OSCURO")
            else:
                print("LUZ: CLARO")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()