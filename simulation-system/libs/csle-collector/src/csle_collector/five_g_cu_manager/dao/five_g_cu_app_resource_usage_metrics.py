from typing import Dict, Any, Union
import time
import datetime
from csle_base.json_serializable import JSONSerializable


class FiveGCUAppResourceUsageMetrics(JSONSerializable):
    """
    DTO class containing srsRAN CU (Central Unit) Application Resource Usage metrics.
    Captures system-level performance indicators for the application process.
    """

    def __init__(self, cpu_usage_percent: float = 0.0, memory_usage_mb: float = 0.0,
                 power_consumption_watts: float = 0.0, ip: Union[None, str] = None,
                 ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param cpu_usage_percent: CPU usage percentage (can exceed 100% on multi-core)
        :param memory_usage_mb: Resident memory usage in Megabytes
        :param power_consumption_watts: Estimated power consumption in Watts
        :param ip: The IP of the CU
        :param ts: The timestamp the metrics were measured
        """
        self.cpu_usage_percent = cpu_usage_percent
        self.memory_usage_mb = memory_usage_mb
        self.power_consumption_watts = power_consumption_watts
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = self.ts if self.ts else time.time()
        record_str = (f"{ts},{ip},{self.cpu_usage_percent},"
                      f"{self.memory_usage_mb},{self.power_consumption_watts}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCUAppResourceUsageMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCUAppResourceUsageMetrics(
            ts=float(parts[0]),
            ip=parts[1],
            cpu_usage_percent=float(parts[2]),
            memory_usage_mb=float(parts[3]),
            power_consumption_watts=float(parts[4])
        )
        return obj

    def update_with_kafka_record(self, record: str, ip: str) -> None:
        """
        Updates the DTO based on a kafka record

        :param record: the kafka record
        :param ip: the host ip
        :return: None
        """
        parts = record.split(",")
        if parts[1] == ip:
            self.ts = float(parts[0])
            self.ip = parts[1]
            self.cpu_usage_percent = float(parts[2])
            self.memory_usage_mb = float(parts[3])
            self.power_consumption_watts = float(parts[4])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"cpu: {self.cpu_usage_percent}%, mem: {self.memory_usage_mb}MB, "
                f"power: {self.power_consumption_watts}W")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCUAppResourceUsageMetrics":
        """
        Converts a dict representation to an instance.
        Expects the flat dictionary format produced by to_dict().

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCUAppResourceUsageMetrics(
            cpu_usage_percent=d.get("cpu_usage_percent", 0.0),
            memory_usage_mb=d.get("memory_usage_mb", 0.0),
            power_consumption_watts=d.get("power_consumption_watts", 0.0),
            ip=d.get("ip"),
            ts=d.get("ts")
        )
        return obj

    @staticmethod
    def from_ws_dict(d: Dict[str, Any], ip: str) -> "FiveGCUAppResourceUsageMetrics":
        """
        Converts the raw dictionary from the WebSocket JSON stream to an instance.
        Handles the nested "app_resource_usage" structure.

        :param d: the raw dictionary from srsRAN WebSocket
        :param ip: the IP of the source CU
        :return: the created instance
        """
        ts = time.time()
        if "timestamp" in d and d["timestamp"] is not None:
            try:
                dt = datetime.datetime.fromisoformat(d["timestamp"])
                ts = dt.timestamp()
            except Exception:
                pass

        data = {}
        if "app_resource_usage" in d:
            data = d["app_resource_usage"]
        else:
            data = d

        obj = FiveGCUAppResourceUsageMetrics(
            cpu_usage_percent=data.get("cpu_usage_percent", 0.0),
            memory_usage_mb=data.get("memory_usage_mb", 0.0),
            power_consumption_watts=data.get("power_consumption_watts", 0.0),
            ip=ip,
            ts=ts
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d: Dict[str, Any] = {}
        d["ts"] = self.ts
        d["ip"] = self.ip
        d["cpu_usage_percent"] = self.cpu_usage_percent
        d["memory_usage_mb"] = self.memory_usage_mb
        d["power_consumption_watts"] = self.power_consumption_watts
        return d

    def copy(self) -> "FiveGCUAppResourceUsageMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCUAppResourceUsageMetrics(
            cpu_usage_percent=self.cpu_usage_percent,
            memory_usage_mb=self.memory_usage_mb,
            power_consumption_watts=self.power_consumption_watts,
            ip=self.ip, ts=self.ts
        )
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 5

    @staticmethod
    def schema() -> "FiveGCUAppResourceUsageMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCUAppResourceUsageMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCUAppResourceUsageMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCUAppResourceUsageMetrics.from_dict(json.loads(json_str))
