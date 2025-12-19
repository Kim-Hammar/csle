from typing import Dict, Any, Union
import time
import datetime
from csle_base.json_serializable import JSONSerializable


class FiveGDUMetrics(JSONSerializable):
    """
    DTO class containing srsRAN DU High-MAC metrics
    """

    def __init__(self, pci: int = 0, average_latency_us: float = 0.0,
                 cpu_usage_percent: float = 0.0, max_latency_us: float = 0.0,
                 min_latency_us: float = 0.0, ip: Union[None, str] = None,
                 ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param pci: The Physical Cell ID
        :param average_latency_us: Average CPU processing latency in microseconds
        :param cpu_usage_percent: CPU usage percentage
        :param max_latency_us: Maximum latency in microseconds
        :param min_latency_us: Minimum latency in microseconds
        :param ip: The IP of the DU
        :param ts: The timestamp the metrics were measured
        """
        self.pci = pci
        self.average_latency_us = average_latency_us
        self.cpu_usage_percent = cpu_usage_percent
        self.max_latency_us = max_latency_us
        self.min_latency_us = min_latency_us
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = self.ts if self.ts else time.time()
        record_str = (f"{ts},{ip},{self.pci},{self.average_latency_us},"
                      f"{self.cpu_usage_percent},{self.max_latency_us},"
                      f"{self.min_latency_us}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGDUMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGDUMetrics(
            ts=float(parts[0]),
            ip=parts[1],
            pci=int(parts[2]),
            average_latency_us=float(parts[3]),
            cpu_usage_percent=float(parts[4]),
            max_latency_us=float(parts[5]),
            min_latency_us=float(parts[6])
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
            self.pci = int(parts[2])
            self.average_latency_us = float(parts[3])
            self.cpu_usage_percent = float(parts[4])
            self.max_latency_us = float(parts[5])
            self.min_latency_us = float(parts[6])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"pci: {self.pci}, "
                f"average_latency_us: {self.average_latency_us}, "
                f"cpu_usage_percent: {self.cpu_usage_percent}, "
                f"max_latency_us: {self.max_latency_us}, "
                f"min_latency_us: {self.min_latency_us}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGDUMetrics":
        """
        Converts a dict representation to an instance.
        Expects the flat dictionary format produced by to_dict().

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGDUMetrics(
            pci=d.get("pci", 0),
            average_latency_us=d.get("average_latency_us", 0.0),
            cpu_usage_percent=d.get("cpu_usage_percent", 0.0),
            max_latency_us=d.get("max_latency_us", 0.0),
            min_latency_us=d.get("min_latency_us", 0.0),
            ip=d.get("ip"),
            ts=d.get("ts")
        )
        return obj

    @staticmethod
    def from_ws_dict(d: Dict[str, Any], ip: str) -> "FiveGDUMetrics":
        """
        Converts the raw dictionary from the WebSocket JSON stream to an instance.

        :param d: the raw dictionary from srsRAN WebSocket
        :param ip: the IP of the source DU
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
        try:
            # Navigate nested structure: du -> du_high -> mac -> dl -> [0]
            data = d["du"]["du_high"]["mac"]["dl"][0]
        except (KeyError, IndexError, TypeError):
            pass

        obj = FiveGDUMetrics(
            pci=data.get("pci", 0),
            average_latency_us=data.get("average_latency_us", 0.0),
            cpu_usage_percent=data.get("cpu_usage_percent", 0.0),
            max_latency_us=data.get("max_latency_us", 0.0),
            min_latency_us=data.get("min_latency_us", 0.0),
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
        d["pci"] = self.pci
        d["average_latency_us"] = self.average_latency_us
        d["cpu_usage_percent"] = self.cpu_usage_percent
        d["max_latency_us"] = self.max_latency_us
        d["min_latency_us"] = self.min_latency_us
        return d

    def copy(self) -> "FiveGDUMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGDUMetrics(
            pci=self.pci,
            average_latency_us=self.average_latency_us,
            cpu_usage_percent=self.cpu_usage_percent,
            max_latency_us=self.max_latency_us,
            min_latency_us=self.min_latency_us,
            ip=self.ip,
            ts=self.ts
        )
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 7

    @staticmethod
    def schema() -> "FiveGDUMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGDUMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGDUMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGDUMetrics.from_dict(json.loads(json_str))
