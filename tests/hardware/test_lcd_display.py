import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.display.lcd_display import LCDDisplay


def test_lcd_configuration():
    lcd = LCDDisplay()

    assert lcd.columns == 16
    assert lcd.rows == 2
    assert lcd.line1 == ""
    assert lcd.line2 == ""


def test_show_message():
    lcd = LCDDisplay()

    lcd.show("Hola", "Sistema")

    assert lcd.line1 == "Hola"
    assert lcd.line2 == "Sistema"


def test_clear():
    lcd = LCDDisplay()

    lcd.show("Hola", "Sistema")
    lcd.clear()

    assert lcd.line1 == ""
    assert lcd.line2 == ""


def test_text_is_limited_to_columns():
    lcd = LCDDisplay(columns=16)

    lcd.show(
        "12345678901234567890",
        "abcdefghijklmnopqrst"
    )

    assert len(lcd.line1) == 16
    assert len(lcd.line2) == 16


def test_temperature_humidity_screen():
    lcd = LCDDisplay()

    lcd.show_temperature_humidity(
        temperature=25.5,
        humidity=60.0
    )

    assert lcd.line1 == "Temp: 25.5C"
    assert lcd.line2 == "Humedad: 60.0%"


def test_distance_screen():
    lcd = LCDDisplay()

    lcd.show_distance(25.4)

    assert lcd.line1 == "Distancia:"
    assert lcd.line2 == "25.4 cm"


def test_system_state_screen():
    lcd = LCDDisplay()

    lcd.show_system_state("NORMAL")

    assert lcd.line1 == "Estado:"
    assert lcd.line2 == "NORMAL"