import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.hardware.display.lcd_display import LCDDisplay
from src.hardware.display.display_controller import DisplayController


def create_controller():
    lcd = LCDDisplay()

    controller = DisplayController(lcd)

    return controller, lcd


def show_next(controller):
    controller.next_screen(
        temperature=25.5,
        humidity=60.0,
        gas_value=350,
        distance_cm=20.5,
        light_value=450,
        door_state="CERRADA",
        system_state="NORMAL",
    )


def test_initial_screen():
    controller, lcd = create_controller()

    assert controller.screen_index == 0


def test_temperature_humidity_screen():
    controller, lcd = create_controller()

    show_next(controller)

    assert lcd.line1 == "Temp: 25.5C"
    assert lcd.line2 == "Humedad: 60.0%"


def test_gas_screen():
    controller, lcd = create_controller()

    show_next(controller)
    show_next(controller)

    assert lcd.line1 == "Gas/Humo:"
    assert lcd.line2 == "350"


def test_distance_screen():
    controller, lcd = create_controller()

    for _ in range(3):
        show_next(controller)

    assert lcd.line1 == "Distancia:"
    assert lcd.line2 == "20.5 cm"


def test_complete_rotation_returns_to_first_screen():
    controller, lcd = create_controller()

    for _ in range(6):
        show_next(controller)

    assert controller.screen_index == 0

    show_next(controller)

    assert lcd.line1 == "Temp: 25.5C"
    assert lcd.line2 == "Humedad: 60.0%"