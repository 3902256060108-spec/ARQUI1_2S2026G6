from src.hardware.config.hardware_setup import create_hardware
from src.hardware.config.sensor_setup import create_sensors

from src.hardware.core.system_controller import SystemController
from src.hardware.core.door_controller import DoorController
from src.hardware.core.lighting_controller import LightingController

from src.hardware.controls.door_control import DoorControl
from src.hardware.controls.lighting_mode_control import LightingModeControl
from src.hardware.controls.buzzer_control import BuzzerControl
from src.hardware.controls.reset_control import ResetControl

from src.hardware.display.lcd_display import LCDDisplay
from src.hardware.display.display_controller import DisplayController

from src.hardware.core.system_state import SystemState
from src.hardware.core.thresholds import (
    TEMP_MAX,
    HUMIDITY_MIN,
    HUMIDITY_MAX,
    DISTANCE_THRESHOLD,
    DOOR_OPEN_TIME,
    LIGHT_THRESHOLD,
)


class HardwareSystem:
    """
    Ensambla todos los componentes lógicos del sistema.
    """
    def __init__(
        self,
        hardware=None,
        sensors=None,
    ):
        self.hardware = (
            hardware
            if hardware is not None
            else create_hardware()
        )

        self.sensors = (
            sensors
            if sensors is not None
            else create_sensors()
        )

        if "lcd" in self.hardware:
            self.lcd = self.hardware["lcd"]
        else:
            self.lcd = LCDDisplay()

        self.system_controller = SystemController(
            normal_led=self.hardware["normal_led"],
            warning_led=self.hardware["warning_led"],
            emergency_led=self.hardware["emergency_led"],
            buzzer=self.hardware["buzzer"],
            fan=self.hardware["fan"],
            servo=self.hardware["servo"],
            temp_max=TEMP_MAX,
            humidity_min=HUMIDITY_MIN,
            humidity_max=HUMIDITY_MAX,
        )

        self.door_controller = DoorController(
            servo=self.hardware["servo"],
            distance_threshold=DISTANCE_THRESHOLD,
        )

        self.lighting_controller = LightingController(
            [
                self.hardware["light_1"],
                self.hardware["light_2"],
            ],
            light_threshold=LIGHT_THRESHOLD,
        )

        self.display_controller = DisplayController(
            self.lcd
        )

    def update(
        self,
        temperature,
        humidity,
        gas_alert,
        distance_cm,
        light_value=None,
    ):
        """
        Actualiza el sistema completo a partir de
        una lectura de sensores.
        """

        # 1. Estado global
        state = self.system_controller.update_state(
            temperature=temperature,
            humidity=humidity,
            gas_alert=gas_alert,
        )

        # 2. Control de puerta
        if state == SystemState.EMERGENCY:
            self.hardware["servo"].open_door()
        else:
            self.door_controller.update(
                distance_cm=distance_cm
            )

        # 3. Iluminación automática
        if light_value is not None:
            self.lighting_controller.update_automatic(
                light_value=light_value
            )

        return state