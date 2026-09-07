"""
Umbrales configurables del sistema.

Los valores definitivos deberán establecerse durante
las pruebas físicas de los sensores.
"""

# Temperatura
TEMP_MAX = 30.0

# Humedad
HUMIDITY_MIN = 30.0
HUMIDITY_MAX = 70.0

# Distancia para detección de presencia (cm)
DISTANCE_THRESHOLD = 30.0

# Tiempo que permanece abierta la puerta (segundos)
DOOR_OPEN_TIME = 5

# Los sensores MQ y LDR requieren calibración física.
GAS_THRESHOLD = None
LIGHT_THRESHOLD = None