class GPIODriver:
    """
    Abstracción simple para controlar GPIO.

    En Raspberry Pi se le inyectará una librería GPIO real.
    En Windows podemos usar un objeto falso para pruebas.
    """

    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0

    def __init__(self, gpio_module):
        self.gpio = gpio_module

    def setup_output(self, pin):
        self.gpio.setup(pin, self.gpio.OUT)

    def setup_input(self, pin):
        self.gpio.setup(pin, self.gpio.IN)

    def write_high(self, pin):
        self.gpio.output(pin, self.gpio.HIGH)

    def write_low(self, pin):
        self.gpio.output(pin, self.gpio.LOW)

    def read(self, pin):
        return self.gpio.input(pin)

    def create_pwm(self, pin, frequency):
        return self.gpio.PWM(pin, frequency)

    def cleanup(self):
        self.gpio.cleanup()