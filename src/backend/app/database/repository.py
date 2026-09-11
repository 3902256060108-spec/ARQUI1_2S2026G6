from datetime import datetime, timezone

from src.backend.app.database.mongodb import mongodb


class Repository:
    def _collection(self, name: str):
        if mongodb.database is None:
            raise RuntimeError("MongoDB no está conectado")

        return mongodb.database[name]

    def insert_sensor_reading(
        self,
        sensor: str,
        valor: float
    ):
        document = {
            "sensor": sensor,
            "valor": valor,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("sensor_readings").insert_one(document)

    def insert_event(
        self,
        tipo: str,
        estado: str,
        descripcion: str
    ):
        document = {
            "tipo": tipo,
            "estado": estado,
            "descripcion": descripcion,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("events").insert_one(document)

    def insert_command(
        self,
        dispositivo: str,
        accion: str,
        origen: str = "dashboard"
    ):
        document = {
            "dispositivo": dispositivo,
            "accion": accion,
            "origen": origen,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("commands").insert_one(document)

    def insert_arm64_result(
        self,
        max_value: float,
        min_value: float,
        avg: float,
        count: int
    ):
        document = {
            "max": max_value,
            "min": min_value,
            "avg": avg,
            "count": count,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("arm64_results").insert_one(document)

    def insert_system_status(
        self,
        estado: str
    ):
        document = {
            "estado": estado,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("system_status").insert_one(document)

    def insert_actuator_status(
        self,
        dispositivo: str,
        estado: str
    ):
        document = {
            "dispositivo": dispositivo,
            "estado": estado,
            "timestamp": datetime.now(timezone.utc)
        }

        return self._collection("actuator_status").insert_one(document)

    def get_latest_sensor_readings(self):
        collection = self._collection("sensor_readings")

        sensors = [
            "temperatura",
            "humedad",
            "gas",
            "distancia",
            "luz"
        ]

        result = {}

        for sensor in sensors:
            document = collection.find_one(
                {"sensor": sensor},
                sort=[("timestamp", -1)]
            )

            if document:
                document.pop("_id", None)
                result[sensor] = document

        return result

    def get_latest_system_status(self):
        document = self._collection("system_status").find_one(
            {},
            sort=[("timestamp", -1)]
        )

        if document:
            document.pop("_id", None)

        return document

    def get_latest_actuator_statuses(self):
        collection = self._collection("actuator_status")

        devices = [
            "puerta",
            "luces",
            "ventilador",
            "alarma"
        ]

        result = {}

        for dispositivo in devices:
            document = collection.find_one(
                {"dispositivo": dispositivo},
                sort=[("timestamp", -1)]
            )

            if document:
                document.pop("_id", None)
                result[dispositivo] = document

        return result

    def get_sensor_history(self, limit: int = 20):
        documents = list(
            self._collection("sensor_readings")
            .find({}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )

        return documents

    def get_event_history(self, limit: int = 20):
        documents = list(
            self._collection("events")
            .find({}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )

        return documents

    def get_latest_arm64_result(self):
        document = self._collection("arm64_results").find_one(
            {},
            sort=[("timestamp", -1)]
        )

        if document:
            document.pop("_id", None)

        return document

    def get_command_history(self, limit: int = 20):
        documents = list(
            self._collection("commands")
            .find({}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )

        return documents
repository = Repository()