import time

from src.hardware.config.dht_factory import create_dht_sensor


def main():
    sensor = create_dht_sensor()

    print("Prueba DHT11")
    print("Presiona Ctrl+C para salir.\n")

    try:
        while True:
            try:
                reading = sensor.read()

                temperature = reading["temperature"]
                humidity = reading["humidity"]

                print(
                    f"Temperatura: {temperature:.1f} °C | "
                    f"Humedad: {humidity:.1f} %"
                )

            except RuntimeError as exc:
                print(f"Lectura inválida: {exc}")

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nPrueba finalizada.")

    finally:
        device = getattr(sensor, "device", None)

        if device is not None and hasattr(device, "exit"):
            device.exit()


if __name__ == "__main__":
    main()