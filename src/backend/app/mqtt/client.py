import json

import paho.mqtt.client as mqtt

from src.backend.app.config.settings import settings


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="ARQUI1_2S2026G6-backend"
        )

        self.client.username_pw_set(
            settings.MQTT_USERNAME,
            settings.MQTT_PASSWORD
        )

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        print("MQTT conectado")

        base = settings.MQTT_BASE_TOPIC

        topics = [
            f"{base}/sensores/temperatura",
            f"{base}/sensores/humedad",
            f"{base}/sensores/gas",
            f"{base}/sensores/distancia",
            f"{base}/sensores/luz",
            f"{base}/estado/global",
            f"{base}/actuadores/+",
            f"{base}/arm64/resultados",
        ]

        for topic in topics:
            client.subscribe(topic)
            print(f"Suscrito a: {topic}")

    def _on_message(self, client, userdata, message):
        try:
            payload = json.loads(
                message.payload.decode("utf-8")
            )

            print(
                f"MQTT recibido | "
                f"topic={message.topic} | "
                f"payload={payload}"
            )

        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            print(f"Error procesando mensaje MQTT: {error}")

    def connect(self):
        if not settings.MQTT_BROKER:
            raise ValueError("MQTT_BROKER no está configurado")

        self.client.connect(
            settings.MQTT_BROKER,
            settings.MQTT_PORT
        )

        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish_command(
        self,
        dispositivo: str,
        accion: str
    ):
        payload = {
            "dispositivo": dispositivo,
            "accion": accion
        }

        topic = f"{settings.MQTT_BASE_TOPIC}/control/remoto"

        self.client.publish(
            topic,
            json.dumps(payload)
        )


mqtt_client = MQTTClient()