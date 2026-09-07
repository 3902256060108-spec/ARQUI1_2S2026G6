class RemoteControlHandler:
    """
    Procesa comandos MQTT remotos y publica
    la confirmación del estado del actuador.
    """

    def __init__(self, subscriber, publisher):
        self.subscriber = subscriber
        self.publisher = publisher

    def process(self, payload):
        result = self.subscriber.process_payload(
            payload
        )

        device = self._get_device(payload)

        if device == "puerta":
            self.publisher.publish_door_state(
                result
            )

        elif device == "luces":
            self.publisher.publish_lights_state(
                result
            )

        elif device == "ventilador":
            self.publisher.publish_fan_state(
                result
            )

        elif device == "alarma":
            self.publisher.publish_alarm_state(
                result
            )

        return result

    def _get_device(self, payload):
        import json

        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")

        data = json.loads(payload)

        return data["dispositivo"]