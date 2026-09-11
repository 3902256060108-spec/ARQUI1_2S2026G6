from datetime import datetime


class SystemStatus:
    def __init__(
        self,
        estado: str,
        timestamp: datetime
    ):
        self.estado = estado
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "estado": self.estado,
            "timestamp": self.timestamp
        }