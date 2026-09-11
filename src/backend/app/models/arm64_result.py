from datetime import datetime


class Arm64Result:
    def __init__(
        self,
        max_value: float,
        min_value: float,
        avg: float,
        count: int,
        timestamp: datetime
    ):
        self.max = max_value
        self.min = min_value
        self.avg = avg
        self.count = count
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "max": self.max,
            "min": self.min,
            "avg": self.avg,
            "count": self.count,
            "timestamp": self.timestamp
        }