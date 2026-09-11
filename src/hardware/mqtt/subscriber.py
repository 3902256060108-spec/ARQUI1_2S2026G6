import json
from src.hardware.mqtt import topics


class MQTTSubscriber:
    """
    Recibe y procesa comandos remotos enviados
    mediante MQTT.

    El cliente MQTT se inyecta para permitir pruebas
    sin un broker real.
    """

    VALID_DEVICES = {
        "puerta",
        "luces",
        "ventilador",
        "alarma",
    }

    def __init__(
        self,
        client,
        servo,
        lighting_controller,
        fan,
        buzzer_control,
    ):
        self.client = client
        self.servo = servo
        self.lighting_controller = lighting_controller
        self.fan = fan
        self.buzzer_control = buzzer_control

    def subscribe(self):
        self.client.subscribe(
            topics.REMOTE_CONTROL_TOPIC
        )

    def process_payload(self, payload):
        """
        Procesa un comando JSON recibido del dashboard.
        """

        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")

        data = json.loads(payload)

        device = data.get("dispositivo")
        action = data.get("accion")

        if device not in self.VALID_DEVICES:
            raise ValueError(
                f"Dispositivo MQTT no válido: {device}"
            )

        if not action:
            raise ValueError(
                "El comando MQTT no contiene una acción."
            )

        if device == "puerta":
            return self._control_door(action)

        if device == "luces":
            return self._control_lights(action)

        if device == "ventilador":
            return self._control_fan(action)

        if device == "alarma":
            return self._control_alarm(action)

    def _control_door(self, action):
        if action == "ABRIR":
            self.servo.open_door()
            return "ABIERTA"

        if action == "CERRAR":
            self.servo.close_door()
            return "CERRADA"

        raise ValueError(
            f"Acción de puerta no válida: {action}"
        )

    def _control_lights(self, action):
        if action == "ENCENDER":
            self.lighting_controller.set_manual_state(
                True
            )
            return "ENCENDIDAS"

        if action == "APAGAR":
            self.lighting_controller.set_manual_state(
                False
            )
            return "APAGADAS"

        raise ValueError(
            f"Acción de luces no válida: {action}"
        )

    def _control_fan(self, action):
        if action == "ENCENDER":
            self.fan.turn_on()
            return "ENCENDIDO"

        if action == "APAGAR":
            self.fan.turn_off()
            return "APAGADO"

        raise ValueError(
            f"Acción de ventilador no válida: {action}"
        )

    def _control_alarm(self, action):
        if action == "DESACTIVAR":
            self.buzzer_control.silence()
            return "INACTIVA"

        if action == "ACTIVAR":
            self.buzzer_control.reset_silence()
            self.buzzer_control.activate_alarm()
            return "ACTIVA"

        raise ValueError(
            f"Acción de alarma no válida: {action}"
        )