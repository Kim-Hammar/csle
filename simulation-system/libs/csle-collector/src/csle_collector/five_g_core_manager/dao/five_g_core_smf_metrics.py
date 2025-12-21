from typing import Dict, Any, Union
import time
from csle_base.json_serializable import JSONSerializable


class FiveGCoreSMFMetrics(JSONSerializable):
    """
    DTO class containing 5G Core SMF metrics
    """

    def __init__(self, ip: Union[None, str] = None, ts: Union[float, None] = None,
                 gn_rx_createpdpcontextreq: int = 0, gn_rx_deletepdpcontextreq: int = 0,
                 gtp1_pdpctxs_active: int = 0, pfcp_peers_active: int = 0,
                 fivegs_smffunction_sm_n4sessionreport: int = 0, ues_active: int = 0,
                 gtp2_sessions_active: int = 0, pfcp_sessions_active: int = 0,
                 s5c_rx_createsession: int = 0, s5c_rx_deletesession: int = 0,
                 gtp_new_node_failed: int = 0, s5c_rx_parse_failed: int = 0,
                 fivegs_smffunction_sm_n4sessionreportsucc: int = 0,
                 fivegs_smffunction_sm_n4sessionestabreq: int = 0, bearers_active: int = 0,
                 gn_rx_parse_failed: int = 0, gtp_peers_active: int = 0,
                 fivegs_smffunction_sm_sessionnbr: int = 0,
                 fivegs_smffunction_sm_pdusessioncreationreq: int = 0,
                 fivegs_smffunction_sm_pdusessioncreationsucc: int = 0,
                 fivegs_smffunction_sm_qos_flow_nbr: int = 0,
                 fivegs_smffunction_sm_n4sessionestabfail: int = 0,
                 fivegs_smffunction_sm_pdusessioncreationfail: int = 0,
                 process_max_fds: int = 0, process_virtual_memory_max_bytes: int = 0,
                 process_cpu_seconds_total: int = 0, process_virtual_memory_bytes: int = 0,
                 process_resident_memory_bytes: int = 0, process_start_time_seconds: int = 0,
                 process_open_fds: int = 0) -> None:
        """
        Initializes the DTO

        :param ip: The IP of the core
        :param ts: The timestamp the metrics were measured
        :param gn_rx_createpdpcontextreq: Received GTPv1C CreatePDPContextRequest messages
        :param gn_rx_deletepdpcontextreq: Received GTPv1C DeletePDPContextRequest messages
        :param gtp1_pdpctxs_active: Active GTPv1 PDP Contexts (GGSN)
        :param pfcp_peers_active: Active PFCP peers
        :param fivegs_smffunction_sm_n4sessionreport: Number of requested N4 session reports evidented by SMF
        :param ues_active: Active User Equipments
        :param gtp2_sessions_active: Active GTPv2 Sessions (PGW)
        :param pfcp_sessions_active: Active PFCP Sessions
        :param s5c_rx_createsession: Received GTPv2C CreateSessionRequest messages
        :param s5c_rx_deletesession: Received GTPv2C DeleteSessionRequest messages
        :param gtp_new_node_failed: Unable to allocate new GTP (peer) Node
        :param s5c_rx_parse_failed: Received GTPv2C messages discarded due to parsing failure
        :param fivegs_smffunction_sm_n4sessionreportsucc: Number of successful N4 session reports evidented by SMF
        :param fivegs_smffunction_sm_n4sessionestabreq: Number of requested N4 session establishments evidented by SMF
        :param bearers_active: Active Bearers
        :param gn_rx_parse_failed: Received GTPv1C messages discarded due to parsing failure
        :param gtp_peers_active: Active GTP peers
        :param fivegs_smffunction_sm_sessionnbr: Active Sessions
        :param fivegs_smffunction_sm_pdusessioncreationreq: Number of PDU sessions requested to be created by the SMF
        :param fivegs_smffunction_sm_pdusessioncreationsucc: Number of PDU sessions successfully created by the SMF
        :param fivegs_smffunction_sm_qos_flow_nbr: Number of QoS flows at the SMF
        :param fivegs_smffunction_sm_n4sessionestabfail: Number of failed N4 session establishments
        :param fivegs_smffunction_sm_pdusessioncreationfail: Number of PDU sessions failed to be created
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
        self.gn_rx_createpdpcontextreq = gn_rx_createpdpcontextreq
        self.gn_rx_deletepdpcontextreq = gn_rx_deletepdpcontextreq
        self.gtp1_pdpctxs_active = gtp1_pdpctxs_active
        self.pfcp_peers_active = pfcp_peers_active
        self.fivegs_smffunction_sm_n4sessionreport = fivegs_smffunction_sm_n4sessionreport
        self.ues_active = ues_active
        self.gtp2_sessions_active = gtp2_sessions_active
        self.pfcp_sessions_active = pfcp_sessions_active
        self.s5c_rx_createsession = s5c_rx_createsession
        self.s5c_rx_deletesession = s5c_rx_deletesession
        self.gtp_new_node_failed = gtp_new_node_failed
        self.s5c_rx_parse_failed = s5c_rx_parse_failed
        self.fivegs_smffunction_sm_n4sessionreportsucc = fivegs_smffunction_sm_n4sessionreportsucc
        self.fivegs_smffunction_sm_n4sessionestabreq = fivegs_smffunction_sm_n4sessionestabreq
        self.bearers_active = bearers_active
        self.gn_rx_parse_failed = gn_rx_parse_failed
        self.gtp_peers_active = gtp_peers_active
        self.fivegs_smffunction_sm_sessionnbr = fivegs_smffunction_sm_sessionnbr
        self.fivegs_smffunction_sm_pdusessioncreationreq = fivegs_smffunction_sm_pdusessioncreationreq
        self.fivegs_smffunction_sm_pdusessioncreationsucc = fivegs_smffunction_sm_pdusessioncreationsucc
        self.fivegs_smffunction_sm_qos_flow_nbr = fivegs_smffunction_sm_qos_flow_nbr
        self.fivegs_smffunction_sm_n4sessionestabfail = fivegs_smffunction_sm_n4sessionestabfail
        self.fivegs_smffunction_sm_pdusessioncreationfail = fivegs_smffunction_sm_pdusessioncreationfail
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
        record_str = (f"{ts},{ip},{self.gn_rx_createpdpcontextreq},{self.gn_rx_deletepdpcontextreq},"
                      f"{self.gtp1_pdpctxs_active},{self.pfcp_peers_active},"
                      f"{self.fivegs_smffunction_sm_n4sessionreport},{self.ues_active},"
                      f"{self.gtp2_sessions_active},{self.pfcp_sessions_active},"
                      f"{self.s5c_rx_createsession},{self.s5c_rx_deletesession},"
                      f"{self.gtp_new_node_failed},{self.s5c_rx_parse_failed},"
                      f"{self.fivegs_smffunction_sm_n4sessionreportsucc},"
                      f"{self.fivegs_smffunction_sm_n4sessionestabreq},"
                      f"{self.bearers_active},{self.gn_rx_parse_failed},{self.gtp_peers_active},"
                      f"{self.fivegs_smffunction_sm_sessionnbr},{self.fivegs_smffunction_sm_pdusessioncreationreq},"
                      f"{self.fivegs_smffunction_sm_pdusessioncreationsucc},{self.fivegs_smffunction_sm_qos_flow_nbr},"
                      f"{self.fivegs_smffunction_sm_n4sessionestabfail},"
                      f"{self.fivegs_smffunction_sm_pdusessioncreationfail},"
                      f"{self.process_max_fds},{self.process_virtual_memory_max_bytes},"
                      f"{self.process_cpu_seconds_total},{self.process_virtual_memory_bytes},"
                      f"{self.process_resident_memory_bytes},{self.process_start_time_seconds},"
                      f"{self.process_open_fds}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCoreSMFMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGCoreSMFMetrics(ip=parts[1], ts=float(parts[0]),
                                  gn_rx_createpdpcontextreq=int(parts[2]),
                                  gn_rx_deletepdpcontextreq=int(parts[3]),
                                  gtp1_pdpctxs_active=int(parts[4]),
                                  pfcp_peers_active=int(parts[5]),
                                  fivegs_smffunction_sm_n4sessionreport=int(parts[6]),
                                  ues_active=int(parts[7]),
                                  gtp2_sessions_active=int(parts[8]),
                                  pfcp_sessions_active=int(parts[9]),
                                  s5c_rx_createsession=int(parts[10]),
                                  s5c_rx_deletesession=int(parts[11]),
                                  gtp_new_node_failed=int(parts[12]),
                                  s5c_rx_parse_failed=int(parts[13]),
                                  fivegs_smffunction_sm_n4sessionreportsucc=int(parts[14]),
                                  fivegs_smffunction_sm_n4sessionestabreq=int(parts[15]),
                                  bearers_active=int(parts[16]),
                                  gn_rx_parse_failed=int(parts[17]),
                                  gtp_peers_active=int(parts[18]),
                                  fivegs_smffunction_sm_sessionnbr=int(parts[19]),
                                  fivegs_smffunction_sm_pdusessioncreationreq=int(parts[20]),
                                  fivegs_smffunction_sm_pdusessioncreationsucc=int(parts[21]),
                                  fivegs_smffunction_sm_qos_flow_nbr=int(parts[22]),
                                  fivegs_smffunction_sm_n4sessionestabfail=int(parts[23]),
                                  fivegs_smffunction_sm_pdusessioncreationfail=int(parts[24]),
                                  process_max_fds=int(parts[25]),
                                  process_virtual_memory_max_bytes=int(parts[26]),
                                  process_cpu_seconds_total=int(parts[27]),
                                  process_virtual_memory_bytes=int(parts[28]),
                                  process_resident_memory_bytes=int(parts[29]),
                                  process_start_time_seconds=int(parts[30]),
                                  process_open_fds=int(parts[31]))
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
            self.gn_rx_createpdpcontextreq = int(parts[2])
            self.gn_rx_deletepdpcontextreq = int(parts[3])
            self.gtp1_pdpctxs_active = int(parts[4])
            self.pfcp_peers_active = int(parts[5])
            self.fivegs_smffunction_sm_n4sessionreport = int(parts[6])
            self.ues_active = int(parts[7])
            self.gtp2_sessions_active = int(parts[8])
            self.pfcp_sessions_active = int(parts[9])
            self.s5c_rx_createsession = int(parts[10])
            self.s5c_rx_deletesession = int(parts[11])
            self.gtp_new_node_failed = int(parts[12])
            self.s5c_rx_parse_failed = int(parts[13])
            self.fivegs_smffunction_sm_n4sessionreportsucc = int(parts[14])
            self.fivegs_smffunction_sm_n4sessionestabreq = int(parts[15])
            self.bearers_active = int(parts[16])
            self.gn_rx_parse_failed = int(parts[17])
            self.gtp_peers_active = int(parts[18])
            self.fivegs_smffunction_sm_sessionnbr = int(parts[19])
            self.fivegs_smffunction_sm_pdusessioncreationreq = int(parts[20])
            self.fivegs_smffunction_sm_pdusessioncreationsucc = int(parts[21])
            self.fivegs_smffunction_sm_qos_flow_nbr = int(parts[22])
            self.fivegs_smffunction_sm_n4sessionestabfail = int(parts[23])
            self.fivegs_smffunction_sm_pdusessioncreationfail = int(parts[24])
            self.process_max_fds = int(parts[25])
            self.process_virtual_memory_max_bytes = int(parts[26])
            self.process_cpu_seconds_total = int(parts[27])
            self.process_virtual_memory_bytes = int(parts[28])
            self.process_resident_memory_bytes = int(parts[29])
            self.process_start_time_seconds = int(parts[30])
            self.process_open_fds = int(parts[31])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, "
                f"gn_rx_createpdpcontextreq: {self.gn_rx_createpdpcontextreq}, "
                f"gn_rx_deletepdpcontextreq: {self.gn_rx_deletepdpcontextreq}, "
                f"gtp1_pdpctxs_active: {self.gtp1_pdpctxs_active}, "
                f"pfcp_peers_active: {self.pfcp_peers_active}, "
                f"fivegs_smffunction_sm_n4sessionreport: {self.fivegs_smffunction_sm_n4sessionreport}, "
                f"ues_active: {self.ues_active}, "
                f"gtp2_sessions_active: {self.gtp2_sessions_active}, "
                f"pfcp_sessions_active: {self.pfcp_sessions_active}, "
                f"s5c_rx_createsession: {self.s5c_rx_createsession}, "
                f"s5c_rx_deletesession: {self.s5c_rx_deletesession}, "
                f"gtp_new_node_failed: {self.gtp_new_node_failed}, "
                f"s5c_rx_parse_failed: {self.s5c_rx_parse_failed}, "
                f"fivegs_smffunction_sm_n4sessionreportsucc: {self.fivegs_smffunction_sm_n4sessionreportsucc}, "
                f"fivegs_smffunction_sm_n4sessionestabreq: {self.fivegs_smffunction_sm_n4sessionestabreq}, "
                f"bearers_active: {self.bearers_active}, "
                f"gn_rx_parse_failed: {self.gn_rx_parse_failed}, "
                f"gtp_peers_active: {self.gtp_peers_active}, "
                f"fivegs_smffunction_sm_sessionnbr: {self.fivegs_smffunction_sm_sessionnbr}, "
                f"fivegs_smffunction_sm_pdusessioncreationreq: {self.fivegs_smffunction_sm_pdusessioncreationreq}, "
                f"fivegs_smffunction_sm_pdusessioncreationsucc: {self.fivegs_smffunction_sm_pdusessioncreationsucc}, "
                f"fivegs_smffunction_sm_qos_flow_nbr: {self.fivegs_smffunction_sm_qos_flow_nbr}, "
                f"fivegs_smffunction_sm_n4sessionestabfail: {self.fivegs_smffunction_sm_n4sessionestabfail}, "
                f"fivegs_smffunction_sm_pdusessioncreationfail: {self.fivegs_smffunction_sm_pdusessioncreationfail}, "
                f"process_max_fds: {self.process_max_fds}, "
                f"process_virtual_memory_max_bytes: {self.process_virtual_memory_max_bytes}, "
                f"process_cpu_seconds_total: {self.process_cpu_seconds_total}, "
                f"process_virtual_memory_bytes: {self.process_virtual_memory_bytes}, "
                f"process_resident_memory_bytes: {self.process_resident_memory_bytes}, "
                f"process_start_time_seconds: {self.process_start_time_seconds}, "
                f"process_open_fds: {self.process_open_fds}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCoreSMFMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCoreSMFMetrics(ip=d["ip"], ts=d["ts"],
                                  gn_rx_createpdpcontextreq=d["gn_rx_createpdpcontextreq"],
                                  gn_rx_deletepdpcontextreq=d["gn_rx_deletepdpcontextreq"],
                                  gtp1_pdpctxs_active=d["gtp1_pdpctxs_active"],
                                  pfcp_peers_active=d["pfcp_peers_active"],
                                  fivegs_smffunction_sm_n4sessionreport=d["fivegs_smffunction_sm_n4sessionreport"],
                                  ues_active=d["ues_active"],
                                  gtp2_sessions_active=d["gtp2_sessions_active"],
                                  pfcp_sessions_active=d["pfcp_sessions_active"],
                                  s5c_rx_createsession=d["s5c_rx_createsession"],
                                  s5c_rx_deletesession=d["s5c_rx_deletesession"],
                                  gtp_new_node_failed=d["gtp_new_node_failed"],
                                  s5c_rx_parse_failed=d["s5c_rx_parse_failed"],
                                  fivegs_smffunction_sm_n4sessionreportsucc=d[
                                      "fivegs_smffunction_sm_n4sessionreportsucc"],
                                  fivegs_smffunction_sm_n4sessionestabreq=d["fivegs_smffunction_sm_n4sessionestabreq"],
                                  bearers_active=d["bearers_active"],
                                  gn_rx_parse_failed=d["gn_rx_parse_failed"],
                                  gtp_peers_active=d["gtp_peers_active"],
                                  fivegs_smffunction_sm_sessionnbr=d["fivegs_smffunction_sm_sessionnbr"],
                                  fivegs_smffunction_sm_pdusessioncreationreq=d[
                                      "fivegs_smffunction_sm_pdusessioncreationreq"],
                                  fivegs_smffunction_sm_pdusessioncreationsucc=d[
                                      "fivegs_smffunction_sm_pdusessioncreationsucc"],
                                  fivegs_smffunction_sm_qos_flow_nbr=d["fivegs_smffunction_sm_qos_flow_nbr"],
                                  fivegs_smffunction_sm_n4sessionestabfail=d[
                                      "fivegs_smffunction_sm_n4sessionestabfail"],
                                  fivegs_smffunction_sm_pdusessioncreationfail=d[
                                      "fivegs_smffunction_sm_pdusessioncreationfail"],
                                  process_max_fds=d["process_max_fds"],
                                  process_virtual_memory_max_bytes=d["process_virtual_memory_max_bytes"],
                                  process_cpu_seconds_total=d["process_cpu_seconds_total"],
                                  process_virtual_memory_bytes=d["process_virtual_memory_bytes"],
                                  process_resident_memory_bytes=d["process_resident_memory_bytes"],
                                  process_open_fds=d["process_open_fds"],
                                  process_start_time_seconds=d["process_start_time_seconds"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d: Dict[str, Any] = {}
        d["ts"] = self.ts
        d["ip"] = self.ip
        d["gn_rx_createpdpcontextreq"] = self.gn_rx_createpdpcontextreq
        d["gn_rx_deletepdpcontextreq"] = self.gn_rx_deletepdpcontextreq
        d["gtp1_pdpctxs_active"] = self.gtp1_pdpctxs_active
        d["pfcp_peers_active"] = self.pfcp_peers_active
        d["fivegs_smffunction_sm_n4sessionreport"] = self.fivegs_smffunction_sm_n4sessionreport
        d["ues_active"] = self.ues_active
        d["gtp2_sessions_active"] = self.gtp2_sessions_active
        d["pfcp_sessions_active"] = self.pfcp_sessions_active
        d["s5c_rx_createsession"] = self.s5c_rx_createsession
        d["s5c_rx_deletesession"] = self.s5c_rx_deletesession
        d["gtp_new_node_failed"] = self.gtp_new_node_failed
        d["s5c_rx_parse_failed"] = self.s5c_rx_parse_failed
        d["fivegs_smffunction_sm_n4sessionreportsucc"] = self.fivegs_smffunction_sm_n4sessionreportsucc
        d["fivegs_smffunction_sm_n4sessionestabreq"] = self.fivegs_smffunction_sm_n4sessionestabreq
        d["bearers_active"] = self.bearers_active
        d["gn_rx_parse_failed"] = self.gn_rx_parse_failed
        d["gtp_peers_active"] = self.gtp_peers_active
        d["fivegs_smffunction_sm_sessionnbr"] = self.fivegs_smffunction_sm_sessionnbr
        d["fivegs_smffunction_sm_pdusessioncreationreq"] = self.fivegs_smffunction_sm_pdusessioncreationreq
        d["fivegs_smffunction_sm_pdusessioncreationsucc"] = self.fivegs_smffunction_sm_pdusessioncreationsucc
        d["fivegs_smffunction_sm_qos_flow_nbr"] = self.fivegs_smffunction_sm_qos_flow_nbr
        d["fivegs_smffunction_sm_n4sessionestabfail"] = self.fivegs_smffunction_sm_n4sessionestabfail
        d["fivegs_smffunction_sm_pdusessioncreationfail"] = self.fivegs_smffunction_sm_pdusessioncreationfail
        d["process_max_fds"] = self.process_max_fds
        d["process_virtual_memory_max_bytes"] = self.process_virtual_memory_max_bytes
        d["process_cpu_seconds_total"] = self.process_cpu_seconds_total
        d["process_virtual_memory_bytes"] = self.process_virtual_memory_bytes
        d["process_resident_memory_bytes"] = self.process_resident_memory_bytes
        d["process_start_time_seconds"] = self.process_start_time_seconds
        d["process_open_fds"] = self.process_open_fds
        return d

    def copy(self) -> "FiveGCoreSMFMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCoreSMFMetrics(ip=self.ip, ts=self.ts)
        # We must copy all fields to be safe, but adhering to the original simplified pattern
        # usually suggests the caller might rely on to_dict/from_dict for deep copies or
        # just needs a shallow copy of the object shell.
        # To be fully correct per the pattern:
        c = FiveGCoreSMFMetrics.from_dict(self.to_dict())
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 32

    @staticmethod
    def schema() -> "FiveGCoreSMFMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCoreSMFMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCoreSMFMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCoreSMFMetrics.from_dict(json.loads(json_str))
