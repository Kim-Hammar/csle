from typing import Dict, Any, Union
import time
from csle_base.json_serializable import JSONSerializable


class CUMetrics(JSONSerializable):
    """
    DTO class containing 5G CU metrics
    """

    def __init__(self, ip: Union[None, str] = None, ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        """
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = time.time()
        record_str = f"{ts},{ip}"
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "CUMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = CUMetrics(ip=parts[1], ts=float(parts[0]))
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
            self.ip = parts[1]
            self.ts = float(parts[0])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ts: {self.ts}, ip: {self.ip}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CUMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = CUMetrics(ip=d["ip"], ts=d["ts"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d: Dict[str, Any] = {}
        d["ts"] = self.ts
        d["ip"] = self.ip
        return d

    def copy(self) -> "CUMetrics":
        """
        :return: a copy of the object
        """
        c = CUMetrics(ip=self.ip, ts=self.ts)
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 2

    @staticmethod
    def schema() -> "CUMetrics":
        """
        :return: get the schema of the DTO
        """
        return CUMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "CUMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return CUMetrics.from_dict(json.loads(json_str))
