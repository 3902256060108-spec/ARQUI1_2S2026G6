import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba HC-SR04")
    print("Presiona Ctrl+C para salir.\n")

    try:
        gpio_driver, devices = create_raspberry_hardware()

        ultrasonic = devices["ultrasonic"]

        while True:
            try:
                distance = ultrasonic.read_distance()

                print(
                    f"Distancia: {distance:.2f} cm"
                )

            except TimeoutError as exc:
                print(f"Error de lectura: {exc}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()