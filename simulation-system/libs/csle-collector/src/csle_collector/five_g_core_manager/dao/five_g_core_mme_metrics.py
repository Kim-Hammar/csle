from typing import Dict, Any, Union
import time
from csle_base.json_serializable import JSONSerializable


class FiveGCoreMMEMetrics(JSONSerializable):
    """
    DTO class containing 5G Core MME metrics
    """

    def __init__(self, ip: Union[None, str] = None, ts: Union[float, None] = None,
                 enb_ue: int = 0, mme_session: int = 0, enb: int = 0, process_max_fds: int = 1024,
                 process_virtual_memory_max_bytes: int = 0, process_cpu_seconds_total: int = 0,
                 process_virtual_memory_bytes: int = 0, process_resident_memory_bytes: int = 0,
                 process_start_time_seconds: int = 0, process_open_fds: int = 0) -> None:
        """
        Initializes the DTO

        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        :param enb_ue: Number of UEs connected to eNodeBs
        :param mme_session: MME Sessions
        :param enb: eNodeBs
        :param process_max_fds: Maximum number of open file descriptors.
        :param process_virtual_memory_max_bytes: Maximum amount of virtual memory available in bytes.
        :param process_cpu_seconds_total: Total user and system CPU time spent in seconds.
        :param process_virtual_memory_bytes:  Virtual memory size in bytes.
        :param process_resident_memory_bytes:  Resident memory size in bytes.
        :param process_start_time_seconds:  Start time of the process since unix epoch in seconds.
        :param process_open_fds: Number of open file descriptors
        """
        self.ip = ip
        self.ts = ts
        self.enb_ue = enb_ue
        self.mme_session = mme_session
        self.enb = enb
        self.process_max_fds = process_max_fds
        self.process_virtual_memory_max_bytes = process_virtual_memory_max_bytes
        self.process_cpu_seconds_total = process_cpu_seconds_total
        self.process_virtual_memory_bytes = process_virtual_memory_bytes
        self.process_resident_memory_bytes = process_resident_memory_bytes
        self.process_start_time_seconds = process_start_time_seconds
        self.process_open_fds = process_open_fds

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = time.time()
        record_str = (f"{ts},{ip},{self.enb_ue},{self.mme_session},{self.enb},{self.process_max_fds},"
                      f"{self.process_virtual_memory_max_bytes},{self.process_cpu_seconds_total},"
                      f"{self.process_virtual_memory_bytes},{self.process_resident_memory_bytes},"
                      f"{self.process_start_time_seconds},{self.process_open_fds}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCoreMMEMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCoreMMEMetrics(ip=parts[1], ts=float(parts[0]),
                                  enb_ue=int(parts[2]),
                                  mme_session=int(parts[3]),
                                  enb=int(parts[4]),
                                  process_max_fds=int(parts[5]),
                                  process_virtual_memory_max_bytes=int(parts[6]),
                                  process_cpu_seconds_total=int(parts[7]),
                                  process_virtual_memory_bytes=int(parts[8]),
                                  process_resident_memory_bytes=int(parts[9]),
                                  process_start_time_seconds=int(parts[10]),
                                  process_open_fds=int(parts[11]))
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
            self.enb_ue = int(parts[2])
            self.mme_session = int(parts[3])
            self.enb = int(parts[4])
            self.process_max_fds = int(parts[5])
            self.process_virtual_memory_max_bytes = int(parts[6])
            self.process_cpu_seconds_total = int(parts[7])
            self.process_virtual_memory_bytes = int(parts[8])
            self.process_resident_memory_bytes = int(parts[9])
            self.process_start_time_seconds = int(parts[10])
            self.process_open_fds = int(parts[11])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"enb_ue: {self.enb_ue}, "
                f"mme_session: {self.mme_session}, "
                f"enb: {self.enb}, "
                f"process_max_fds: {self.process_max_fds}, "
                f"process_virtual_memory_max_bytes: {self.process_virtual_memory_max_bytes}, "
                f"process_cpu_seconds_total: {self.process_cpu_seconds_total}, "
                f"process_virtual_memory_bytes: {self.process_virtual_memory_bytes}, "
                f"process_resident_memory_bytes: {self.process_resident_memory_bytes}, "
                f"process_start_time_seconds: {self.process_start_time_seconds}, "
                f"process_open_fds: {self.process_open_fds}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCoreMMEMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCoreMMEMetrics(ip=d["ip"], ts=d["ts"],
                                  enb_ue=d["enb_ue"],
                                  mme_session=d["mme_session"],
                                  enb=d["enb"],
                                  process_max_fds=d["process_max_fds"],
                                  process_virtual_memory_max_bytes=d["process_virtual_memory_max_bytes"],
                                  process_cpu_seconds_total=d["process_cpu_seconds_total"],
                                  process_virtual_memory_bytes=d["process_virtual_memory_bytes"],
                                  process_resident_memory_bytes=d["process_resident_memory_bytes"],
                                  process_start_time_seconds=d["process_start_time_seconds"],
                                  process_open_fds=d["process_open_fds"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d: Dict[str, Any] = {}
        d["ts"] = self.ts
        d["ip"] = self.ip
        d["enb_ue"] = self.enb_ue
        d["mme_session"] = self.mme_session
        d["enb"] = self.enb
        d["process_max_fds"] = self.process_max_fds
        d["process_virtual_memory_max_bytes"] = self.process_virtual_memory_max_bytes
        d["process_cpu_seconds_total"] = self.process_cpu_seconds_total
        d["process_virtual_memory_bytes"] = self.process_virtual_memory_bytes
        d["process_resident_memory_bytes"] = self.process_resident_memory_bytes
        d["process_start_time_seconds"] = self.process_start_time_seconds
        d["process_open_fds"] = self.process_open_fds
        return d

    def copy(self) -> "FiveGCoreMMEMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCoreMMEMetrics(ip=self.ip, ts=self.ts)
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 16

    @staticmethod
    def schema() -> "FiveGCoreMMEMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCoreMMEMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCoreMMEMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCoreMMEMetrics.from_dict(json.loads(json_str))
