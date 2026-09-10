import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba Ventilador")
    print("El ventilador se encenderá y apagará cada 3 segundos.")
    print("Presiona Ctrl+C para salir.\n")

    try:
        gpio_driver, devices = create_raspberry_hardware()

        fan = devices["fan"]

        while True:
            print("Ventilador: ENCENDIDO")
            fan.turn_on()
            time.sleep(3)

            print("Ventilador: APAGADO")
            fan.turn_off()
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if devices is not None:
            fan = devices.get("fan")

            if fan is not None:
                fan.turn_off()

        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()