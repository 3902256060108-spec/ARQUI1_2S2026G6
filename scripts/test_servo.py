import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba Servo SG90")
    print("La puerta alternará entre CERRADA y ABIERTA.")
    print("Presiona Ctrl+C para salir.\n")

    try:
        gpio_driver, devices = create_raspberry_hardware()

        servo = devices["servo"]

        while True:
            print("Puerta: ABIERTA")
            servo.open_door()
            time.sleep(2)

            print("Puerta: CERRADA")
            servo.close_door()
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if devices is not None:
            servo = devices.get("servo")

            if servo is not None:
                servo.stop()

        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()