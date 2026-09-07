class RaspberryGasSensor:
    """
    Driver para módulo MQ-2 usando la salida digital DO.

    Retorna un valor booleano indicando si existe
    una condición de alarma de gas/humo.

    La sensibilidad se calibrará físicamente mediante
    el potenciómetro del módulo.
    """

    def __init__(self, pin, gpio_driver, active_low=True):
        self.pin = pin
        self.gpio = gpio_driver
        self.active_low = active_low

        self.gpio.setup_input(self.pin)

    def read(self):
        """
        Retorna True cuando existe una alerta de gas/humo
        y False cuando no existe alerta.
        """

        value = self.gpio.read(self.pin)

        if self.active_low:
            return value == self.gpio.LOW

        return value == self.gpio.HIGH

    def is_alert(self):
        return self.read()