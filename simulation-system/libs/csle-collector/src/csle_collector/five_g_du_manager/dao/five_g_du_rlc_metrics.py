from typing import Dict, Any, Union
import time
import datetime
import csle_collector.constants.constants as constants
from csle_base.json_serializable import JSONSerializable


class FiveGDURLCMetrics(JSONSerializable):
    """
    DTO class containing srsRAN DU RLC layer metrics
    """

    def __init__(self, ue_id: int = 0, drb_id: int = 0, rx_num_pdus: int = 0,
                 rx_num_bytes: int = 0, rx_num_lost_pdus: int = 0,
                 rx_num_malformed_pdus: int = 0, tx_num_sdus: int = 0,
                 tx_num_bytes: int = 0, tx_num_dropped_sdus: int = 0,
                 tx_num_discarded_sdus: int = 0, tx_max_pdu_latency_ns: int = 0,
                 tx_sum_pdu_latency_ns: int = 0, tx_sum_sdu_latency_us: int = 0,
                 ip: Union[None, str] = None, ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param ue_id: The User Equipment ID
        :param drb_id: Data Radio Bearer ID
        :param rx_num_pdus: Number of received PDUs
        :param rx_num_bytes: Number of received bytes (PDU level)
        :param rx_num_lost_pdus: Number of lost PDUs detected
        :param rx_num_malformed_pdus: Number of malformed PDUs
        :param tx_num_sdus: Number of transmitted SDUs
        :param tx_num_bytes: Number of transmitted bytes (SDU level)
        :param tx_num_dropped_sdus: Number of dropped SDUs (e.g. buffer full)
        :param tx_num_discarded_sdus: Number of discarded SDUs (e.g. timeout)
        :param tx_max_pdu_latency_ns: Maximum PDU latency in nanoseconds
        :param tx_sum_pdu_latency_ns: Sum of PDU latencies in nanoseconds (for avg calc)
        :param tx_sum_sdu_latency_us: Sum of SDU latencies in microseconds
        :param ip: The IP of the DU
        :param ts: The timestamp the metrics were measured
        """
        self.ue_id = ue_id
        self.drb_id = drb_id
        self.rx_num_pdus = rx_num_pdus
        self.rx_num_bytes = rx_num_bytes
        self.rx_num_lost_pdus = rx_num_lost_pdus
        self.rx_num_malformed_pdus = rx_num_malformed_pdus
        self.tx_num_sdus = tx_num_sdus
        self.tx_num_bytes = tx_num_bytes
        self.tx_num_dropped_sdus = tx_num_dropped_sdus
        self.tx_num_discarded_sdus = tx_num_discarded_sdus
        self.tx_max_pdu_latency_ns = tx_max_pdu_latency_ns
        self.tx_sum_pdu_latency_ns = tx_sum_pdu_latency_ns
        self.tx_sum_sdu_latency_us = tx_sum_sdu_latency_us
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = self.ts if self.ts else time.time()
        record_str = (f"{ts},{ip},{self.ue_id},{self.drb_id},"
                      f"{self.rx_num_pdus},{self.rx_num_bytes},"
                      f"{self.rx_num_lost_pdus},{self.rx_num_malformed_pdus},"
                      f"{self.tx_num_sdus},{self.tx_num_bytes},"
                      f"{self.tx_num_dropped_sdus},{self.tx_num_discarded_sdus},"
                      f"{self.tx_max_pdu_latency_ns},{self.tx_sum_pdu_latency_ns},"
                      f"{self.tx_sum_sdu_latency_us}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGDURLCMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGDURLCMetrics(
            ts=float(parts[0]),
            ip=parts[1],
            ue_id=int(parts[2]),
            drb_id=int(parts[3]),
            rx_num_pdus=int(parts[4]),
            rx_num_bytes=int(parts[5]),
            rx_num_lost_pdus=int(parts[6]),
            rx_num_malformed_pdus=int(parts[7]),
            tx_num_sdus=int(parts[8]),
            tx_num_bytes=int(parts[9]),
            tx_num_dropped_sdus=int(parts[10]),
            tx_num_discarded_sdus=int(parts[11]),
            tx_max_pdu_latency_ns=int(parts[12]),
            tx_sum_pdu_latency_ns=int(parts[13]),
            tx_sum_sdu_latency_us=int(parts[14])
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
            self.ue_id = int(parts[2])
            self.drb_id = int(parts[3])
            self.rx_num_pdus = int(parts[4])
            self.rx_num_bytes = int(parts[5])
            self.rx_num_lost_pdus = int(parts[6])
            self.rx_num_malformed_pdus = int(parts[7])
            self.tx_num_sdus = int(parts[8])
            self.tx_num_bytes = int(parts[9])
            self.tx_num_dropped_sdus = int(parts[10])
            self.tx_num_discarded_sdus = int(parts[11])
            self.tx_max_pdu_latency_ns = int(parts[12])
            self.tx_sum_pdu_latency_ns = int(parts[13])
            self.tx_sum_sdu_latency_us = int(parts[14])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, ue_id: {self.ue_id}, "
                f"drb_id: {self.drb_id}, rx_pdus: {self.rx_num_pdus}, "
                f"lost: {self.rx_num_lost_pdus}, tx_sdus: {self.tx_num_sdus}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGDURLCMetrics":
        """
        Converts a dict representation to an instance.
        Expects the flat dictionary format produced by to_dict().

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGDURLCMetrics(
            ue_id=d.get(constants.FIVE_G_DU.UE_ID, 0),
            drb_id=d.get(constants.FIVE_G_DU.DRB_ID, 0),
            rx_num_pdus=d.get(constants.FIVE_G_DU.RX_NUM_PDUS, 0),
            rx_num_bytes=d.get(constants.FIVE_G_DU.RX_NUM_BYTES, 0),
            rx_num_lost_pdus=d.get(constants.FIVE_G_DU.RX_NUM_LOST_PDUS, 0),
            rx_num_malformed_pdus=d.get(constants.FIVE_G_DU.RX_NUM_MALFORMED_PDUS, 0),
            tx_num_sdus=d.get(constants.FIVE_G_DU.TX_NUM_SDUS, 0),
            tx_num_bytes=d.get(constants.FIVE_G_DU.TX_NUM_BYTES, 0),
            tx_num_dropped_sdus=d.get(constants.FIVE_G_DU.TX_NUM_DROPPED_SDUS, 0),
            tx_num_discarded_sdus=d.get(constants.FIVE_G_DU.TX_NUM_DISCARDED_SDUS, 0),
            tx_max_pdu_latency_ns=d.get(constants.FIVE_G_DU.TX_MAX_PDU_LATENCY_NS, 0),
            tx_sum_pdu_latency_ns=d.get(constants.FIVE_G_DU.TX_SUM_PDU_LATENCY_NS, 0),
            tx_sum_sdu_latency_us=d.get(constants.FIVE_G_DU.TX_SUM_SDU_LATENCY_US, 0),
            ip=d.get(constants.FIVE_G_DU.IP),
            ts=d.get(constants.FIVE_G_DU.TS)
        )
        return obj

    @staticmethod
    def from_ws_dict(d: Dict[str, Any], ip: str) -> "FiveGDURLCMetrics":
        """
        Converts the raw dictionary from the WebSocket JSON stream to an instance.
        Handles the nested "rlc_metrics" -> "rx"/"tx" structure.

        :param d: the raw dictionary from srsRAN WebSocket
        :param ip: the IP of the source DU
        :return: the created instance
        """
        ts = time.time()
        if constants.FIVE_G_DU.TIMESTAMP in d and d[constants.FIVE_G_DU.TIMESTAMP] is not None:
            try:
                dt = datetime.datetime.fromisoformat(d[constants.FIVE_G_DU.TIMESTAMP])
                ts = dt.timestamp()
            except Exception:
                pass

        data = {}
        if constants.FIVE_G_DU.RLC_METRICS in d:
            data = d[constants.FIVE_G_DU.RLC_METRICS]
        else:
            data = d

        rx = data.get(constants.FIVE_G_DU.RX, {})
        tx = data.get(constants.FIVE_G_DU.TX, {})

        obj = FiveGDURLCMetrics(
            ue_id=data.get(constants.FIVE_G_DU.UE_ID, 0),
            drb_id=data.get(constants.FIVE_G_DU.DRB_ID, 0),
            rx_num_pdus=rx.get(constants.FIVE_G_DU.NUM_PDUS, 0),
            rx_num_bytes=rx.get(constants.FIVE_G_DU.NUM_PDU_BYTES, 0),
            rx_num_lost_pdus=rx.get(constants.FIVE_G_DU.NUM_LOST_PDUS, 0),
            rx_num_malformed_pdus=rx.get(constants.FIVE_G_DU.NUM_MALFORMED_PDUS, 0),
            tx_num_sdus=tx.get(constants.FIVE_G_DU.NUM_SDUS, 0),
            tx_num_bytes=tx.get(constants.FIVE_G_DU.NUM_SDU_BYTES, 0),
            tx_num_dropped_sdus=tx.get(constants.FIVE_G_DU.NUM_DROPPED_SDUS, 0),
            tx_num_discarded_sdus=tx.get(constants.FIVE_G_DU.NUM_DISCARDED_SDUS, 0),
            tx_max_pdu_latency_ns=tx.get(constants.FIVE_G_DU.MAX_PDU_LATENCY_NS, 0),
            tx_sum_pdu_latency_ns=tx.get(constants.FIVE_G_DU.SUM_PDU_LATENCY_NS, 0),
            tx_sum_sdu_latency_us=tx.get(constants.FIVE_G_DU.SUM_SDU_LATENCY_US, 0),
            ip=ip,
            ts=ts
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d: Dict[str, Any] = {}
        d[constants.FIVE_G_DU.TS] = self.ts
        d[constants.FIVE_G_DU.IP] = self.ip
        d[constants.FIVE_G_DU.UE_ID] = self.ue_id
        d[constants.FIVE_G_DU.DRB_ID] = self.drb_id
        d[constants.FIVE_G_DU.RX_NUM_PDUS] = self.rx_num_pdus
        d[constants.FIVE_G_DU.RX_NUM_BYTES] = self.rx_num_bytes
        d[constants.FIVE_G_DU.RX_NUM_LOST_PDUS] = self.rx_num_lost_pdus
        d[constants.FIVE_G_DU.RX_NUM_MALFORMED_PDUS] = self.rx_num_malformed_pdus
        d[constants.FIVE_G_DU.TX_NUM_SDUS] = self.tx_num_sdus
        d[constants.FIVE_G_DU.TX_NUM_BYTES] = self.tx_num_bytes
        d[constants.FIVE_G_DU.TX_NUM_DROPPED_SDUS] = self.tx_num_dropped_sdus
        d[constants.FIVE_G_DU.TX_NUM_DISCARDED_SDUS] = self.tx_num_discarded_sdus
        d[constants.FIVE_G_DU.TX_MAX_PDU_LATENCY_NS] = self.tx_max_pdu_latency_ns
        d[constants.FIVE_G_DU.TX_SUM_PDU_LATENCY_NS] = self.tx_sum_pdu_latency_ns
        d[constants.FIVE_G_DU.TX_SUM_SDU_LATENCY_US] = self.tx_sum_sdu_latency_us
        return d

    def copy(self) -> "FiveGDURLCMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGDURLCMetrics(
            ue_id=self.ue_id, drb_id=self.drb_id, rx_num_pdus=self.rx_num_pdus,
            rx_num_bytes=self.rx_num_bytes, rx_num_lost_pdus=self.rx_num_lost_pdus,
            rx_num_malformed_pdus=self.rx_num_malformed_pdus,
            tx_num_sdus=self.tx_num_sdus, tx_num_bytes=self.tx_num_bytes,
            tx_num_dropped_sdus=self.tx_num_dropped_sdus,
            tx_num_discarded_sdus=self.tx_num_discarded_sdus,
            tx_max_pdu_latency_ns=self.tx_max_pdu_latency_ns,
            tx_sum_pdu_latency_ns=self.tx_sum_pdu_latency_ns,
            tx_sum_sdu_latency_us=self.tx_sum_sdu_latency_us,
            ip=self.ip, ts=self.ts
        )
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 15

    @staticmethod
    def schema() -> "FiveGDURLCMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGDURLCMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGDURLCMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGDURLCMetrics.from_dict(json.loads(json_str))
