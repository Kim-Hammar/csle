from typing import Dict, Any, Union
import time
import csle_collector.constants.constants as constants
from csle_base.json_serializable import JSONSerializable


class FiveGCoreAMFMetrics(JSONSerializable):
    """
    DTO class containing 5G core metrics related to the AMF service
    """

    def __init__(self, gnb: int = 0, fivegs_amffunction_mm_confupdate: int = 0,
                 fivegs_amffunction_rm_reginitreq: int = 0,
                 fivegs_amffunction_rm_regemergreq: int = 0, fivegs_amffunction_mm_paging5greq: int = 0,
                 fivegs_amffunction_rm_regperiodreq: int = 0, fivegs_amffunction_mm_confupdatesucc: int = 0,
                 fivegs_amffunction_rm_reginitsucc: int = 0, fivegs_amffunction_amf_authreject: int = 0,
                 fivegs_amffunction_rm_regmobreq: int = 0, amf_session: int = 0,
                 fivegs_amffunction_rm_regmobsucc: int = 0,
                 fivegs_amffunction_amf_authreq: int = 0, fivegs_amffunction_rm_regemergsucc: int = 0,
                 fivegs_amffunction_mm_paging5gsucc: int = 0, ran_ue: int = 0,
                 fivegs_amffunction_rm_regperiodsucc: int = 0,
                 process_max_fds: int = 0, process_virtual_memory_max_bytes: int = 0,
                 process_cpu_seconds_total: int = 0,
                 process_virtual_memory_bytes: int = 0, process_resident_memory_bytes: int = 0,
                 process_start_time_seconds: int = 0,
                 process_open_fds: int = 0, ip: Union[None, str] = None, ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param gnb: Number of gnbs
        :param fivegs_amffunction_mm_confupdate: Number of UE Configuration Update commands requested by the AMF
        :param fivegs_amffunction_rm_reginitreq: Number of initial registration requests received by the AMF
        :param fivegs_amffunction_rm_regemergreq: Number of emergency registration requests received by the AMF
        :param fivegs_amffunction_mm_paging5greq: Number of 5G paging procedures initiated at the AMF
        :param fivegs_amffunction_rm_regperiodreq: Number of periodic registration update requests received by the AMF
        :param fivegs_amffunction_mm_confupdatesucc: Number of UE Configuration Update complete messages
                                                     received by the AMF
        :param fivegs_amffunction_rm_reginitsucc: Number of successful initial registrations at the AMF
        :param fivegs_amffunction_amf_authreject: Number of authentication rejections sent by the AMF
        :param fivegs_amffunction_rm_regmobreq: Number of mobility registration update requests received by the AMF
        :param amf_session: AMF Sessions
        :param fivegs_amffunction_rm_regmobsucc: Number of successful mobility registration updates at the AMF
        :param fivegs_amffunction_amf_authreq: Number of authentication requests sent by the AMF
        :param fivegs_amffunction_rm_regemergsucc: Number of successful emergency registrations at the AMF
        :param fivegs_amffunction_mm_paging5gsucc: Number of successful 5G paging procedures initiated at the AMF
        :param ran_ue: gauge
        :param fivegs_amffunction_rm_regperiodsucc: Number of successful periodic registration
                                                    update requests at the AMF
        :param process_max_fds: Maximum number of open file descriptors.
        :param process_virtual_memory_max_bytes: Maximum amount of virtual memory available in bytes.
        :param process_cpu_seconds_total: Total user and system CPU time spent in seconds.
        :param process_virtual_memory_bytes: Virtual memory size in bytes.
        :param process_resident_memory_bytes: Resident memory size in bytes.
        :param process_start_time_seconds: Start time of the process since unix epoch in seconds.
        :param process_open_fds: Number of open file descriptors.
        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        """
        self.gnb = gnb
        self.fivegs_amffunction_mm_confupdate = fivegs_amffunction_mm_confupdate
        self.fivegs_amffunction_rm_reginitreq = fivegs_amffunction_rm_reginitreq
        self.fivegs_amffunction_rm_regemergreq = fivegs_amffunction_rm_regemergreq
        self.fivegs_amffunction_mm_paging5greq = fivegs_amffunction_mm_paging5greq
        self.fivegs_amffunction_rm_regperiodreq = fivegs_amffunction_rm_regperiodreq
        self.fivegs_amffunction_mm_confupdatesucc = fivegs_amffunction_mm_confupdatesucc
        self.fivegs_amffunction_rm_reginitsucc = fivegs_amffunction_rm_reginitsucc
        self.fivegs_amffunction_amf_authreject = fivegs_amffunction_amf_authreject
        self.fivegs_amffunction_rm_regmobreq = fivegs_amffunction_rm_regmobreq
        self.amf_session = amf_session
        self.fivegs_amffunction_rm_regmobsucc = fivegs_amffunction_rm_regmobsucc
        self.fivegs_amffunction_amf_authreq = fivegs_amffunction_amf_authreq
        self.fivegs_amffunction_rm_regemergsucc = fivegs_amffunction_rm_regemergsucc
        self.fivegs_amffunction_mm_paging5gsucc = fivegs_amffunction_mm_paging5gsucc
        self.ran_ue = ran_ue
        self.fivegs_amffunction_rm_regperiodsucc = fivegs_amffunction_rm_regperiodsucc
        self.process_max_fds = process_max_fds
        self.process_virtual_memory_max_bytes = process_virtual_memory_max_bytes
        self.process_cpu_seconds_total = process_cpu_seconds_total
        self.process_virtual_memory_bytes = process_virtual_memory_bytes
        self.process_resident_memory_bytes = process_resident_memory_bytes
        self.process_start_time_seconds = process_start_time_seconds
        self.process_open_fds = process_open_fds
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = time.time()
        record_str = (f"{ts},{ip},{self.gnb},{self.fivegs_amffunction_mm_confupdate},"
                      f"{self.fivegs_amffunction_rm_reginitreq},{self.fivegs_amffunction_rm_regemergreq},"
                      f"{self.fivegs_amffunction_mm_paging5greq},{self.fivegs_amffunction_rm_regperiodreq},"
                      f"{self.fivegs_amffunction_mm_confupdatesucc},{self.fivegs_amffunction_rm_reginitsucc},"
                      f"{self.fivegs_amffunction_amf_authreject}, {self.fivegs_amffunction_rm_regmobreq},"
                      f"{self.amf_session},{self.fivegs_amffunction_rm_regmobsucc},"
                      f"{self.fivegs_amffunction_amf_authreq},{self.fivegs_amffunction_rm_regemergsucc},"
                      f"{self.fivegs_amffunction_mm_paging5gsucc},{self.ran_ue},"
                      f"{self.fivegs_amffunction_rm_regperiodsucc},{self.process_max_fds},"
                      f"{self.process_virtual_memory_max_bytes},{self.process_cpu_seconds_total},"
                      f"{self.process_virtual_memory_bytes},{self.process_resident_memory_bytes},"
                      f"{self.process_start_time_seconds},{self.process_open_fds}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCoreAMFMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCoreAMFMetrics(
            ip=parts[1], ts=float(parts[0]), fivegs_amffunction_mm_confupdate=int(parts[2]),
            fivegs_amffunction_rm_reginitreq=int(parts[3]), fivegs_amffunction_rm_regemergreq=int(parts[4]),
            fivegs_amffunction_mm_paging5greq=int(parts[5]), fivegs_amffunction_rm_regperiodreq=int(parts[6]),
            fivegs_amffunction_mm_confupdatesucc=int(parts[7]), fivegs_amffunction_rm_reginitsucc=int(parts[8]),
            fivegs_amffunction_amf_authreject=int(parts[9]), fivegs_amffunction_rm_regmobreq=int(parts[10]),
            amf_session=int(parts[11]), fivegs_amffunction_rm_regmobsucc=int(parts[12]),
            fivegs_amffunction_amf_authreq=int(parts[13]), fivegs_amffunction_rm_regemergsucc=int(parts[14]),
            fivegs_amffunction_mm_paging5gsucc=int(parts[15]), ran_ue=int(parts[16]),
            fivegs_amffunction_rm_regperiodsucc=int(parts[17]), process_max_fds=int(parts[18]),
            process_virtual_memory_max_bytes=int(parts[19]), process_cpu_seconds_total=int(parts[20]),
            process_virtual_memory_bytes=int(parts[21]), process_resident_memory_bytes=int(parts[22]),
            process_start_time_seconds=int(parts[23]), process_open_fds=int(parts[24])
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
            self.ip = parts[1]
            self.ts = float(parts[0])
            self.fivegs_amffunction_mm_confupdate = int(parts[2])
            self.fivegs_amffunction_rm_reginitreq = int(parts[3])
            self.fivegs_amffunction_rm_regemergreq = int(parts[4])
            self.fivegs_amffunction_mm_paging5greq = int(parts[5])
            self.fivegs_amffunction_rm_regperiodreq = int(parts[6])
            self.fivegs_amffunction_mm_confupdatesucc = int(parts[7])
            self.fivegs_amffunction_rm_reginitsucc = int(parts[8])
            self.fivegs_amffunction_amf_authreject = int(parts[9])
            self.fivegs_amffunction_rm_regmobreq = int(parts[10])
            self.amf_session = int(parts[11])
            self.fivegs_amffunction_rm_regmobsucc = int(parts[12])
            self.fivegs_amffunction_amf_authreq = int(parts[13])
            self.fivegs_amffunction_rm_regemergsucc = int(parts[14])
            self.fivegs_amffunction_mm_paging5gsucc = int(parts[15])
            self.ran_ue = int(parts[16])
            self.fivegs_amffunction_rm_regperiodsucc = int(parts[17])
            self.process_max_fds = int(parts[18])
            self.process_virtual_memory_max_bytes = int(parts[19])
            self.process_cpu_seconds_total = int(parts[20])
            self.process_virtual_memory_bytes = int(parts[21])
            self.process_resident_memory_bytes = int(parts[2])
            self.process_start_time_seconds = int(parts[23])
            self.process_open_fds = int(parts[24])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"gnb: {self.gnb}, "
                f"fivegs_amffunction_mm_confupdate: {self.fivegs_amffunction_mm_confupdate}"
                f"fivegs_amffunction_rm_reginitreq: {self.fivegs_amffunction_rm_reginitreq}"
                f"fivegs_amffunction_rm_regemergreq: {self.fivegs_amffunction_rm_regemergreq}"
                f"fivegs_amffunction_mm_paging5greq: {self.fivegs_amffunction_mm_paging5greq}"
                f"fivegs_amffunction_rm_regperiodreq: {self.fivegs_amffunction_rm_regperiodreq}"
                f"fivegs_amffunction_mm_confupdatesucc: {self.fivegs_amffunction_mm_confupdatesucc}"
                f"fivegs_amffunction_rm_reginitsucc: {self.fivegs_amffunction_rm_reginitsucc}"
                f"fivegs_amffunction_amf_authreject: {self.fivegs_amffunction_amf_authreject}"
                f"fivegs_amffunction_rm_regmobreq: {self.fivegs_amffunction_rm_regmobreq}"
                f"amf_session: {self.amf_session}"
                f"fivegs_amffunction_rm_regmobsucc: {self.fivegs_amffunction_rm_regmobsucc}"
                f"fivegs_amffunction_amf_authreq: {self.fivegs_amffunction_amf_authreq}"
                f"fivegs_amffunction_rm_regemergsucc: {self.fivegs_amffunction_rm_regemergsucc}"
                f"fivegs_amffunction_mm_paging5gsucc: {self.fivegs_amffunction_mm_paging5gsucc}"
                f"ran_ue: {self.ran_ue}"
                f"fivegs_amffunction_rm_regperiodsucc: {self.fivegs_amffunction_rm_regperiodsucc}"
                f"process_max_fds: {self.process_max_fds}"
                f"process_virtual_memory_max_bytes: {self.process_virtual_memory_max_bytes}"
                f"process_cpu_seconds_total: {self.process_cpu_seconds_total}"
                f"process_virtual_memory_bytes: {self.process_virtual_memory_bytes}"
                f"process_resident_memory_bytes: {self.process_resident_memory_bytes}"
                f"process_start_time_seconds: {self.process_start_time_seconds}"
                f"process_open_fds: {self.process_open_fds}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCoreAMFMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCoreAMFMetrics(
            ip=d[constants.FIVE_G_CORE.IP],
            ts=d[constants.FIVE_G_CORE.TS],
            fivegs_amffunction_mm_confupdate=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_CONFUPDATE],
            fivegs_amffunction_rm_reginitreq=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGINITREQ],
            fivegs_amffunction_rm_regemergreq=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGEMERGREQ],
            fivegs_amffunction_mm_paging5greq=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_PAGING5GREQ],
            fivegs_amffunction_rm_regperiodreq=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGPERIODREQ],
            fivegs_amffunction_mm_confupdatesucc=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_CONFUPDATESUCC],
            fivegs_amffunction_rm_reginitsucc=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGINITSUCC],
            fivegs_amffunction_amf_authreject=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_AMF_AUTHREJECT],
            fivegs_amffunction_rm_regmobreq=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGMOBREQ],
            amf_session=d[constants.FIVE_G_CORE.AMF_SESSION],
            fivegs_amffunction_rm_regmobsucc=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGMOBSUCC],
            fivegs_amffunction_amf_authreq=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_AMF_AUTHREQ],
            fivegs_amffunction_rm_regemergsucc=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGEMERGSUCC],
            fivegs_amffunction_mm_paging5gsucc=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_PAGING5GSUCC],
            ran_ue=d[constants.FIVE_G_CORE.RAN_UE],
            fivegs_amffunction_rm_regperiodsucc=d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGPERIODSUCC],
            process_max_fds=d[constants.FIVE_G_CORE.PROCESS_MAX_FDS],
            process_virtual_memory_max_bytes=d[constants.FIVE_G_CORE.PROCESS_VIRTUAL_MEMORY_MAX_BYTES],
            process_cpu_seconds_total=d[constants.FIVE_G_CORE.PROCESS_CPU_SECONDS_TOTAL],
            process_virtual_memory_bytes=d[constants.FIVE_G_CORE.PROCESS_VIRTUAL_MEMORY_BYTES],
            process_resident_memory_bytes=d[constants.FIVE_G_CORE.PROCESS_RESIDENT_MEMORY_BYTES],
            process_start_time_seconds=d[constants.FIVE_G_CORE.PROCESS_START_TIME_SECONDS],
            process_open_fds=d[constants.FIVE_G_CORE.PROCESS_OPEN_FDS])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d: Dict[str, Any] = {}
        d[constants.FIVE_G_CORE.TS] = self.ts
        d[constants.FIVE_G_CORE.IP] = self.ip
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_CONFUPDATE] = self.fivegs_amffunction_mm_confupdate
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGINITREQ] = self.fivegs_amffunction_rm_reginitreq
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGEMERGREQ] = self.fivegs_amffunction_rm_regemergreq
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_PAGING5GREQ] = self.fivegs_amffunction_mm_paging5greq
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGPERIODREQ] = self.fivegs_amffunction_rm_regperiodreq
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_CONFUPDATESUCC] = self.fivegs_amffunction_mm_confupdatesucc
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGINITSUCC] = self.fivegs_amffunction_rm_reginitsucc
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_AMF_AUTHREJECT] = self.fivegs_amffunction_amf_authreject
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGMOBREQ] = self.fivegs_amffunction_rm_regmobreq
        d[constants.FIVE_G_CORE.AMF_SESSION] = self.amf_session
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGMOBSUCC] = self.fivegs_amffunction_rm_regmobsucc
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_AMF_AUTHREQ] = self.fivegs_amffunction_amf_authreq
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGEMERGSUCC] = self.fivegs_amffunction_rm_regemergsucc
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_MM_PAGING5GSUCC] = self.fivegs_amffunction_mm_paging5gsucc
        d[constants.FIVE_G_CORE.RAN_UE] = self.ran_ue
        d[constants.FIVE_G_CORE.FIVEGS_AMFFUNCTION_RM_REGPERIODSUCC] = self.fivegs_amffunction_rm_regperiodsucc
        d[constants.FIVE_G_CORE.PROCESS_MAX_FDS] = self.process_max_fds
        d[constants.FIVE_G_CORE.PROCESS_VIRTUAL_MEMORY_MAX_BYTES] = self.process_virtual_memory_max_bytes
        d[constants.FIVE_G_CORE.PROCESS_CPU_SECONDS_TOTAL] = self.process_cpu_seconds_total
        d[constants.FIVE_G_CORE.PROCESS_VIRTUAL_MEMORY_BYTES] = self.process_virtual_memory_bytes
        d[constants.FIVE_G_CORE.PROCESS_RESIDENT_MEMORY_BYTES] = self.process_resident_memory_bytes
        d[constants.FIVE_G_CORE.PROCESS_START_TIME_SECONDS] = self.process_start_time_seconds
        d[constants.FIVE_G_CORE.PROCESS_OPEN_FDS] = self.process_open_fds
        return d

    def copy(self) -> "FiveGCoreAMFMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCoreAMFMetrics(
            ip=self.ip, ts=self.ts, fivegs_amffunction_mm_confupdate=self.fivegs_amffunction_mm_confupdate,
            fivegs_amffunction_rm_reginitreq=self.fivegs_amffunction_rm_reginitreq,
            fivegs_amffunction_rm_regemergreq=self.fivegs_amffunction_rm_regemergreq,
            fivegs_amffunction_mm_paging5greq=self.fivegs_amffunction_mm_paging5greq,
            fivegs_amffunction_rm_regperiodreq=self.fivegs_amffunction_rm_regperiodreq,
            fivegs_amffunction_mm_confupdatesucc=self.fivegs_amffunction_mm_confupdatesucc,
            fivegs_amffunction_rm_reginitsucc=self.fivegs_amffunction_rm_reginitsucc,
            fivegs_amffunction_amf_authreject=self.fivegs_amffunction_amf_authreject,
            fivegs_amffunction_rm_regmobreq=self.fivegs_amffunction_rm_regmobreq,
            amf_session=self.amf_session, fivegs_amffunction_rm_regmobsucc=self.fivegs_amffunction_rm_regmobsucc,
            fivegs_amffunction_amf_authreq=self.fivegs_amffunction_amf_authreq,
            fivegs_amffunction_rm_regemergsucc=self.fivegs_amffunction_rm_regemergsucc,
            fivegs_amffunction_mm_paging5gsucc=self.fivegs_amffunction_mm_paging5gsucc, ran_ue=self.ran_ue,
            fivegs_amffunction_rm_regperiodsucc=self.fivegs_amffunction_rm_regperiodsucc,
            process_max_fds=self.process_max_fds,
            process_virtual_memory_max_bytes=self.process_virtual_memory_max_bytes,
            process_cpu_seconds_total=self.process_cpu_seconds_total,
            process_virtual_memory_bytes=self.process_virtual_memory_bytes,
            process_resident_memory_bytes=self.process_resident_memory_bytes,
            process_start_time_seconds=self.process_start_time_seconds, process_open_fds=self.process_open_fds)
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 25

    @staticmethod
    def schema() -> "FiveGCoreAMFMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCoreAMFMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCoreAMFMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCoreAMFMetrics.from_dict(json.loads(json_str))
