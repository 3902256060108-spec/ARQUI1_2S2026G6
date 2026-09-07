import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba MQ-2")
    print("Presiona Ctrl+C para salir.\n")

    try:
        gpio_driver, devices = create_raspberry_hardware()

        gas_sensor = devices["gas_sensor"]

        while True:
            gas_alert = gas_sensor.is_alert()

            if gas_alert:
                print("GAS: ALERTA")
            else:
                print("GAS: OK")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()