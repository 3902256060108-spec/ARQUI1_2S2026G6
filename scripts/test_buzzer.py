import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba Buzzer")
    print("El buzzer se encenderá y apagará cada segundo.")
    print("Presiona Ctrl+C para salir.\n")

    try:
        gpio_driver, devices = create_raspberry_hardware()

        buzzer = devices["buzzer"]

        while True:
            print("Buzzer: ENCENDIDO")
            buzzer.turn_on()
            time.sleep(1)

            print("Buzzer: APAGADO")
            buzzer.turn_off()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        if devices is not None:
            buzzer = devices.get("buzzer")

            if buzzer is not None:
                buzzer.turn_off()

        if gpio_driver is not None:
            gpio_driver.cleanup()


if __name__ == "__main__":
    main()