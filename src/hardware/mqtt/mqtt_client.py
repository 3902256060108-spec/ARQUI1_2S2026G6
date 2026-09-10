class RaspberryMQTTClient:
    """
    Administra la conexión MQTT utilizada por
    el sistema de hardware de la Raspberry Pi.
    """

    def __init__(
        self,
        mqtt_module,
        host,
        port=1883,
        keepalive=60,
    ):
        self.host = host
        self.port = port
        self.keepalive = keepalive

        self.client = mqtt_module.Client()

        self._message_handler = None

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def set_message_handler(self, handler):
        self._message_handler = handler

    def connect(self):
        self.client.connect(
            self.host,
            self.port,
            self.keepalive,
        )

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()

    def publish(self, topic, payload):
        return self.client.publish(
            topic,
            payload,
        )

    def subscribe(self, topic):
        return self.client.subscribe(topic)

    def _on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties=None,
    ):
        """
        Callback ejecutado cuando se establece
        la conexión con el broker.
        """
        return None

    def _on_message(
        self,
        client,
        userdata,
        message,
    ):
        if self._message_handler is None:
            return

        self._message_handler(
            message.payload
        )