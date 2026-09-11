import os


MQTT_HOST = os.getenv(
    "MQTT_BROKER",
    "p2229e87.ala.eu-central-1.emqxsl.com",
)

MQTT_PORT = int(
    os.getenv(
        "MQTT_PORT",
        "8883",
    )
)

MQTT_KEEPALIVE = int(
    os.getenv(
        "MQTT_KEEPALIVE",
        "60",
    )
)

MQTT_USERNAME = os.getenv(
    "MQTT_USERNAME",
    "arqui_backend",
)

MQTT_PASSWORD = os.getenv(
    "MQTT_PASSWORD",
    "arqui2026",
)

MQTT_TLS = os.getenv(
    "MQTT_TLS",
    "true",
).lower() == "true"