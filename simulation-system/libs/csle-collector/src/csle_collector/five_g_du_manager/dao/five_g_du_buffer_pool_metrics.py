from typing import Dict, Any, Union
import time
import datetime
from csle_base.json_serializable import JSONSerializable


class FiveGDUBufferPoolMetrics(JSONSerializable):
    """
    DTO class containing srsRAN DU Buffer Pool metrics
    """

    def __init__(self, central_cache_size: int = 0, ip: Union[None, str] = None,
                 ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param central_cache_size: The current size (in bytes/entries) of the central memory pool used for
                                   zero-copy buffer allocation across layers
        :param ip: The IP of the DU
        :param ts: The timestamp the metrics were measured
        """
        self.central_cache_size = central_cache_size
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = self.ts if self.ts else time.time()
        record_str = (f"{ts},{ip},{self.central_cache_size}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGDUBufferPoolMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGDUBufferPoolMetrics(
            ts=float(parts[0]),
            ip=parts[1],
            central_cache_size=int(parts[2])
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
            self.central_cache_size = int(parts[2])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"central_cache_size: {self.central_cache_size}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGDUBufferPoolMetrics":
        """
        Converts a dict representation to an instance.
        Expects the flat dictionary format produced by to_dict().

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGDUBufferPoolMetrics(
            central_cache_size=d.get("central_cache_size", 0),
            ip=d.get("ip"),
            ts=d.get("ts")
        )
        return obj

    @staticmethod
    def from_ws_dict(d: Dict[str, Any], ip: str) -> "FiveGDUBufferPoolMetrics":
        """
        Converts the raw dictionary from the WebSocket JSON stream to an instance.
        Handles the nested "buffer_pool" structure.

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
        if "buffer_pool" in d:
            data = d["buffer_pool"]
        else:
            data = d

        obj = FiveGDUBufferPoolMetrics(
            central_cache_size=data.get("central_cache_size", 0),
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
        d["central_cache_size"] = self.central_cache_size
        return d

    def copy(self) -> "FiveGDUBufferPoolMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGDUBufferPoolMetrics(
            central_cache_size=self.central_cache_size,
            ip=self.ip, ts=self.ts
        )
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 3

    @staticmethod
    def schema() -> "FiveGDUBufferPoolMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGDUBufferPoolMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGDUBufferPoolMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGDUBufferPoolMetrics.from_dict(json.loads(json_str))
