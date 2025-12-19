from typing import Dict, Any, Union
import time
from csle_base.json_serializable import JSONSerializable


class FiveGCoreHSSMetrics(JSONSerializable):
    """
    DTO class containing 5G Core HSS metrics
    """

    def __init__(self, ip: Union[None, str] = None, ts: Union[float, None] = None,
                 cx_rx_lir: int = 0, cx_rx_uar: int = 0, cx_tx_lia: int = 0, cx_rx_unknown: int = 0,
                 cx_rx_sar: int = 0, s6a_rx_pur: int = 0, swx_rx_mar_error: int = 0, cx_tx_uaa: int = 0,
                 s6a_rx_pur_error: int = 0, s6a_tx_clr: int = 0, cx_tx_saa: int = 0, cx_rx_lir_error: int = 0,
                 s6a_rx_ulr: int = 0, s6a_rx_cla: int = 0, s6a_rx_cla_error: int = 0, s6a_rx_air: int = 0,
                 cx_rx_mar: int = 0, swx_rx_sar: int = 0, s6a_rx_air_error: int = 0, s6a_rx_ida_error: int = 0,
                 cx_tx_maa: int = 0, swx_rx_mar: int = 0, s6a_rx_unknown: int = 0, s6a_tx_pua: int = 0,
                 swx_rx_unknown: int = 0, cx_rx_mar_error: int = 0, cx_rx_uar_error: int = 0, s6a_tx_ula: int = 0,
                 s6a_rx_ulr_error: int = 0, s6a_tx_aia: int = 0, s6a_tx_idr: int = 0, s6a_rx_ida: int = 0,
                 cx_rx_sar_error: int = 0, swx_rx_sar_error: int = 0, swx_tx_maa: int = 0, swx_tx_saa: int = 0,
                 hss_imsi: int = 0, hss_impi: int = 0, hss_impu: int = 0,
                 process_max_fds: int = 0, process_virtual_memory_max_bytes: int = 0,
                 process_cpu_seconds_total: int = 0, process_virtual_memory_bytes: int = 0,
                 process_resident_memory_bytes: int = 0, process_start_time_seconds: int = 0,
                 process_open_fds: int = 0) -> None:
        """
        Initializes the DTO

        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        :param cx_rx_lir: Transmitted Cx LIR messages
        :param cx_rx_uar: Received Cx UAR messages
        :param cx_tx_lia: Transmitted Cx LIA messages
        :param cx_rx_unknown: Received Cx unknown messages
        :param cx_rx_sar: Received Cx SAR messages
        :param s6a_rx_pur: Transmitted S6a PUR messages
        :param swx_rx_mar_error: Received SWx MAR messages failed
        :param cx_tx_uaa: Transmitted Cx UAA messages
        :param s6a_rx_pur_error: Transmitted S6a PUR messages failed
        :param s6a_tx_clr: Transmitted S6a CLR messages
        :param cx_tx_saa: Transmitted Cx SAA messages
        :param cx_rx_lir_error: Transmitted Cx LIR messages failed
        :param s6a_rx_ulr: Transmitted S6a ULR messages
        :param s6a_rx_cla: Received S6a CLA messages
        :param s6a_rx_cla_error: Received S6a CLA messages failed
        :param s6a_rx_air: Received S6a AIR messages
        :param cx_rx_mar: Received Cx MAR messages
        :param swx_rx_sar: Received SWx SAR messages
        :param s6a_rx_air_error: Received S6a AIR messages failed
        :param s6a_rx_ida_error: Received S6a IDA messages failed
        :param cx_tx_maa: Transmitted Cx MAA messages
        :param swx_rx_mar: Received SWx MAR messages
        :param s6a_rx_unknown: Received S6a unknown messages
        :param s6a_tx_pua: Transmitted S6a PUA messages
        :param swx_rx_unknown: Received SWx unknown messages
        :param cx_rx_mar_error: Received Cx MAR messages failed
        :param cx_rx_uar_error: Received Cx UAR messages failed
        :param s6a_tx_ula: Transmitted S6a ULA messages
        :param s6a_rx_ulr_error: Transmitted S6a ULR messages failed
        :param s6a_tx_aia: Transmitted S6a AIA messages
        :param s6a_tx_idr: Transmitted S6a IDR messages
        :param s6a_rx_ida: Received S6a IDA messages
        :param cx_rx_sar_error: Received Cx SAR messages failed
        :param swx_rx_sar_error: Received SWx SAR messages failed
        :param swx_tx_maa: Transmitted SWx MAA messages
        :param swx_tx_saa: Transmitted SWx SAA messages
        :param hss_imsi: Number of IMSIs attached to HSS
        :param hss_impi: Number of IMPIs attached to HSS
        :param hss_impu: Number of IMPUs attached to HSS
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
        self.cx_rx_lir = cx_rx_lir
        self.cx_rx_uar = cx_rx_uar
        self.cx_tx_lia = cx_tx_lia
        self.cx_rx_unknown = cx_rx_unknown
        self.cx_rx_sar = cx_rx_sar
        self.s6a_rx_pur = s6a_rx_pur
        self.swx_rx_mar_error = swx_rx_mar_error
        self.cx_tx_uaa = cx_tx_uaa
        self.s6a_rx_pur_error = s6a_rx_pur_error
        self.s6a_tx_clr = s6a_tx_clr
        self.cx_tx_saa = cx_tx_saa
        self.cx_rx_lir_error = cx_rx_lir_error
        self.s6a_rx_ulr = s6a_rx_ulr
        self.s6a_rx_cla = s6a_rx_cla
        self.s6a_rx_cla_error = s6a_rx_cla_error
        self.s6a_rx_air = s6a_rx_air
        self.cx_rx_mar = cx_rx_mar
        self.swx_rx_sar = swx_rx_sar
        self.s6a_rx_air_error = s6a_rx_air_error
        self.s6a_rx_ida_error = s6a_rx_ida_error
        self.cx_tx_maa = cx_tx_maa
        self.swx_rx_mar = swx_rx_mar
        self.s6a_rx_unknown = s6a_rx_unknown
        self.s6a_tx_pua = s6a_tx_pua
        self.swx_rx_unknown = swx_rx_unknown
        self.cx_rx_mar_error = cx_rx_mar_error
        self.cx_rx_uar_error = cx_rx_uar_error
        self.s6a_tx_ula = s6a_tx_ula
        self.s6a_rx_ulr_error = s6a_rx_ulr_error
        self.s6a_tx_aia = s6a_tx_aia
        self.s6a_tx_idr = s6a_tx_idr
        self.s6a_rx_ida = s6a_rx_ida
        self.cx_rx_sar_error = cx_rx_sar_error
        self.swx_rx_sar_error = swx_rx_sar_error
        self.swx_tx_maa = swx_tx_maa
        self.swx_tx_saa = swx_tx_saa
        self.hss_imsi = hss_imsi
        self.hss_impi = hss_impi
        self.hss_impu = hss_impu
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
        record_str = (f"{ts},{ip},{self.cx_rx_lir},{self.cx_rx_uar},{self.cx_tx_lia},{self.cx_rx_unknown},"
                      f"{self.cx_rx_sar},{self.s6a_rx_pur},{self.swx_rx_mar_error},{self.cx_tx_uaa},"
                      f"{self.s6a_rx_pur_error},{self.s6a_tx_clr},{self.cx_tx_saa},{self.cx_rx_lir_error},"
                      f"{self.s6a_rx_ulr},{self.s6a_rx_cla},{self.s6a_rx_cla_error},{self.s6a_rx_air},"
                      f"{self.cx_rx_mar},{self.swx_rx_sar},{self.s6a_rx_air_error},{self.s6a_rx_ida_error},"
                      f"{self.cx_tx_maa},{self.swx_rx_mar},{self.s6a_rx_unknown},{self.s6a_tx_pua},"
                      f"{self.swx_rx_unknown},{self.cx_rx_mar_error},{self.cx_rx_uar_error},{self.s6a_tx_ula},"
                      f"{self.s6a_rx_ulr_error},{self.s6a_tx_aia},{self.s6a_tx_idr},{self.s6a_rx_ida},"
                      f"{self.cx_rx_sar_error},{self.swx_rx_sar_error},{self.swx_tx_maa},{self.swx_tx_saa},"
                      f"{self.hss_imsi},{self.hss_impi},{self.hss_impu},"
                      f"{self.process_max_fds},{self.process_virtual_memory_max_bytes},"
                      f"{self.process_cpu_seconds_total},{self.process_virtual_memory_bytes},"
                      f"{self.process_resident_memory_bytes},{self.process_start_time_seconds},"
                      f"{self.process_open_fds}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCoreHSSMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCoreHSSMetrics(ip=parts[1], ts=float(parts[0]),
                                  cx_rx_lir=int(parts[2]), cx_rx_uar=int(parts[3]), cx_tx_lia=int(parts[4]),
                                  cx_rx_unknown=int(parts[5]), cx_rx_sar=int(parts[6]), s6a_rx_pur=int(parts[7]),
                                  swx_rx_mar_error=int(parts[8]), cx_tx_uaa=int(parts[9]),
                                  s6a_rx_pur_error=int(parts[10]),
                                  s6a_tx_clr=int(parts[11]), cx_tx_saa=int(parts[12]), cx_rx_lir_error=int(parts[13]),
                                  s6a_rx_ulr=int(parts[14]), s6a_rx_cla=int(parts[15]), s6a_rx_cla_error=int(parts[16]),
                                  s6a_rx_air=int(parts[17]), cx_rx_mar=int(parts[18]), swx_rx_sar=int(parts[19]),
                                  s6a_rx_air_error=int(parts[20]), s6a_rx_ida_error=int(parts[21]),
                                  cx_tx_maa=int(parts[22]),
                                  swx_rx_mar=int(parts[23]), s6a_rx_unknown=int(parts[24]), s6a_tx_pua=int(parts[25]),
                                  swx_rx_unknown=int(parts[26]), cx_rx_mar_error=int(parts[27]),
                                  cx_rx_uar_error=int(parts[28]),
                                  s6a_tx_ula=int(parts[29]), s6a_rx_ulr_error=int(parts[30]), s6a_tx_aia=int(parts[31]),
                                  s6a_tx_idr=int(parts[32]), s6a_rx_ida=int(parts[33]), cx_rx_sar_error=int(parts[34]),
                                  swx_rx_sar_error=int(parts[35]), swx_tx_maa=int(parts[36]), swx_tx_saa=int(parts[37]),
                                  hss_imsi=int(parts[38]), hss_impi=int(parts[39]), hss_impu=int(parts[40]),
                                  process_max_fds=int(parts[41]), process_virtual_memory_max_bytes=int(parts[42]),
                                  process_cpu_seconds_total=int(parts[43]), process_virtual_memory_bytes=int(parts[44]),
                                  process_resident_memory_bytes=int(parts[45]),
                                  process_start_time_seconds=int(parts[46]),
                                  process_open_fds=int(parts[47]))
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
            self.cx_rx_lir = int(parts[2])
            self.cx_rx_uar = int(parts[3])
            self.cx_tx_lia = int(parts[4])
            self.cx_rx_unknown = int(parts[5])
            self.cx_rx_sar = int(parts[6])
            self.s6a_rx_pur = int(parts[7])
            self.swx_rx_mar_error = int(parts[8])
            self.cx_tx_uaa = int(parts[9])
            self.s6a_rx_pur_error = int(parts[10])
            self.s6a_tx_clr = int(parts[11])
            self.cx_tx_saa = int(parts[12])
            self.cx_rx_lir_error = int(parts[13])
            self.s6a_rx_ulr = int(parts[14])
            self.s6a_rx_cla = int(parts[15])
            self.s6a_rx_cla_error = int(parts[16])
            self.s6a_rx_air = int(parts[17])
            self.cx_rx_mar = int(parts[18])
            self.swx_rx_sar = int(parts[19])
            self.s6a_rx_air_error = int(parts[20])
            self.s6a_rx_ida_error = int(parts[21])
            self.cx_tx_maa = int(parts[22])
            self.swx_rx_mar = int(parts[23])
            self.s6a_rx_unknown = int(parts[24])
            self.s6a_tx_pua = int(parts[25])
            self.swx_rx_unknown = int(parts[26])
            self.cx_rx_mar_error = int(parts[27])
            self.cx_rx_uar_error = int(parts[28])
            self.s6a_tx_ula = int(parts[29])
            self.s6a_rx_ulr_error = int(parts[30])
            self.s6a_tx_aia = int(parts[31])
            self.s6a_tx_idr = int(parts[32])
            self.s6a_rx_ida = int(parts[33])
            self.cx_rx_sar_error = int(parts[34])
            self.swx_rx_sar_error = int(parts[35])
            self.swx_tx_maa = int(parts[36])
            self.swx_tx_saa = int(parts[37])
            self.hss_imsi = int(parts[38])
            self.hss_impi = int(parts[39])
            self.hss_impu = int(parts[40])
            self.process_max_fds = int(parts[41])
            self.process_virtual_memory_max_bytes = int(parts[42])
            self.process_cpu_seconds_total = int(parts[43])
            self.process_virtual_memory_bytes = int(parts[44])
            self.process_resident_memory_bytes = int(parts[45])
            self.process_start_time_seconds = int(parts[46])
            self.process_open_fds = int(parts[47])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"cx_rx_lir: {self.cx_rx_lir}, cx_rx_uar: {self.cx_rx_uar}, "
                f"cx_tx_lia: {self.cx_tx_lia}, cx_rx_unknown: {self.cx_rx_unknown}, "
                f"cx_rx_sar: {self.cx_rx_sar}, s6a_rx_pur: {self.s6a_rx_pur}, "
                f"swx_rx_mar_error: {self.swx_rx_mar_error}, cx_tx_uaa: {self.cx_tx_uaa}, "
                f"s6a_rx_pur_error: {self.s6a_rx_pur_error}, s6a_tx_clr: {self.s6a_tx_clr}, "
                f"cx_tx_saa: {self.cx_tx_saa}, cx_rx_lir_error: {self.cx_rx_lir_error}, "
                f"s6a_rx_ulr: {self.s6a_rx_ulr}, s6a_rx_cla: {self.s6a_rx_cla}, "
                f"s6a_rx_cla_error: {self.s6a_rx_cla_error}, s6a_rx_air: {self.s6a_rx_air}, "
                f"cx_rx_mar: {self.cx_rx_mar}, swx_rx_sar: {self.swx_rx_sar}, "
                f"s6a_rx_air_error: {self.s6a_rx_air_error}, s6a_rx_ida_error: {self.s6a_rx_ida_error}, "
                f"cx_tx_maa: {self.cx_tx_maa}, swx_rx_mar: {self.swx_rx_mar}, "
                f"s6a_rx_unknown: {self.s6a_rx_unknown}, s6a_tx_pua: {self.s6a_tx_pua}, "
                f"swx_rx_unknown: {self.swx_rx_unknown}, cx_rx_mar_error: {self.cx_rx_mar_error}, "
                f"cx_rx_uar_error: {self.cx_rx_uar_error}, s6a_tx_ula: {self.s6a_tx_ula}, "
                f"s6a_rx_ulr_error: {self.s6a_rx_ulr_error}, s6a_tx_aia: {self.s6a_tx_aia}, "
                f"s6a_tx_idr: {self.s6a_tx_idr}, s6a_rx_ida: {self.s6a_rx_ida}, "
                f"cx_rx_sar_error: {self.cx_rx_sar_error}, swx_rx_sar_error: {self.swx_rx_sar_error}, "
                f"swx_tx_maa: {self.swx_tx_maa}, swx_tx_saa: {self.swx_tx_saa}, "
                f"hss_imsi: {self.hss_imsi}, hss_impi: {self.hss_impi}, hss_impu: {self.hss_impu}, "
                f"process_max_fds: {self.process_max_fds}, "
                f"process_virtual_memory_max_bytes: {self.process_virtual_memory_max_bytes}, "
                f"process_cpu_seconds_total: {self.process_cpu_seconds_total}, "
                f"process_virtual_memory_bytes: {self.process_virtual_memory_bytes}, "
                f"process_resident_memory_bytes: {self.process_resident_memory_bytes}, "
                f"process_start_time_seconds: {self.process_start_time_seconds}, "
                f"process_open_fds: {self.process_open_fds}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCoreHSSMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCoreHSSMetrics(ip=d["ip"], ts=d["ts"],
                                  cx_rx_lir=d["cx_rx_lir"], cx_rx_uar=d["cx_rx_uar"], cx_tx_lia=d["cx_tx_lia"],
                                  cx_rx_unknown=d["cx_rx_unknown"], cx_rx_sar=d["cx_rx_sar"],
                                  s6a_rx_pur=d["s6a_rx_pur"],
                                  swx_rx_mar_error=d["swx_rx_mar_error"], cx_tx_uaa=d["cx_tx_uaa"],
                                  s6a_rx_pur_error=d["s6a_rx_pur_error"], s6a_tx_clr=d["s6a_tx_clr"],
                                  cx_tx_saa=d["cx_tx_saa"],
                                  cx_rx_lir_error=d["cx_rx_lir_error"], s6a_rx_ulr=d["s6a_rx_ulr"],
                                  s6a_rx_cla=d["s6a_rx_cla"],
                                  s6a_rx_cla_error=d["s6a_rx_cla_error"], s6a_rx_air=d["s6a_rx_air"],
                                  cx_rx_mar=d["cx_rx_mar"],
                                  swx_rx_sar=d["swx_rx_sar"], s6a_rx_air_error=d["s6a_rx_air_error"],
                                  s6a_rx_ida_error=d["s6a_rx_ida_error"], cx_tx_maa=d["cx_tx_maa"],
                                  swx_rx_mar=d["swx_rx_mar"],
                                  s6a_rx_unknown=d["s6a_rx_unknown"], s6a_tx_pua=d["s6a_tx_pua"],
                                  swx_rx_unknown=d["swx_rx_unknown"], cx_rx_mar_error=d["cx_rx_mar_error"],
                                  cx_rx_uar_error=d["cx_rx_uar_error"], s6a_tx_ula=d["s6a_tx_ula"],
                                  s6a_rx_ulr_error=d["s6a_rx_ulr_error"], s6a_tx_aia=d["s6a_tx_aia"],
                                  s6a_tx_idr=d["s6a_tx_idr"],
                                  s6a_rx_ida=d["s6a_rx_ida"], cx_rx_sar_error=d["cx_rx_sar_error"],
                                  swx_rx_sar_error=d["swx_rx_sar_error"], swx_tx_maa=d["swx_tx_maa"],
                                  swx_tx_saa=d["swx_tx_saa"], hss_imsi=d["hss_imsi"], hss_impi=d["hss_impi"],
                                  hss_impu=d["hss_impu"], process_max_fds=d["process_max_fds"],
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
        d["cx_rx_lir"] = self.cx_rx_lir
        d["cx_rx_uar"] = self.cx_rx_uar
        d["cx_tx_lia"] = self.cx_tx_lia
        d["cx_rx_unknown"] = self.cx_rx_unknown
        d["cx_rx_sar"] = self.cx_rx_sar
        d["s6a_rx_pur"] = self.s6a_rx_pur
        d["swx_rx_mar_error"] = self.swx_rx_mar_error
        d["cx_tx_uaa"] = self.cx_tx_uaa
        d["s6a_rx_pur_error"] = self.s6a_rx_pur_error
        d["s6a_tx_clr"] = self.s6a_tx_clr
        d["cx_tx_saa"] = self.cx_tx_saa
        d["cx_rx_lir_error"] = self.cx_rx_lir_error
        d["s6a_rx_ulr"] = self.s6a_rx_ulr
        d["s6a_rx_cla"] = self.s6a_rx_cla
        d["s6a_rx_cla_error"] = self.s6a_rx_cla_error
        d["s6a_rx_air"] = self.s6a_rx_air
        d["cx_rx_mar"] = self.cx_rx_mar
        d["swx_rx_sar"] = self.swx_rx_sar
        d["s6a_rx_air_error"] = self.s6a_rx_air_error
        d["s6a_rx_ida_error"] = self.s6a_rx_ida_error
        d["cx_tx_maa"] = self.cx_tx_maa
        d["swx_rx_mar"] = self.swx_rx_mar
        d["s6a_rx_unknown"] = self.s6a_rx_unknown
        d["s6a_tx_pua"] = self.s6a_tx_pua
        d["swx_rx_unknown"] = self.swx_rx_unknown
        d["cx_rx_mar_error"] = self.cx_rx_mar_error
        d["cx_rx_uar_error"] = self.cx_rx_uar_error
        d["s6a_tx_ula"] = self.s6a_tx_ula
        d["s6a_rx_ulr_error"] = self.s6a_rx_ulr_error
        d["s6a_tx_aia"] = self.s6a_tx_aia
        d["s6a_tx_idr"] = self.s6a_tx_idr
        d["s6a_rx_ida"] = self.s6a_rx_ida
        d["cx_rx_sar_error"] = self.cx_rx_sar_error
        d["swx_rx_sar_error"] = self.swx_rx_sar_error
        d["swx_tx_maa"] = self.swx_tx_maa
        d["swx_tx_saa"] = self.swx_tx_saa
        d["hss_imsi"] = self.hss_imsi
        d["hss_impi"] = self.hss_impi
        d["hss_impu"] = self.hss_impu
        d["process_max_fds"] = self.process_max_fds
        d["process_virtual_memory_max_bytes"] = self.process_virtual_memory_max_bytes
        d["process_cpu_seconds_total"] = self.process_cpu_seconds_total
        d["process_virtual_memory_bytes"] = self.process_virtual_memory_bytes
        d["process_resident_memory_bytes"] = self.process_resident_memory_bytes
        d["process_start_time_seconds"] = self.process_start_time_seconds
        d["process_open_fds"] = self.process_open_fds
        return d

    def copy(self) -> "FiveGCoreHSSMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCoreHSSMetrics.from_dict(self.to_dict())
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 48

    @staticmethod
    def schema() -> "FiveGCoreHSSMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCoreHSSMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCoreHSSMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCoreHSSMetrics.from_dict(json.loads(json_str))
