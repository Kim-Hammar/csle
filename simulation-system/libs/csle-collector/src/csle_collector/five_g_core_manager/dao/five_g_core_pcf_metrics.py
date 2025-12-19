from typing import Dict, Any, Union
import time
from csle_base.json_serializable import JSONSerializable


class FiveGCorePCFMetrics(JSONSerializable):
    """
    DTO class containing 5G Core PCF metrics
    """

    def __init__(self, ip: Union[None, str] = None, ts: Union[float, None] = None,
                 fivegs_pcffunction_pa_policyamassoreq: int = 0,
                 fivegs_pcffunction_pa_policyamassosucc: int = 0,
                 fivegs_pcffunction_pa_policysmassoreq: int = 0,
                 fivegs_pcffunction_pa_policysmassosucc: int = 0,
                 fivegs_pcffunction_pa_sessionnbr: int = 0,
                 process_max_fds: int = 0, process_virtual_memory_max_bytes: int = 0,
                 process_cpu_seconds_total: int = 0, process_virtual_memory_bytes: int = 0,
                 process_resident_memory_bytes: int = 0, process_start_time_seconds: int = 0,
                 process_open_fds: int = 0) -> None:
        """
        Initializes the DTO

        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        :param fivegs_pcffunction_pa_policyamassoreq: Number of AM policy association requests
        :param fivegs_pcffunction_pa_policyamassosucc: Number of successful AM policy associations
        :param fivegs_pcffunction_pa_policysmassoreq: Number of SM policy association requests
        :param fivegs_pcffunction_pa_policysmassosucc: Number of successful SM policy associations
        :param fivegs_pcffunction_pa_sessionnbr: Active Sessions
        :param process_max_fds: Maximum number of open file descriptors
        :param process_virtual_memory_max_bytes: Maximum amount of virtual memory available in bytes
        :param process_cpu_seconds_total: Total user and system CPU time spent in seconds
        :param process_virtual_memory_bytes: Virtual memory size in bytes
        :param process_resident_memory_bytes: Resident memory size in bytes
        :param process_start_time_seconds: Start time of the process since unix epoch in seconds
        :param process_open_fds: Number of open file descriptors
        """
        self.ip = ip
        self.ts = ts
        self.fivegs_pcffunction_pa_policyamassoreq = fivegs_pcffunction_pa_policyamassoreq
        self.fivegs_pcffunction_pa_policyamassosucc = fivegs_pcffunction_pa_policyamassosucc
        self.fivegs_pcffunction_pa_policysmassoreq = fivegs_pcffunction_pa_policysmassoreq
        self.fivegs_pcffunction_pa_policysmassosucc = fivegs_pcffunction_pa_policysmassosucc
        self.fivegs_pcffunction_pa_sessionnbr = fivegs_pcffunction_pa_sessionnbr
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
        record_str = (f"{ts},{ip},{self.fivegs_pcffunction_pa_policyamassoreq},"
                      f"{self.fivegs_pcffunction_pa_policyamassosucc},"
                      f"{self.fivegs_pcffunction_pa_policysmassoreq},"
                      f"{self.fivegs_pcffunction_pa_policysmassosucc},"
                      f"{self.fivegs_pcffunction_pa_sessionnbr},"
                      f"{self.process_max_fds},{self.process_virtual_memory_max_bytes},"
                      f"{self.process_cpu_seconds_total},{self.process_virtual_memory_bytes},"
                      f"{self.process_resident_memory_bytes},{self.process_start_time_seconds},"
                      f"{self.process_open_fds}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCorePCFMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCorePCFMetrics(ip=parts[1], ts=float(parts[0]),
                                  fivegs_pcffunction_pa_policyamassoreq=int(parts[2]),
                                  fivegs_pcffunction_pa_policyamassosucc=int(parts[3]),
                                  fivegs_pcffunction_pa_policysmassoreq=int(parts[4]),
                                  fivegs_pcffunction_pa_policysmassosucc=int(parts[5]),
                                  fivegs_pcffunction_pa_sessionnbr=int(parts[6]),
                                  process_max_fds=int(parts[7]),
                                  process_virtual_memory_max_bytes=int(parts[8]),
                                  process_cpu_seconds_total=int(parts[9]),
                                  process_virtual_memory_bytes=int(parts[10]),
                                  process_resident_memory_bytes=int(parts[11]),
                                  process_start_time_seconds=int(parts[12]),
                                  process_open_fds=int(parts[13]))
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
            self.fivegs_pcffunction_pa_policyamassoreq = int(parts[2])
            self.fivegs_pcffunction_pa_policyamassosucc = int(parts[3])
            self.fivegs_pcffunction_pa_policysmassoreq = int(parts[4])
            self.fivegs_pcffunction_pa_policysmassosucc = int(parts[5])
            self.fivegs_pcffunction_pa_sessionnbr = int(parts[6])
            self.process_max_fds = int(parts[7])
            self.process_virtual_memory_max_bytes = int(parts[8])
            self.process_cpu_seconds_total = int(parts[9])
            self.process_virtual_memory_bytes = int(parts[10])
            self.process_resident_memory_bytes = int(parts[11])
            self.process_start_time_seconds = int(parts[12])
            self.process_open_fds = int(parts[13])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"fivegs_pcffunction_pa_policyamassoreq: {self.fivegs_pcffunction_pa_policyamassoreq}, "
                f"fivegs_pcffunction_pa_policyamassosucc: {self.fivegs_pcffunction_pa_policyamassosucc}, "
                f"fivegs_pcffunction_pa_policysmassoreq: {self.fivegs_pcffunction_pa_policysmassoreq}, "
                f"fivegs_pcffunction_pa_policysmassosucc: {self.fivegs_pcffunction_pa_policysmassosucc}, "
                f"fivegs_pcffunction_pa_sessionnbr: {self.fivegs_pcffunction_pa_sessionnbr}, "
                f"process_max_fds: {self.process_max_fds}, "
                f"process_virtual_memory_max_bytes: {self.process_virtual_memory_max_bytes}, "
                f"process_cpu_seconds_total: {self.process_cpu_seconds_total}, "
                f"process_virtual_memory_bytes: {self.process_virtual_memory_bytes}, "
                f"process_resident_memory_bytes: {self.process_resident_memory_bytes}, "
                f"process_start_time_seconds: {self.process_start_time_seconds}, "
                f"process_open_fds: {self.process_open_fds}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCorePCFMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCorePCFMetrics(ip=d["ip"], ts=d["ts"],
                                  fivegs_pcffunction_pa_policyamassoreq=d["fivegs_pcffunction_pa_policyamassoreq"],
                                  fivegs_pcffunction_pa_policyamassosucc=d["fivegs_pcffunction_pa_policyamassosucc"],
                                  fivegs_pcffunction_pa_policysmassoreq=d["fivegs_pcffunction_pa_policysmassoreq"],
                                  fivegs_pcffunction_pa_policysmassosucc=d["fivegs_pcffunction_pa_policysmassosucc"],
                                  fivegs_pcffunction_pa_sessionnbr=d["fivegs_pcffunction_pa_sessionnbr"],
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
        d["fivegs_pcffunction_pa_policyamassoreq"] = self.fivegs_pcffunction_pa_policyamassoreq
        d["fivegs_pcffunction_pa_policyamassosucc"] = self.fivegs_pcffunction_pa_policyamassosucc
        d["fivegs_pcffunction_pa_policysmassoreq"] = self.fivegs_pcffunction_pa_policysmassoreq
        d["fivegs_pcffunction_pa_policysmassosucc"] = self.fivegs_pcffunction_pa_policysmassosucc
        d["fivegs_pcffunction_pa_sessionnbr"] = self.fivegs_pcffunction_pa_sessionnbr
        d["process_max_fds"] = self.process_max_fds
        d["process_virtual_memory_max_bytes"] = self.process_virtual_memory_max_bytes
        d["process_cpu_seconds_total"] = self.process_cpu_seconds_total
        d["process_virtual_memory_bytes"] = self.process_virtual_memory_bytes
        d["process_resident_memory_bytes"] = self.process_resident_memory_bytes
        d["process_start_time_seconds"] = self.process_start_time_seconds
        d["process_open_fds"] = self.process_open_fds
        return d

    def copy(self) -> "FiveGCorePCFMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCorePCFMetrics.from_dict(self.to_dict())
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 14

    @staticmethod
    def schema() -> "FiveGCorePCFMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCorePCFMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCorePCFMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCorePCFMetrics.from_dict(json.loads(json_str))
