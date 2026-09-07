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

    def __init__(self):
        # --------------------------------------------------
        # Hardware base
        # --------------------------------------------------
        self.hardware = create_hardware()
        self.sensors = create_sensors()

        # --------------------------------------------------
        # Control global
        # --------------------------------------------------
        self.system_controller = SystemController(
            normal_led=self.hardware["normal_led"],
            warning_led=self.hardware["warning_led"],
            emergency_led=self.hardware["emergency_led"],
            buzzer=self.hardware["buzzer"],
            servo=self.hardware["servo"],
            fan=self.hardware["fan"],
            temp_max=TEMP_MAX,
            humidity_min=HUMIDITY_MIN,
            humidity_max=HUMIDITY_MAX,
        )

        # --------------------------------------------------
        # Puerta automática
        # --------------------------------------------------
        self.door_controller = DoorController(
            servo=self.hardware["servo"],
            distance_threshold=DISTANCE_THRESHOLD,
            open_time=DOOR_OPEN_TIME,
        )

        # --------------------------------------------------
        # Iluminación
        # --------------------------------------------------
        self.lighting_controller = LightingController(
            lights=[
                self.hardware["light_1"],
                self.hardware["light_2"],
            ],
            light_threshold=LIGHT_THRESHOLD,
        )

        # --------------------------------------------------
        # Controles físicos
        # --------------------------------------------------
        self.door_control = DoorControl(
            button=self.hardware["door_button"],
            servo=self.hardware["servo"],
        )

        self.lighting_mode_control = LightingModeControl(
            button=self.hardware["light_mode_button"],
            lighting_controller=self.lighting_controller,
        )

        self.buzzer_control = BuzzerControl(
            button=self.hardware["silence_button"],
            buzzer=self.hardware["buzzer"],
        )

        self.reset_control = ResetControl(
            button=self.hardware["reset_button"],
            buzzer_control=self.buzzer_control,
        )

        # --------------------------------------------------
        # LCD
        # --------------------------------------------------
        self.lcd = LCDDisplay()

        self.display_controller = DisplayController(
            self.lcd
        )

    def update(
        self,
        temperature,
        humidity,
        gas_alert,
        distance_cm,
        light_value,
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
        self.lighting_controller.update_automatic(
            light_value=light_value
        )

        return state