import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    PROJECT_ID: str = os.getenv(
        "PROJECT_ID",
        "ARQUI1_2S2026G6"
    )

    MQTT_BASE_TOPIC: str = os.getenv(
        "MQTT_BASE_TOPIC",
        "ARQUI1_2S2026G6/edificio"
    )

    MQTT_BROKER: str = os.getenv(
        "MQTT_BROKER",
        ""
    )

    MQTT_PORT: int = int(os.getenv(
        "MQTT_PORT",
        "1883"
    ))

    MQTT_USERNAME: str = os.getenv(
        "MQTT_USERNAME",
        ""
    )

    MQTT_PASSWORD: str = os.getenv(
        "MQTT_PASSWORD",
        ""
    )

    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        ""
    )

    MONGODB_DATABASE: str = os.getenv(
        "MONGODB_DATABASE",
        "ARQUI1_2S2026G6"
    )


settings = Settings()