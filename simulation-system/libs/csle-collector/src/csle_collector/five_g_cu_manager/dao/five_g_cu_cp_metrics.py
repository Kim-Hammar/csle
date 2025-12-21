from typing import Dict, Any, Union
import time
import datetime
from csle_base.json_serializable import JSONSerializable


class FiveGCUCPMetrics(JSONSerializable):
    """
    DTO class containing srsRAN CU-CP (Central Unit - Control Plane) metrics.
    Captures NGAP (AMF interface) and RRC (UE/DU interface) statistics.
    """

    def __init__(self,
                 # --- Metadata ---
                 cu_cp_id: str = "",

                 # --- NGAP (AMF Interface) ---
                 amf_connected: bool = False,
                 nof_cn_initiated_paging_requests: int = 0,
                 nof_pdu_sessions_requested_to_setup: int = 0,
                 nof_pdu_sessions_successfully_setup: int = 0,
                 nof_pdu_sessions_failed_to_setup_total: int = 0,  # Aggregated sum of failure reasons
                 nof_handover_preparations_requested: int = 0,
                 nof_successful_handover_preparations: int = 0,

                 # --- RRC (Radio Interface) ---
                 rrc_establishments_attempted_total: int = 0,
                 rrc_establishments_successful_total: int = 0,
                 rrc_establishments_attempted_mo_data: int = 0,  # Mobile Originated Data
                 rrc_establishments_successful_mo_data: int = 0,
                 rrc_establishments_attempted_mo_sig: int = 0,  # Mobile Originated Signaling
                 rrc_establishments_successful_mo_sig: int = 0,
                 max_nof_rrc_connections: int = 0,
                 mean_nof_rrc_connections: int = 0,
                 rrc_reestablishments_attempted: int = 0,
                 rrc_reestablishments_successful: int = 0,
                 nof_handover_executions_requested: int = 0,
                 nof_successful_handover_executions: int = 0,

                 ip: Union[None, str] = None,
                 ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param cu_cp_id: Identifier of the CU-CP instance
        :param amf_connected: Boolean status if connected to AMF
        :param nof_cn_initiated_paging_requests: Number of paging requests from Core Network
        :param nof_pdu_sessions_requested_to_setup: Total PDU session setup requests
        :param nof_pdu_sessions_successfully_setup: Total successful PDU sessions
        :param nof_pdu_sessions_failed_to_setup_total: Total failed PDU sessions (sum of all failure causes)
        :param nof_handover_preparations_requested: Handover preparation requests (NGAP)
        :param nof_successful_handover_preparations: Successful handover preparations (NGAP)
        :param rrc_establishments_attempted_total: Total RRC connection attempts (all causes)
        :param rrc_establishments_successful_total: Total successful RRC connections (all causes)
        :param rrc_establishments_attempted_mo_data: RRC attempts for MO Data
        :param rrc_establishments_successful_mo_data: Successful RRC connections for MO Data
        :param rrc_establishments_attempted_mo_sig: RRC attempts for MO Signaling
        :param rrc_establishments_successful_mo_sig: Successful RRC connections for MO Signaling
        :param max_nof_rrc_connections: Maximum concurrent RRC connections observed
        :param mean_nof_rrc_connections: Mean concurrent RRC connections observed
        :param rrc_reestablishments_attempted: Total RRC re-establishment attempts
        :param rrc_reestablishments_successful: Total successful RRC re-establishments
        :param nof_handover_executions_requested: Handover execution requests (RRC)
        :param nof_successful_handover_executions: Successful handover executions (RRC)
        :param ip: The IP of the CU-CP
        :param ts: The timestamp the metrics were measured
        """
        self.cu_cp_id = cu_cp_id
        self.amf_connected = amf_connected
        self.nof_cn_initiated_paging_requests = nof_cn_initiated_paging_requests
        self.nof_pdu_sessions_requested_to_setup = nof_pdu_sessions_requested_to_setup
        self.nof_pdu_sessions_successfully_setup = nof_pdu_sessions_successfully_setup
        self.nof_pdu_sessions_failed_to_setup_total = nof_pdu_sessions_failed_to_setup_total
        self.nof_handover_preparations_requested = nof_handover_preparations_requested
        self.nof_successful_handover_preparations = nof_successful_handover_preparations

        self.rrc_establishments_attempted_total = rrc_establishments_attempted_total
        self.rrc_establishments_successful_total = rrc_establishments_successful_total
        self.rrc_establishments_attempted_mo_data = rrc_establishments_attempted_mo_data
        self.rrc_establishments_successful_mo_data = rrc_establishments_successful_mo_data
        self.rrc_establishments_attempted_mo_sig = rrc_establishments_attempted_mo_sig
        self.rrc_establishments_successful_mo_sig = rrc_establishments_successful_mo_sig
        self.max_nof_rrc_connections = max_nof_rrc_connections
        self.mean_nof_rrc_connections = mean_nof_rrc_connections
        self.rrc_reestablishments_attempted = rrc_reestablishments_attempted
        self.rrc_reestablishments_successful = rrc_reestablishments_successful
        self.nof_handover_executions_requested = nof_handover_executions_requested
        self.nof_successful_handover_executions = nof_successful_handover_executions

        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = self.ts if self.ts else time.time()
        record_str = (f"{ts},{ip},{self.cu_cp_id},{self.amf_connected},"
                      f"{self.nof_cn_initiated_paging_requests},"
                      f"{self.nof_pdu_sessions_requested_to_setup},"
                      f"{self.nof_pdu_sessions_successfully_setup},"
                      f"{self.nof_pdu_sessions_failed_to_setup_total},"
                      f"{self.nof_handover_preparations_requested},"
                      f"{self.nof_successful_handover_preparations},"
                      f"{self.rrc_establishments_attempted_total},"
                      f"{self.rrc_establishments_successful_total},"
                      f"{self.rrc_establishments_attempted_mo_data},"
                      f"{self.rrc_establishments_successful_mo_data},"
                      f"{self.rrc_establishments_attempted_mo_sig},"
                      f"{self.rrc_establishments_successful_mo_sig},"
                      f"{self.max_nof_rrc_connections},"
                      f"{self.mean_nof_rrc_connections},"
                      f"{self.rrc_reestablishments_attempted},"
                      f"{self.rrc_reestablishments_successful},"
                      f"{self.nof_handover_executions_requested},"
                      f"{self.nof_successful_handover_executions}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGCUCPMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        # Handling boolean conversion from string
        amf_conn = parts[3].lower() == 'true'

        obj = FiveGCUCPMetrics(
            ts=float(parts[0]),
            ip=parts[1],
            cu_cp_id=parts[2],
            amf_connected=amf_conn,
            nof_cn_initiated_paging_requests=int(parts[4]),
            nof_pdu_sessions_requested_to_setup=int(parts[5]),
            nof_pdu_sessions_successfully_setup=int(parts[6]),
            nof_pdu_sessions_failed_to_setup_total=int(parts[7]),
            nof_handover_preparations_requested=int(parts[8]),
            nof_successful_handover_preparations=int(parts[9]),
            rrc_establishments_attempted_total=int(parts[10]),
            rrc_establishments_successful_total=int(parts[11]),
            rrc_establishments_attempted_mo_data=int(parts[12]),
            rrc_establishments_successful_mo_data=int(parts[13]),
            rrc_establishments_attempted_mo_sig=int(parts[14]),
            rrc_establishments_successful_mo_sig=int(parts[15]),
            max_nof_rrc_connections=int(parts[16]),
            mean_nof_rrc_connections=int(parts[17]),
            rrc_reestablishments_attempted=int(parts[18]),
            rrc_reestablishments_successful=int(parts[19]),
            nof_handover_executions_requested=int(parts[20]),
            nof_successful_handover_executions=int(parts[21])
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
            self.cu_cp_id = parts[2]
            self.amf_connected = parts[3].lower() == 'true'
            self.nof_cn_initiated_paging_requests = int(parts[4])
            self.nof_pdu_sessions_requested_to_setup = int(parts[5])
            self.nof_pdu_sessions_successfully_setup = int(parts[6])
            self.nof_pdu_sessions_failed_to_setup_total = int(parts[7])
            self.nof_handover_preparations_requested = int(parts[8])
            self.nof_successful_handover_preparations = int(parts[9])
            self.rrc_establishments_attempted_total = int(parts[10])
            self.rrc_establishments_successful_total = int(parts[11])
            self.rrc_establishments_attempted_mo_data = int(parts[12])
            self.rrc_establishments_successful_mo_data = int(parts[13])
            self.rrc_establishments_attempted_mo_sig = int(parts[14])
            self.rrc_establishments_successful_mo_sig = int(parts[15])
            self.max_nof_rrc_connections = int(parts[16])
            self.mean_nof_rrc_connections = int(parts[17])
            self.rrc_reestablishments_attempted = int(parts[18])
            self.rrc_reestablishments_successful = int(parts[19])
            self.nof_handover_executions_requested = int(parts[20])
            self.nof_successful_handover_executions = int(parts[21])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, connected: {self.amf_connected}, "
                f"rrc_conns (max/mean): {self.max_nof_rrc_connections}/{self.mean_nof_rrc_connections}, "
                f"pdu_success: {self.nof_pdu_sessions_successfully_setup}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGCUCPMetrics":
        """
        Converts a dict representation to an instance.
        Expects the flat dictionary format produced by to_dict().

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGCUCPMetrics(
            cu_cp_id=d.get("cu_cp_id", ""),
            amf_connected=d.get("amf_connected", False),
            nof_cn_initiated_paging_requests=d.get("nof_cn_initiated_paging_requests", 0),
            nof_pdu_sessions_requested_to_setup=d.get("nof_pdu_sessions_requested_to_setup", 0),
            nof_pdu_sessions_successfully_setup=d.get("nof_pdu_sessions_successfully_setup", 0),
            nof_pdu_sessions_failed_to_setup_total=d.get("nof_pdu_sessions_failed_to_setup_total", 0),
            nof_handover_preparations_requested=d.get("nof_handover_preparations_requested", 0),
            nof_successful_handover_preparations=d.get("nof_successful_handover_preparations", 0),

            rrc_establishments_attempted_total=d.get("rrc_establishments_attempted_total", 0),
            rrc_establishments_successful_total=d.get("rrc_establishments_successful_total", 0),
            rrc_establishments_attempted_mo_data=d.get("rrc_establishments_attempted_mo_data", 0),
            rrc_establishments_successful_mo_data=d.get("rrc_establishments_successful_mo_data", 0),
            rrc_establishments_attempted_mo_sig=d.get("rrc_establishments_attempted_mo_sig", 0),
            rrc_establishments_successful_mo_sig=d.get("rrc_establishments_successful_mo_sig", 0),
            max_nof_rrc_connections=d.get("max_nof_rrc_connections", 0),
            mean_nof_rrc_connections=d.get("mean_nof_rrc_connections", 0),
            rrc_reestablishments_attempted=d.get("rrc_reestablishments_attempted", 0),
            rrc_reestablishments_successful=d.get("rrc_reestablishments_successful", 0),
            nof_handover_executions_requested=d.get("nof_handover_executions_requested", 0),
            nof_successful_handover_executions=d.get("nof_successful_handover_executions", 0),

            ip=d.get("ip"),
            ts=d.get("ts")
        )
        return obj

    @staticmethod
    def from_ws_dict(d: Dict[str, Any], ip: str) -> "FiveGCUCPMetrics":
        """
        Converts the raw dictionary from the WebSocket JSON stream to an instance.
        Handles the nested "cu-cp" structure.

        :param d: the raw dictionary from srsRAN WebSocket
        :param ip: the IP of the source CU-CP
        :return: the created instance
        """
        ts = time.time()
        if "timestamp" in d and d["timestamp"] is not None:
            try:
                dt = datetime.datetime.fromisoformat(d["timestamp"])
                ts = dt.timestamp()
            except Exception:
                pass

        # Navigation Safety
        root = d.get("cu-cp", {})

        # --- 1. NGAP Parsing ---
        ngaps = root.get("ngaps", {})
        ngap_list = ngaps.get("ngap", [])

        # Defaults
        amf_connected = False
        paging_reqs = 0
        pdu_req = 0
        pdu_succ = 0
        pdu_fail_total = 0

        # We aggregate stats if multiple AMFs exist, or just take the first one
        if ngap_list:
            for ngap in ngap_list:
                if ngap.get("connected", False):
                    amf_connected = True

                paging = ngap.get("paging_measurement", {})
                paging_reqs += paging.get("nof_cn_initiated_paging_requests", 0)

                pdu_mgmt = ngap.get("pdu_session_management", {})
                pdu_req += pdu_mgmt.get("nof_pdu_sessions_requested_to_setup", 0)
                pdu_succ += pdu_mgmt.get("nof_pdu_sessions_successfully_setup", 0)

                # Sum up all failure causes in the failure dict
                fail_dict = pdu_mgmt.get("nof_pdu_sessions_failed_to_setup", {})
                if fail_dict:
                    pdu_fail_total += sum(fail_dict.values())

        ho_prep_req = ngaps.get("nof_handover_preparations_requested", 0)
        ho_prep_succ = ngaps.get("nof_successful_handover_preparations", 0)

        # --- 2. RRC Parsing ---
        rrcs = root.get("rrcs", {})
        du_list = rrcs.get("du", [])

        # RRC Aggregators
        rrc_att_total = 0
        rrc_succ_total = 0
        rrc_att_mo_data = 0
        rrc_succ_mo_data = 0
        rrc_att_mo_sig = 0
        rrc_succ_mo_sig = 0
        max_rrc = 0
        mean_rrc = 0
        reest_att = 0
        reest_succ = 0

        if du_list:
            # Usually one DU context per entry, but could be multiple
            for du in du_list:
                est = du.get("rrc_connection_establishment", {})

                # Attempted
                att = est.get("attempted_rrc_connection_establishments", {})
                rrc_att_total += sum(att.values())
                rrc_att_mo_data += att.get("mo_data", 0)
                rrc_att_mo_sig += att.get("mo_sig", 0)

                # Successful
                succ = est.get("successful_rrc_connection_establishments", {})
                rrc_succ_total += sum(succ.values())
                rrc_succ_mo_data += succ.get("mo_data", 0)
                rrc_succ_mo_sig += succ.get("mo_sig", 0)

                # Numbers
                nums = du.get("rrc_connection_number", {})
                # We take the max of maxes, and maybe avg of means?
                # For simplicity, let's take max of max
                max_rrc = max(max_rrc, nums.get("max_nof_rrc_connections", 0))
                # For mean, just taking the value (assuming single DU for now is simpler)
                mean_rrc = nums.get("mean_nof_rrc_connections", 0)

                # Re-establishment
                reest = du.get("rrc_connection_reestablishment", {})
                reest_att += reest.get("attempted_rrc_connection_reestablishments", 0)
                reest_succ += reest.get("successful_rrc_connection_reestablishments_with_ue_context", 0)
                # Note: 'without_ue_context' is technically a success but usually implies a drop, ignoring for 'succ'

        ho_exec_req = rrcs.get("nof_handover_executions_requested", 0)
        ho_exec_succ = rrcs.get("nof_successful_handover_executions", 0)

        obj = FiveGCUCPMetrics(
            cu_cp_id=root.get("id", ""),
            amf_connected=amf_connected,
            nof_cn_initiated_paging_requests=paging_reqs,
            nof_pdu_sessions_requested_to_setup=pdu_req,
            nof_pdu_sessions_successfully_setup=pdu_succ,
            nof_pdu_sessions_failed_to_setup_total=pdu_fail_total,
            nof_handover_preparations_requested=ho_prep_req,
            nof_successful_handover_preparations=ho_prep_succ,

            rrc_establishments_attempted_total=rrc_att_total,
            rrc_establishments_successful_total=rrc_succ_total,
            rrc_establishments_attempted_mo_data=rrc_att_mo_data,
            rrc_establishments_successful_mo_data=rrc_succ_mo_data,
            rrc_establishments_attempted_mo_sig=rrc_att_mo_sig,
            rrc_establishments_successful_mo_sig=rrc_succ_mo_sig,
            max_nof_rrc_connections=max_rrc,
            mean_nof_rrc_connections=mean_rrc,
            rrc_reestablishments_attempted=reest_att,
            rrc_reestablishments_successful=reest_succ,
            nof_handover_executions_requested=ho_exec_req,
            nof_successful_handover_executions=ho_exec_succ,

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
        d["cu_cp_id"] = self.cu_cp_id
        d["amf_connected"] = self.amf_connected
        d["nof_cn_initiated_paging_requests"] = self.nof_cn_initiated_paging_requests
        d["nof_pdu_sessions_requested_to_setup"] = self.nof_pdu_sessions_requested_to_setup
        d["nof_pdu_sessions_successfully_setup"] = self.nof_pdu_sessions_successfully_setup
        d["nof_pdu_sessions_failed_to_setup_total"] = self.nof_pdu_sessions_failed_to_setup_total
        d["nof_handover_preparations_requested"] = self.nof_handover_preparations_requested
        d["nof_successful_handover_preparations"] = self.nof_successful_handover_preparations

        d["rrc_establishments_attempted_total"] = self.rrc_establishments_attempted_total
        d["rrc_establishments_successful_total"] = self.rrc_establishments_successful_total
        d["rrc_establishments_attempted_mo_data"] = self.rrc_establishments_attempted_mo_data
        d["rrc_establishments_successful_mo_data"] = self.rrc_establishments_successful_mo_data
        d["rrc_establishments_attempted_mo_sig"] = self.rrc_establishments_attempted_mo_sig
        d["rrc_establishments_successful_mo_sig"] = self.rrc_establishments_successful_mo_sig
        d["max_nof_rrc_connections"] = self.max_nof_rrc_connections
        d["mean_nof_rrc_connections"] = self.mean_nof_rrc_connections
        d["rrc_reestablishments_attempted"] = self.rrc_reestablishments_attempted
        d["rrc_reestablishments_successful"] = self.rrc_reestablishments_successful
        d["nof_handover_executions_requested"] = self.nof_handover_executions_requested
        d["nof_successful_handover_executions"] = self.nof_successful_handover_executions
        return d

    def copy(self) -> "FiveGCUCPMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGCUCPMetrics(
            cu_cp_id=self.cu_cp_id, amf_connected=self.amf_connected,
            nof_cn_initiated_paging_requests=self.nof_cn_initiated_paging_requests,
            nof_pdu_sessions_requested_to_setup=self.nof_pdu_sessions_requested_to_setup,
            nof_pdu_sessions_successfully_setup=self.nof_pdu_sessions_successfully_setup,
            nof_pdu_sessions_failed_to_setup_total=self.nof_pdu_sessions_failed_to_setup_total,
            nof_handover_preparations_requested=self.nof_handover_preparations_requested,
            nof_successful_handover_preparations=self.nof_successful_handover_preparations,
            rrc_establishments_attempted_total=self.rrc_establishments_attempted_total,
            rrc_establishments_successful_total=self.rrc_establishments_successful_total,
            rrc_establishments_attempted_mo_data=self.rrc_establishments_attempted_mo_data,
            rrc_establishments_successful_mo_data=self.rrc_establishments_successful_mo_data,
            rrc_establishments_attempted_mo_sig=self.rrc_establishments_attempted_mo_sig,
            rrc_establishments_successful_mo_sig=self.rrc_establishments_successful_mo_sig,
            max_nof_rrc_connections=self.max_nof_rrc_connections,
            mean_nof_rrc_connections=self.mean_nof_rrc_connections,
            rrc_reestablishments_attempted=self.rrc_reestablishments_attempted,
            rrc_reestablishments_successful=self.rrc_reestablishments_successful,
            nof_handover_executions_requested=self.nof_handover_executions_requested,
            nof_successful_handover_executions=self.nof_successful_handover_executions,
            ip=self.ip, ts=self.ts
        )
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 22

    @staticmethod
    def schema() -> "FiveGCUCPMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGCUCPMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGCUCPMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGCUCPMetrics.from_dict(json.loads(json_str))
