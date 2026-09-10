import os


MQTT_HOST = os.getenv(
    "MQTT_HOST",
    "localhost",
)

MQTT_PORT = int(
    os.getenv(
        "MQTT_PORT",
        "1883",
    )
)

MQTT_KEEPALIVE = int(
    os.getenv(
        "MQTT_KEEPALIVE",
        "60",
    )
)