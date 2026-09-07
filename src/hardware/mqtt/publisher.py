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
        self.publish_sensor_value(
            topics.TEMPERATURE_TOPIC,
            snapshot["temperature"],
        )

        self.publish_sensor_value(
            topics.HUMIDITY_TOPIC,
            snapshot["humidity"],
        )

        self.publish_sensor_value(
            topics.GAS_TOPIC,
            snapshot["gas_alert"],
        )

        self.publish_sensor_value(
            topics.DISTANCE_TOPIC,
            snapshot["distance_cm"],
        )

        self.publish_sensor_value(
            topics.LIGHT_TOPIC,
            snapshot["is_dark"],
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