from typing import Dict, Any, Union
import time
from csle_base.json_serializable import JSONSerializable


class FiveGCoreUPFMetrics(JSONSerializable):
    """
    DTO class containing 5G Core UPF metrics
    """

    def __init__(self, ip: Union[None, str] = None, ts: Union[float, None] = None,
                 fivegs_ep_n3_gtp_indatapktn3upf: int = 0, fivegs_ep_n3_gtp_outdatapktn3upf: int = 0,
                 fivegs_upffunction_sm_n4sessionestabreq: int = 0, fivegs_upffunction_sm_n4sessionreport: int = 0,
                 fivegs_upffunction_sm_n4sessionreportsucc: int = 0, fivegs_upffunction_upf_sessionnbr: int = 0,
                 pfcp_peers_active: int = 0, process_max_fds: int = 0, process_virtual_memory_max_bytes: int = 0,
                 process_cpu_seconds_total: int = 0, process_virtual_memory_bytes: int = 0,
                 process_resident_memory_bytes: int = 0, process_start_time_seconds: int = 0,
                 process_open_fds: int = 0) -> None:
        """
        Initializes the DTO

        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        :param fivegs_ep_n3_gtp_indatapktn3upf: Number of incoming GTP data packets on the N3 interface
        :param fivegs_upffunction_sm_n4sessionestabreq: Number of outgoing GTP data packets on the N3 interface
        :param fivegs_upffunction_sm_n4sessionreport: Number of requested N4 session establishments
        :param fivegs_upffunction_sm_n4sessionreportsucc: Number of successful N4 session reports
        :param fivegs_upffunction_upf_sessionnbr: Active Sessions
        :param pfcp_peers_active: Active PFCP peers
        :param process_max_fds: Maximum number of open file descriptors.
        :param process_virtual_memory_max_bytes: Maximum amount of virtual memory available in bytes.
        :param process_cpu_seconds_total: Total user and system CPU time spent in seconds.
        :param process_virtual_memory_bytes: Virtual memory size in bytes.
        :param process_resident_memory_bytes: Resident memory size in bytes.
        :param process_start_time_seconds: Start time of the process since unix epoch in seconds
        :param process_open_fds: Number of open file descriptors.
        """
        self.ip = ip
        self.ts = ts
        self.fivegs_ep_n3_gtp_indatapktn3upf = fivegs_ep_n3_gtp_indatapktn3upf
        self.fivegs_ep_n3_gtp_outdatapktn3upf = fivegs_ep_n3_gtp_outdatapktn3upf
        self.fivegs_upffunction_sm_n4sessionestabreq = fivegs_upffunction_sm_n4sessionestabreq
        self.fivegs_upffunction_sm_n4sessionreport = fivegs_upffunction_sm_n4sessionreport
        self.fivegs_upffunction_sm_n4sessionreportsucc = fivegs_upffunction_sm_n4sessionreportsucc
        self.fivegs_upffunction_upf_sessionnbr = fivegs_upffunction_upf_sessionnbr
        self.pfcp_peers_active = pfcp_peers_active
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
        record_str = (f"{ts},{ip},{self.fivegs_ep_n3_gtp_indatapktn3upf},{self.fivegs_ep_n3_gtp_outdatapktn3upf},"
                      f"{self.fivegs_upffunction_sm_n4sessionestabreq},{self.fivegs_upffunction_sm_n4sessionreport},"
                      f"{self.fivegs_upffunction_sm_n4sessionreportsucc},{self.fivegs_upffunction_upf_sessionnbr},"
                      f"{self.pfcp_peers_active},{self.process_max_fds},{self.process_virtual_memory_max_bytes},"
                      f"{self.process_cpu_seconds_total},{self.process_virtual_memory_bytes},"
                      f"{self.process_resident_memory_bytes},{self.process_start_time_seconds},{self.process_open_fds}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCoreUPFMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCoreUPFMetrics(ip=parts[1], ts=float(parts[0]),
                                  fivegs_ep_n3_gtp_indatapktn3upf=int(parts[2]),
                                  fivegs_ep_n3_gtp_outdatapktn3upf=int(parts[3]),
                                  fivegs_upffunction_sm_n4sessionestabreq=int(parts[4]),
                                  fivegs_upffunction_sm_n4sessionreport=int(parts[5]),
                                  fivegs_upffunction_sm_n4sessionreportsucc=int(parts[6]),
                                  fivegs_upffunction_upf_sessionnbr=int(parts[7]),
                                  pfcp_peers_active=int(parts[8]),
                                  process_max_fds=int(parts[9]),
                                  process_virtual_memory_max_bytes=int(parts[10]),
                                  process_cpu_seconds_total=int(parts[11]),
                                  process_virtual_memory_bytes=int(parts[12]),
                                  process_resident_memory_bytes=int(parts[13]),
                                  process_start_time_seconds=int(parts[14]),
                                  process_open_fds=int(parts[15]))
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
            self.fivegs_ep_n3_gtp_indatapktn3upf = int(parts[2])
            self.fivegs_ep_n3_gtp_outdatapktn3upf = int(parts[3])
            self.fivegs_upffunction_sm_n4sessionestabreq = int(parts[4])
            self.fivegs_upffunction_sm_n4sessionreport = int(parts[5])
            self.fivegs_upffunction_sm_n4sessionreportsucc = int(parts[6])
            self.fivegs_upffunction_upf_sessionnbr = int(parts[7])
            self.pfcp_peers_active = int(parts[8])
            self.process_max_fds = int(parts[9])
            self.process_virtual_memory_max_bytes = int(parts[10])
            self.process_cpu_seconds_total = int(parts[11])
            self.process_virtual_memory_bytes = int(parts[12])
            self.process_resident_memory_bytes = int(parts[13])
            self.process_start_time_seconds = int(parts[14])
            self.process_open_fds = int(parts[15])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"fivegs_ep_n3_gtp_indatapktn3upf: {self.fivegs_ep_n3_gtp_indatapktn3upf}"
                f"fivegs_ep_n3_gtp_outdatapktn3upf: {self.fivegs_ep_n3_gtp_outdatapktn3upf}"
                f"fivegs_upffunction_sm_n4sessionestabreq: {self.fivegs_upffunction_sm_n4sessionestabreq}"
                f"fivegs_upffunction_sm_n4sessionreport: {self.fivegs_upffunction_sm_n4sessionreport}"
                f"fivegs_upffunction_sm_n4sessionreportsucc: {self.fivegs_upffunction_sm_n4sessionreportsucc}"
                f"fivegs_upffunction_upf_sessionnbr: {self.fivegs_upffunction_upf_sessionnbr}"
                f"pfcp_peers_active: {self.pfcp_peers_active}"
                f"process_max_fds: {self.process_max_fds}"
                f"process_virtual_memory_max_bytes: {self.process_virtual_memory_max_bytes}"
                f"process_cpu_seconds_total: {self.process_cpu_seconds_total}"
                f"process_virtual_memory_bytes: {self.process_virtual_memory_bytes}"
                f"process_resident_memory_bytes: {self.process_resident_memory_bytes}"
                f"process_start_time_seconds: {self.process_start_time_seconds}"
                f"process_open_fds: {self.process_open_fds}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCoreUPFMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCoreUPFMetrics(ip=d["ip"], ts=d["ts"],
                                  fivegs_ep_n3_gtp_indatapktn3upf=d["fivegs_ep_n3_gtp_indatapktn3upf"],
                                  fivegs_ep_n3_gtp_outdatapktn3upf=d["fivegs_ep_n3_gtp_outdatapktn3upf"],
                                  fivegs_upffunction_sm_n4sessionestabreq=d["fivegs_upffunction_sm_n4sessionestabreq"],
                                  fivegs_upffunction_sm_n4sessionreport=d["fivegs_upffunction_sm_n4sessionreport"],
                                  fivegs_upffunction_sm_n4sessionreportsucc=d[
                                      "fivegs_upffunction_sm_n4sessionreportsucc"],
                                  fivegs_upffunction_upf_sessionnbr=d["fivegs_upffunction_upf_sessionnbr"],
                                  pfcp_peers_active=d["pfcp_peers_active"],
                                  process_max_fds=d["process_max_fds"],
                                  process_virtual_memory_max_bytes=d["process_virtual_memory_max_bytes"],
                                  process_cpu_seconds_total=d["process_cpu_seconds_total"],
                                  process_virtual_memory_bytes=d["process_virtual_memory_bytes"],
                                  process_resident_memory_bytes=d["process_resident_memory_bytes"],
                                  process_open_fds=d["process_open_fds"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d: Dict[str, Any] = {}
        d["ts"] = self.ts
        d["ip"] = self.ip
        d["fivegs_ep_n3_gtp_indatapktn3upf"] = self.fivegs_ep_n3_gtp_indatapktn3upf
        d["fivegs_ep_n3_gtp_outdatapktn3upf"] = self.fivegs_ep_n3_gtp_outdatapktn3upf
        d["fivegs_upffunction_sm_n4sessionestabreq"] = self.fivegs_upffunction_sm_n4sessionestabreq
        d["fivegs_upffunction_sm_n4sessionreport"] = self.fivegs_upffunction_sm_n4sessionreport
        d["fivegs_upffunction_sm_n4sessionreportsucc"] = self.fivegs_upffunction_sm_n4sessionreportsucc
        d["fivegs_upffunction_upf_sessionnbr"] = self.fivegs_upffunction_upf_sessionnbr
        d["pfcp_peers_active"] = self.pfcp_peers_active
        d["process_max_fds"] = self.process_max_fds
        d["process_virtual_memory_max_bytes"] = self.process_virtual_memory_max_bytes
        d["process_cpu_seconds_total"] = self.process_cpu_seconds_total
        d["process_virtual_memory_bytes"] = self.process_virtual_memory_bytes
        d["process_resident_memory_bytes"] = self.process_resident_memory_bytes
        d["process_start_time_seconds"] = self.process_start_time_seconds
        d["process_open_fds"] = self.process_open_fds
        return d

    def copy(self) -> "FiveGCoreUPFMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCoreUPFMetrics(ip=self.ip, ts=self.ts)
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 16

    @staticmethod
    def schema() -> "FiveGCoreUPFMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCoreUPFMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCoreUPFMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCoreUPFMetrics.from_dict(json.loads(json_str))
