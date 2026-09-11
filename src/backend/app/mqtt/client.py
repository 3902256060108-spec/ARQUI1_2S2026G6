import json
import paho.mqtt.client as mqtt
from src.backend.app.database.mongodb import mongodb

from src.backend.app.config.settings import settings
from src.backend.app.database.repository import repository


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
        self.client.tls_set()

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.actuator_states = {}

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

            base = settings.MQTT_BASE_TOPIC

            sensor_topics = {
                f"{base}/sensores/temperatura": "temperatura",
                f"{base}/sensores/humedad": "humedad",
                f"{base}/sensores/gas": "gas",
                f"{base}/sensores/distancia": "distancia",
                f"{base}/sensores/luz": "luz",
            }

            if message.topic in sensor_topics:
                sensor = sensor_topics[message.topic]
                valor = payload["valor"]

                repository.insert_sensor_reading(
                    sensor,
                    valor
                )

                print(
                    f"Sensor guardado en MongoDB | "
                    f"sensor={sensor} | "
                    f"valor={valor}"
                )

            elif message.topic == f"{base}/estado/global":
                estado = payload["estado"]

                repository.insert_system_status(estado)

                descripcion = f"El estado global cambió a {estado}"

                repository.insert_event(
                    tipo="ESTADO_GLOBAL",
                    estado=estado,
                    descripcion=descripcion
                )

                print(f"Estado global guardado en MongoDB | estado={estado}")
                print(f"Evento guardado en MongoDB | tipo=ESTADO_GLOBAL | estado={estado}")

            elif message.topic.startswith(f"{base}/actuadores/"):
                dispositivo = message.topic.split("/")[-1]
                estado = payload["estado"]
                estados_validos = {
                    "puerta": {"ABIERTA", "CERRADA"},
                    "luces": {"ENCENDIDAS", "APAGADAS"},
                    "ventilador": {"ENCENDIDO", "APAGADO"},
                    "alarma": {"ACTIVA", "INACTIVA"},
                }

                if dispositivo not in estados_validos:
                    raise ValueError(
                        f"Dispositivo de actuador inválido: {dispositivo}"
                    )

                if estado not in estados_validos[dispositivo]:
                    raise ValueError(
                        f"Estado inválido para {dispositivo}: {estado}"
                    )

                self.actuator_states[dispositivo] = estado

                repository.insert_actuator_status(
                    dispositivo,
                    estado
                )

                print(
                    f"Estado de actuador confirmado | "
                    f"dispositivo={dispositivo} | "
                    f"estado={estado}"
                )

            elif message.topic == f"{base}/arm64/resultados":
                repository.insert_arm64_result(
                    payload["max"],
                    payload["min"],
                    payload["avg"],
                    payload["count"]
                )

                print(
                    "Resultado ARM64 guardado en MongoDB | "
                    f"max={payload['max']} | "
                    f"min={payload['min']} | "
                    f"avg={payload['avg']} | "
                    f"count={payload['count']}"
                )

        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            print(f"Error procesando mensaje MQTT: {error}")

        except (KeyError, TypeError, ValueError) as error:
            print(f"Payload MQTT inválido: {error}")

        except Exception as error:
            print(f"Error guardando mensaje MQTT: {error}")

    def connect(self):
        if not settings.MQTT_BROKER:
            raise ValueError("MQTT_BROKER no está configurado")
        if mongodb.database is None:
            mongodb.connect()
            print("Base de datos MongoDB conectada exitosamente.")
        self.client.connect(
            settings.MQTT_BROKER,
            settings.MQTT_PORT
        )

        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish_command(self, dispositivo: str, accion: str):
        dispositivos_validos = {
            "puerta": {"ABRIR", "CERRAR"},
            "luces": {"ENCENDER", "APAGAR"},
            "ventilador": {"ENCENDER", "APAGAR"},
            "alarma": {"ACTIVAR", "DESACTIVAR"},
        }

        if dispositivo not in dispositivos_validos:
            raise ValueError(
                f"Dispositivo inválido: {dispositivo}"
            )

        if accion not in dispositivos_validos[dispositivo]:
            raise ValueError(
                f"Acción inválida para {dispositivo}: {accion}"
            )

        payload = {
            "dispositivo": dispositivo,
            "accion": accion
        }

        topic = f"{settings.MQTT_BASE_TOPIC}/control/remoto"

        self.client.publish(
            topic,
            json.dumps(payload)
        )

        repository.insert_command(
            dispositivo,
            accion,
            "dashboard"
        )

        print(
            f"Comando remoto enviado | "
            f"dispositivo={dispositivo} | "
            f"accion={accion}"
        )

mqtt_client = MQTTClient()
