"""
Mapa centralizado de GPIO para Raspberry Pi 4.

IMPORTANTE:
- Todos los números corresponden a numeración BCM.
- No representan el número físico del conector de 40 pines.
- Las conexiones físicas se realizarán después de revisar
  alimentación y adaptación de voltajes.
"""


# ==========================================================
# SENSORES
# ==========================================================

# DHT11 - temperatura y humedad
DHT_PIN = 4

# MQ-2 - salida digital DO
GAS_PIN = 17

# Módulo LDR - salida digital DO
LIGHT_SENSOR_PIN = 27

# HC-SR04
ULTRASONIC_TRIGGER_PIN = 23
ULTRASONIC_ECHO_PIN = 24


# ==========================================================
# ACTUADORES
# ==========================================================

# Servo SG90
SERVO_PIN = 18

# Buzzer activo
BUZZER_PIN = 22

# Ventilador controlado mediante transistor 2N2222
FAN_PIN = 25


# ==========================================================
# LEDS DE ESTADO
# ==========================================================

LED_NORMAL_PIN = 5
LED_WARNING_PIN = 6
LED_EMERGENCY_PIN = 13


# ==========================================================
# LEDS DE ILUMINACIÓN
# ==========================================================

LIGHT_1_PIN = 19
LIGHT_2_PIN = 26


# ==========================================================
# BOTONES
# ==========================================================

BUTTON_DOOR_PIN = 16
BUTTON_LIGHT_MODE_PIN = 20
BUTTON_SILENCE_PIN = 21
BUTTON_RESET_PIN = 12


# ==========================================================
# LCD 1602A - MODO PARALELO DE 4 BITS
# ==========================================================

LCD_RS_PIN = 7
LCD_ENABLE_PIN = 8

LCD_D4_PIN = 9
LCD_D5_PIN = 10
LCD_D6_PIN = 11
LCD_D7_PIN = 14