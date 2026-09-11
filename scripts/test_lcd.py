import time

from src.hardware.config.driver_factory import create_raspberry_hardware


def main():
    gpio_driver = None
    devices = None

    print("Prueba LCD 16x2")
    print("Presiona Ctrl+C para salir.\n")

    try:
        gpio_driver, devices = create_raspberry_hardware()

        lcd = devices["lcd"]

        lcd.clear()
        lcd.write_line(0, "ARQUI1 G6")
        lcd.write_line(1, "LCD FUNCIONA")

        print("Mensaje enviado al LCD.")
        print("Esperando 5 segundos...")

        time.sleep(5)

        lcd.clear()

        lcd.write_line(0, "Prueba")
        lcd.write_line(1, "completada")

        time.sleep(3)

    except KeyboardInterrupt:
        print("\nPrueba interrumpida.")

    finally:
        if devices is not None:
            lcd = devices.get("lcd")

            if lcd is not None:
                lcd.clear()

        if gpio_driver is not None:
            gpio_driver.cleanup()

        print("Prueba finalizada.")


if __name__ == "__main__":
    main()