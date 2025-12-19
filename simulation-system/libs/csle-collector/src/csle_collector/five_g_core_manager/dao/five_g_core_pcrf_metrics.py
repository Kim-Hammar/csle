from typing import Dict, Any, Union
import time
from csle_base.json_serializable import JSONSerializable


class FiveGCorePCRFMetrics(JSONSerializable):
    """
    DTO class containing 5G Core PCRF metrics (Gx and Rx interfaces)
    """

    def __init__(self, ip: Union[None, str] = None, ts: Union[float, None] = None,
                 gx_rx_unknown: int = 0, gx_rx_ccr: int = 0, gx_rx_ccr_error: int = 0,
                 gx_rx_raa: int = 0, gx_tx_cca: int = 0, gx_tx_rar: int = 0,
                 gx_tx_rar_error: int = 0, rx_rx_unknown: int = 0, rx_rx_aar: int = 0,
                 rx_rx_aar_error: int = 0, rx_rx_asa: int = 0, rx_rx_asa_error: int = 0,
                 rx_rx_str_error: int = 0, rx_tx_aaa: int = 0, rx_tx_sar: int = 0,
                 rx_tx_sta: int = 0, process_max_fds: int = 0,
                 process_virtual_memory_max_bytes: int = 0, process_cpu_seconds_total: int = 0,
                 process_virtual_memory_bytes: int = 0, process_resident_memory_bytes: int = 0,
                 process_start_time_seconds: int = 0, process_open_fds: int = 0) -> None:
        """
        Initializes the DTO

        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        :param gx_rx_unknown: Received Gx unknown messages
        :param gx_rx_ccr: Received Gx CCR messages
        :param gx_rx_ccr_error: Received Gx CCR messages failed
        :param gx_rx_raa: Received Gx RAA messages
        :param gx_tx_cca: Transmitted Gx CCA messages (Note: description in metrics said RAA failed, usually CCA)
        :param gx_tx_rar: Transmitted Gx RAR messages
        :param gx_tx_rar_error: Failed to transmit Gx RAR messages
        :param rx_rx_unknown: Received Rx unknown messages
        :param rx_rx_aar: Received Rx AAR messages
        :param rx_rx_aar_error: Received Rx AAR messages failed
        :param rx_rx_asa: Received Rx ASA messages
        :param rx_rx_asa_error: Received Rx ASA messages failed
        :param rx_rx_str_error: Received Rx STR messages failed
        :param rx_tx_aaa: Transmitted Rx AAA messages
        :param rx_tx_sar: Transmitted Rx SAR messages
        :param rx_tx_sta: Transmitted Rx STA messages
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
        self.gx_rx_unknown = gx_rx_unknown
        self.gx_rx_ccr = gx_rx_ccr
        self.gx_rx_ccr_error = gx_rx_ccr_error
        self.gx_rx_raa = gx_rx_raa
        self.gx_tx_cca = gx_tx_cca
        self.gx_tx_rar = gx_tx_rar
        self.gx_tx_rar_error = gx_tx_rar_error
        self.rx_rx_unknown = rx_rx_unknown
        self.rx_rx_aar = rx_rx_aar
        self.rx_rx_aar_error = rx_rx_aar_error
        self.rx_rx_asa = rx_rx_asa
        self.rx_rx_asa_error = rx_rx_asa_error
        self.rx_rx_str_error = rx_rx_str_error
        self.rx_tx_aaa = rx_tx_aaa
        self.rx_tx_sar = rx_tx_sar
        self.rx_tx_sta = rx_tx_sta
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
        record_str = (f"{ts},{ip},{self.gx_rx_unknown},{self.gx_rx_ccr},{self.gx_rx_ccr_error},"
                      f"{self.gx_rx_raa},{self.gx_tx_cca},{self.gx_tx_rar},{self.gx_tx_rar_error},"
                      f"{self.rx_rx_unknown},{self.rx_rx_aar},{self.rx_rx_aar_error},"
                      f"{self.rx_rx_asa},{self.rx_rx_asa_error},{self.rx_rx_str_error},"
                      f"{self.rx_tx_aaa},{self.rx_tx_sar},{self.rx_tx_sta},"
                      f"{self.process_max_fds},{self.process_virtual_memory_max_bytes},"
                      f"{self.process_cpu_seconds_total},{self.process_virtual_memory_bytes},"
                      f"{self.process_resident_memory_bytes},{self.process_start_time_seconds},"
                      f"{self.process_open_fds}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCorePCRFMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCorePCRFMetrics(ip=parts[1], ts=float(parts[0]),
                                   gx_rx_unknown=int(parts[2]), gx_rx_ccr=int(parts[3]),
                                   gx_rx_ccr_error=int(parts[4]), gx_rx_raa=int(parts[5]),
                                   gx_tx_cca=int(parts[6]), gx_tx_rar=int(parts[7]),
                                   gx_tx_rar_error=int(parts[8]), rx_rx_unknown=int(parts[9]),
                                   rx_rx_aar=int(parts[10]), rx_rx_aar_error=int(parts[11]),
                                   rx_rx_asa=int(parts[12]), rx_rx_asa_error=int(parts[13]),
                                   rx_rx_str_error=int(parts[14]), rx_tx_aaa=int(parts[15]),
                                   rx_tx_sar=int(parts[16]), rx_tx_sta=int(parts[17]),
                                   process_max_fds=int(parts[18]),
                                   process_virtual_memory_max_bytes=int(parts[19]),
                                   process_cpu_seconds_total=int(parts[20]),
                                   process_virtual_memory_bytes=int(parts[21]),
                                   process_resident_memory_bytes=int(parts[22]),
                                   process_start_time_seconds=int(parts[23]),
                                   process_open_fds=int(parts[24]))
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
            self.gx_rx_unknown = int(parts[2])
            self.gx_rx_ccr = int(parts[3])
            self.gx_rx_ccr_error = int(parts[4])
            self.gx_rx_raa = int(parts[5])
            self.gx_tx_cca = int(parts[6])
            self.gx_tx_rar = int(parts[7])
            self.gx_tx_rar_error = int(parts[8])
            self.rx_rx_unknown = int(parts[9])
            self.rx_rx_aar = int(parts[10])
            self.rx_rx_aar_error = int(parts[11])
            self.rx_rx_asa = int(parts[12])
            self.rx_rx_asa_error = int(parts[13])
            self.rx_rx_str_error = int(parts[14])
            self.rx_tx_aaa = int(parts[15])
            self.rx_tx_sar = int(parts[16])
            self.rx_tx_sta = int(parts[17])
            self.process_max_fds = int(parts[18])
            self.process_virtual_memory_max_bytes = int(parts[19])
            self.process_cpu_seconds_total = int(parts[20])
            self.process_virtual_memory_bytes = int(parts[21])
            self.process_resident_memory_bytes = int(parts[22])
            self.process_start_time_seconds = int(parts[23])
            self.process_open_fds = int(parts[24])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"gx_rx_unknown: {self.gx_rx_unknown}, gx_rx_ccr: {self.gx_rx_ccr}, "
                f"gx_rx_ccr_error: {self.gx_rx_ccr_error}, gx_rx_raa: {self.gx_rx_raa}, "
                f"gx_tx_cca: {self.gx_tx_cca}, gx_tx_rar: {self.gx_tx_rar}, "
                f"gx_tx_rar_error: {self.gx_tx_rar_error}, rx_rx_unknown: {self.rx_rx_unknown}, "
                f"rx_rx_aar: {self.rx_rx_aar}, rx_rx_aar_error: {self.rx_rx_aar_error}, "
                f"rx_rx_asa: {self.rx_rx_asa}, rx_rx_asa_error: {self.rx_rx_asa_error}, "
                f"rx_rx_str_error: {self.rx_rx_str_error}, rx_tx_aaa: {self.rx_tx_aaa}, "
                f"rx_tx_sar: {self.rx_tx_sar}, rx_tx_sta: {self.rx_tx_sta}, "
                f"process_max_fds: {self.process_max_fds}, "
                f"process_virtual_memory_max_bytes: {self.process_virtual_memory_max_bytes}, "
                f"process_cpu_seconds_total: {self.process_cpu_seconds_total}, "
                f"process_virtual_memory_bytes: {self.process_virtual_memory_bytes}, "
                f"process_resident_memory_bytes: {self.process_resident_memory_bytes}, "
                f"process_start_time_seconds: {self.process_start_time_seconds}, "
                f"process_open_fds: {self.process_open_fds}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCorePCRFMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCorePCRFMetrics(ip=d["ip"], ts=d["ts"],
                                   gx_rx_unknown=d["gx_rx_unknown"], gx_rx_ccr=d["gx_rx_ccr"],
                                   gx_rx_ccr_error=d["gx_rx_ccr_error"], gx_rx_raa=d["gx_rx_raa"],
                                   gx_tx_cca=d["gx_tx_cca"], gx_tx_rar=d["gx_tx_rar"],
                                   gx_tx_rar_error=d["gx_tx_rar_error"], rx_rx_unknown=d["rx_rx_unknown"],
                                   rx_rx_aar=d["rx_rx_aar"], rx_rx_aar_error=d["rx_rx_aar_error"],
                                   rx_rx_asa=d["rx_rx_asa"], rx_rx_asa_error=d["rx_rx_asa_error"],
                                   rx_rx_str_error=d["rx_rx_str_error"], rx_tx_aaa=d["rx_tx_aaa"],
                                   rx_tx_sar=d["rx_tx_sar"], rx_tx_sta=d["rx_tx_sta"],
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
        d["gx_rx_unknown"] = self.gx_rx_unknown
        d["gx_rx_ccr"] = self.gx_rx_ccr
        d["gx_rx_ccr_error"] = self.gx_rx_ccr_error
        d["gx_rx_raa"] = self.gx_rx_raa
        d["gx_tx_cca"] = self.gx_tx_cca
        d["gx_tx_rar"] = self.gx_tx_rar
        d["gx_tx_rar_error"] = self.gx_tx_rar_error
        d["rx_rx_unknown"] = self.rx_rx_unknown
        d["rx_rx_aar"] = self.rx_rx_aar
        d["rx_rx_aar_error"] = self.rx_rx_aar_error
        d["rx_rx_asa"] = self.rx_rx_asa
        d["rx_rx_asa_error"] = self.rx_rx_asa_error
        d["rx_rx_str_error"] = self.rx_rx_str_error
        d["rx_tx_aaa"] = self.rx_tx_aaa
        d["rx_tx_sar"] = self.rx_tx_sar
        d["rx_tx_sta"] = self.rx_tx_sta
        d["process_max_fds"] = self.process_max_fds
        d["process_virtual_memory_max_bytes"] = self.process_virtual_memory_max_bytes
        d["process_cpu_seconds_total"] = self.process_cpu_seconds_total
        d["process_virtual_memory_bytes"] = self.process_virtual_memory_bytes
        d["process_resident_memory_bytes"] = self.process_resident_memory_bytes
        d["process_start_time_seconds"] = self.process_start_time_seconds
        d["process_open_fds"] = self.process_open_fds
        return d

    def copy(self) -> "FiveGCorePCRFMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCorePCRFMetrics.from_dict(self.to_dict())
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 25

    @staticmethod
    def schema() -> "FiveGCorePCRFMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCorePCRFMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCorePCRFMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCorePCRFMetrics.from_dict(json.loads(json_str))
