import time


class RaspberryLCD:
    """
    Driver para LCD 1602A compatible con HD44780
    usando interfaz paralela de 4 bits.
    """

    LCD_WIDTH = 16

    LCD_CHR = 1
    LCD_CMD = 0

    LINE_1 = 0x80
    LINE_2 = 0xC0

    ENABLE_PULSE = 0.0005
    ENABLE_DELAY = 0.0005

    def __init__(
        self,
        rs_pin,
        enable_pin,
        d4_pin,
        d5_pin,
        d6_pin,
        d7_pin,
        gpio_driver,
        sleep_provider=None,
    ):
        self.rs_pin = rs_pin
        self.enable_pin = enable_pin

        self.data_pins = [
            d4_pin,
            d5_pin,
            d6_pin,
            d7_pin,
        ]

        self.gpio = gpio_driver
        self._sleep = sleep_provider or time.sleep

        self._line1 = ""
        self._line2 = ""

        self.gpio.setup_output(self.rs_pin)
        self.gpio.setup_output(self.enable_pin)

        for pin in self.data_pins:
            self.gpio.setup_output(pin)

        self._set_all_low()

    @property
    def line1(self):
        return self._line1

    @property
    def line2(self):
        return self._line2

    def _set_all_low(self):
        self.gpio.write_low(self.rs_pin)
        self.gpio.write_low(self.enable_pin)

        for pin in self.data_pins:
            self.gpio.write_low(pin)

    def _pulse_enable(self):
        self._sleep(self.ENABLE_DELAY)

        self.gpio.write_high(self.enable_pin)
        self._sleep(self.ENABLE_PULSE)

        self.gpio.write_low(self.enable_pin)
        self._sleep(self.ENABLE_DELAY)

    def _write_nibble(self, nibble):
        for index, pin in enumerate(self.data_pins):
            if nibble & (1 << index):
                self.gpio.write_high(pin)
            else:
                self.gpio.write_low(pin)

        self._pulse_enable()

    def send_byte(self, value, mode):
        if mode == self.LCD_CHR:
            self.gpio.write_high(self.rs_pin)
        else:
            self.gpio.write_low(self.rs_pin)

        high_nibble = (value >> 4) & 0x0F
        low_nibble = value & 0x0F

        self._write_nibble(high_nibble)
        self._write_nibble(low_nibble)

    def initialize(self):
        """
        Secuencia básica de inicialización del HD44780
        en modo de 4 bits y display de 2 líneas.
        """

        self.send_byte(0x33, self.LCD_CMD)
        self.send_byte(0x32, self.LCD_CMD)
        self.send_byte(0x06, self.LCD_CMD)
        self.send_byte(0x0C, self.LCD_CMD)
        self.send_byte(0x28, self.LCD_CMD)
        self.send_byte(0x01, self.LCD_CMD)

        self._sleep(0.005)

    def _write_text(self, text):
        text = str(text)[:self.LCD_WIDTH]
        text = text.ljust(self.LCD_WIDTH)

        for character in text:
            self.send_byte(
                ord(character),
                self.LCD_CHR,
            )

    def show(self, line1="", line2=""):
        self._line1 = str(line1)[:self.LCD_WIDTH]
        self._line2 = str(line2)[:self.LCD_WIDTH]

        self.send_byte(
            self.LINE_1,
            self.LCD_CMD,
        )
        self._write_text(self._line1)

        self.send_byte(
            self.LINE_2,
            self.LCD_CMD,
        )
        self._write_text(self._line2)

    def clear(self):
        self.send_byte(
            0x01,
            self.LCD_CMD,
        )

        self._line1 = ""
        self._line2 = ""

        self._sleep(0.005)

    def show_temperature_humidity(self, temperature, humidity):
        temperature_text = (
            f"{temperature:.1f}C"
            if temperature is not None
            else "N/A"
        )

        humidity_text = (
            f"{humidity:.1f}%"
            if humidity is not None
            else "N/A"
        )

        self.show(
            f"Temp: {temperature_text}",
            f"Humedad: {humidity_text}",
        )

    def show_gas(self, value):
        self.show(
            "Gas/Humo:",
            str(value),
        )

    def show_distance(self, distance_cm):
        distance_text = (
            f"{distance_cm:.1f} cm"
            if distance_cm is not None
            else "N/A"
        )

        self.show(
            "Distancia:",
            distance_text,
        )

    def show_light(self, value):
        self.show(
            "Luz:",
            str(value),
        )

    def show_door(self, state):
        self.show(
            "Puerta:",
            str(state),
        )

    def show_system_state(self, state):
        self.show(
            "Estado:",
            str(state),
        )