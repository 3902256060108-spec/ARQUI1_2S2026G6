import json

from src.hardware.mqtt import topics


class MQTTPublisher:
    """
    Publica datos del sistema mediante un cliente MQTT.

    El cliente se inyecta para poder probar esta clase
    sin conectarse a un broker real.
    """

    def __init__(self, client):
        self.client = client

    def _publish_json(self, topic, payload):
        message = json.dumps(payload)
        self.client.publish(topic, message)

    def publish_sensor_value(self, topic, value):
        self._publish_json(
            topic,
            {
                "valor": value,
            },
        )

    def publish_snapshot(self, snapshot):
        temperature = snapshot["temperature"]
        humidity = snapshot["humidity"]
        gas_alert = snapshot["gas_alert"]
        distance_cm = snapshot["distance_cm"]
        is_dark = snapshot["is_dark"]

        if temperature is not None:
            self.publish_sensor_value(
                topics.TEMPERATURE_TOPIC,
                temperature,
            )

        if humidity is not None:
            self.publish_sensor_value(
                topics.HUMIDITY_TOPIC,
                humidity,
            )

        if gas_alert is not None:
            self.publish_sensor_value(
                topics.GAS_TOPIC,
                gas_alert,
            )

        if distance_cm is not None:
            self.publish_sensor_value(
                topics.DISTANCE_TOPIC,
                distance_cm,
            )

        if is_dark is not None:
            self.publish_sensor_value(
                topics.LIGHT_TOPIC,
                is_dark,
            )

        self._publish_json(
            topics.GLOBAL_STATE_TOPIC,
            {
                "estado": snapshot["state"].value,
            },
        )

    def publish_door_state(self, state):
        self._publish_json(
            topics.DOOR_STATE_TOPIC,
            {
                "estado": state,
            },
        )

    def publish_lights_state(self, state):
        self._publish_json(
            topics.LIGHTS_STATE_TOPIC,
            {
                "estado": state,
            },
        )

    def publish_fan_state(self, state):
        self._publish_json(
            topics.FAN_STATE_TOPIC,
            {
                "estado": state,
            },
        )

    def publish_alarm_state(self, state):
        self._publish_json(
            topics.ALARM_STATE_TOPIC,
            {
                "estado": state,
            },
        )

    def publish_arm64_results(self, results):
        self._publish_json(
            topics.ARM64_RESULTS_TOPIC,
            results,
        )