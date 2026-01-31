from typing import Dict, Any, Union
import time
import datetime
import csle_collector.constants.constants as constants
from csle_base.json_serializable import JSONSerializable


class FiveGDULowMetrics(JSONSerializable):
    """
    DTO class containing srsRAN DU Low-PHY metrics.
    Captures Downlink (DL) and Uplink (UL) performance at the physical layer.
    """

    def __init__(self, dl_avg_latency_us: float = 0.0, dl_cpu_usage_percent: float = 0.0,
                 dl_max_latency_us: float = 0.0, dl_fec_tput_mbps: float = 0.0,
                 ul_avg_latency_us: float = 0.0, ul_cpu_usage_percent: float = 0.0,
                 ul_max_latency_us: float = 0.0, ul_sinr_db: float = 0.0,
                 ul_ch_est_latency_us: float = 0.0, ul_ldpc_dec_latency_us: float = 0.0,
                 ul_fec_tput_mbps: float = 0.0, ip: Union[None, str] = None,
                 ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param dl_avg_latency_us: Average processing latency for Downlink slots
        :param dl_cpu_usage_percent: CPU usage of the Downlink PHY thread
        :param dl_max_latency_us: Maximum processing latency for Downlink slots
        :param dl_fec_tput_mbps: Downlink Forward Error Correction throughput
        :param ul_avg_latency_us: Average processing latency for Uplink slots
        :param ul_cpu_usage_percent: CPU usage of the Uplink PHY thread
        :param ul_max_latency_us: Maximum processing latency for Uplink slots
        :param ul_sinr_db: Uplink Signal-to-Interference-plus-Noise Ratio (Radio Quality)
        :param ul_ch_est_latency_us: Latency for Channel Estimation (expensive operation)
        :param ul_ldpc_dec_latency_us: Latency for LDPC Decoding
        :param ul_fec_tput_mbps: Uplink Forward Error Correction throughput
        :param ip: The IP of the DU
        :param ts: The timestamp the metrics were measured
        """
        self.dl_avg_latency_us = dl_avg_latency_us
        self.dl_cpu_usage_percent = dl_cpu_usage_percent
        self.dl_max_latency_us = dl_max_latency_us
        self.dl_fec_tput_mbps = dl_fec_tput_mbps
        self.ul_avg_latency_us = ul_avg_latency_us
        self.ul_cpu_usage_percent = ul_cpu_usage_percent
        self.ul_max_latency_us = ul_max_latency_us
        self.ul_sinr_db = ul_sinr_db
        self.ul_ch_est_latency_us = ul_ch_est_latency_us
        self.ul_ldpc_dec_latency_us = ul_ldpc_dec_latency_us
        self.ul_fec_tput_mbps = ul_fec_tput_mbps
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = self.ts if self.ts else time.time()
        record_str = (f"{ts},{ip},{self.dl_avg_latency_us},"
                      f"{self.dl_cpu_usage_percent},{self.dl_max_latency_us},"
                      f"{self.dl_fec_tput_mbps},{self.ul_avg_latency_us},"
                      f"{self.ul_cpu_usage_percent},{self.ul_max_latency_us},"
                      f"{self.ul_sinr_db},{self.ul_ch_est_latency_us},"
                      f"{self.ul_ldpc_dec_latency_us},{self.ul_fec_tput_mbps}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGDULowMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGDULowMetrics(
            ts=float(parts[0]),
            ip=parts[1],
            dl_avg_latency_us=float(parts[2]),
            dl_cpu_usage_percent=float(parts[3]),
            dl_max_latency_us=float(parts[4]),
            dl_fec_tput_mbps=float(parts[5]),
            ul_avg_latency_us=float(parts[6]),
            ul_cpu_usage_percent=float(parts[7]),
            ul_max_latency_us=float(parts[8]),
            ul_sinr_db=float(parts[9]),
            ul_ch_est_latency_us=float(parts[10]),
            ul_ldpc_dec_latency_us=float(parts[11]),
            ul_fec_tput_mbps=float(parts[12])
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
            self.dl_avg_latency_us = float(parts[2])
            self.dl_cpu_usage_percent = float(parts[3])
            self.dl_max_latency_us = float(parts[4])
            self.dl_fec_tput_mbps = float(parts[5])
            self.ul_avg_latency_us = float(parts[6])
            self.ul_cpu_usage_percent = float(parts[7])
            self.ul_max_latency_us = float(parts[8])
            self.ul_sinr_db = float(parts[9])
            self.ul_ch_est_latency_us = float(parts[10])
            self.ul_ldpc_dec_latency_us = float(parts[11])
            self.ul_fec_tput_mbps = float(parts[12])

    def __str__(self) -> str:
        """
        :return: A structured string representation of all metrics with units.
        """
        return (f"FiveGDULowMetrics(ts={self.ts}, ip={self.ip}, "
                f"DL=[avg_lat={self.dl_avg_latency_us}us, max_lat={self.dl_max_latency_us}us, "
                f"cpu={self.dl_cpu_usage_percent}%, tput={self.dl_fec_tput_mbps}Mbps], "
                f"UL=[avg_lat={self.ul_avg_latency_us}us, max_lat={self.ul_max_latency_us}us, "
                f"cpu={self.ul_cpu_usage_percent}%, sinr={self.ul_sinr_db}dB, "
                f"ch_est={self.ul_ch_est_latency_us}us, ldpc={self.ul_ldpc_dec_latency_us}us, "
                f"tput={self.ul_fec_tput_mbps}Mbps])")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGDULowMetrics":
        """
        Converts a dict representation to an instance.
        Expects the flat dictionary format produced by to_dict().

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGDULowMetrics(
            dl_avg_latency_us=d.get(constants.FIVE_G_DU.DL_AVG_LATENCY_US, 0.0),
            dl_cpu_usage_percent=d.get(constants.FIVE_G_DU.DL_CPU_USAGE_PERCENT, 0.0),
            dl_max_latency_us=d.get(constants.FIVE_G_DU.DL_MAX_LATENCY_US, 0.0),
            dl_fec_tput_mbps=d.get(constants.FIVE_G_DU.DL_FEC_TPUT_MBPS, 0.0),

            ul_avg_latency_us=d.get(constants.FIVE_G_DU.UL_AVG_LATENCY_US, 0.0),
            ul_cpu_usage_percent=d.get(constants.FIVE_G_DU.UL_CPU_USAGE_PERCENT, 0.0),
            ul_max_latency_us=d.get(constants.FIVE_G_DU.UL_MAX_LATENCY_US, 0.0),
            ul_sinr_db=d.get(constants.FIVE_G_DU.UL_SINR_DB, 0.0),
            ul_ch_est_latency_us=d.get(constants.FIVE_G_DU.UL_CH_EST_LATENCY_US, 0.0),
            ul_ldpc_dec_latency_us=d.get(constants.FIVE_G_DU.UL_LDPC_DEC_LATENCY_US, 0.0),
            ul_fec_tput_mbps=d.get(constants.FIVE_G_DU.UL_FEC_TPUT_MBPS, 0.0),

            ip=d.get(constants.FIVE_G_DU.IP),
            ts=d.get(constants.FIVE_G_DU.TS)
        )
        return obj

    @staticmethod
    def from_ws_dict(d: Dict[str, Any], ip: str) -> "FiveGDULowMetrics":
        """
        Converts the raw dictionary from the WebSocket JSON stream to an instance.
        Handles the nested "du_low" structure.

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

        # Parse nested structure safely
        dl_data = {}
        ul_data = {}

        if constants.FIVE_G_DU.DU_LOW in d:
            dl_data = d[constants.FIVE_G_DU.DU_LOW].get(constants.FIVE_G_DU.DL, {})
            ul_data = d[constants.FIVE_G_DU.DU_LOW].get(constants.FIVE_G_DU.UL, {})

        # Downlink Sub-components
        dl_fec = dl_data.get(constants.FIVE_G_DU.FEC, {})

        # Uplink Sub-components
        ul_algo = ul_data.get(constants.FIVE_G_DU.ALGO_EFFICIENCY, {})
        ul_ch_est = ul_data.get(constants.FIVE_G_DU.CHANNEL_ESTIMATION, {})
        ul_ldpc = ul_data.get(constants.FIVE_G_DU.LDPC_DECODER, {})
        ul_fec = ul_data.get(constants.FIVE_G_DU.FEC, {})

        obj = FiveGDULowMetrics(
            dl_avg_latency_us=dl_data.get(constants.FIVE_G_DU.AVERAGE_LATENCY_US, 0.0),
            dl_cpu_usage_percent=dl_data.get(constants.FIVE_G_DU.CPU_USAGE_PERCENT, 0.0),
            dl_max_latency_us=dl_data.get(constants.FIVE_G_DU.MAX_LATENCY_US, 0.0),
            dl_fec_tput_mbps=dl_fec.get(constants.FIVE_G_DU.AVERAGE_THROUGHPUT_MBPS, 0.0),

            ul_avg_latency_us=ul_data.get(constants.FIVE_G_DU.AVERAGE_LATENCY_US, 0.0),
            ul_cpu_usage_percent=ul_data.get(constants.FIVE_G_DU.CPU_USAGE_PERCENT, 0.0),
            ul_max_latency_us=ul_data.get(constants.FIVE_G_DU.MAX_LATENCY_US, 0.0),
            ul_sinr_db=ul_algo.get(constants.FIVE_G_DU.UL_SINR_DB, 0.0),
            ul_ch_est_latency_us=ul_ch_est.get(constants.FIVE_G_DU.AVERAGE_LATENCY_US, 0.0),
            ul_ldpc_dec_latency_us=ul_ldpc.get(constants.FIVE_G_DU.AVERAGE_LATENCY_US, 0.0),
            ul_fec_tput_mbps=ul_fec.get(constants.FIVE_G_DU.AVERAGE_THROUGHPUT_MBPS, 0.0),

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
        d[constants.FIVE_G_DU.DL_AVG_LATENCY_US] = self.dl_avg_latency_us
        d[constants.FIVE_G_DU.DL_CPU_USAGE_PERCENT] = self.dl_cpu_usage_percent
        d[constants.FIVE_G_DU.DL_MAX_LATENCY_US] = self.dl_max_latency_us
        d[constants.FIVE_G_DU.DL_FEC_TPUT_MBPS] = self.dl_fec_tput_mbps
        d[constants.FIVE_G_DU.UL_AVG_LATENCY_US] = self.ul_avg_latency_us
        d[constants.FIVE_G_DU.UL_CPU_USAGE_PERCENT] = self.ul_cpu_usage_percent
        d[constants.FIVE_G_DU.UL_MAX_LATENCY_US] = self.ul_max_latency_us
        d[constants.FIVE_G_DU.UL_SINR_DB] = self.ul_sinr_db
        d[constants.FIVE_G_DU.UL_CH_EST_LATENCY_US] = self.ul_ch_est_latency_us
        d[constants.FIVE_G_DU.UL_LDPC_DEC_LATENCY_US] = self.ul_ldpc_dec_latency_us
        d[constants.FIVE_G_DU.UL_FEC_TPUT_MBPS] = self.ul_fec_tput_mbps
        return d

    def copy(self) -> "FiveGDULowMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGDULowMetrics(
            dl_avg_latency_us=self.dl_avg_latency_us,
            dl_cpu_usage_percent=self.dl_cpu_usage_percent,
            dl_max_latency_us=self.dl_max_latency_us,
            dl_fec_tput_mbps=self.dl_fec_tput_mbps,
            ul_avg_latency_us=self.ul_avg_latency_us,
            ul_cpu_usage_percent=self.ul_cpu_usage_percent,
            ul_max_latency_us=self.ul_max_latency_us,
            ul_sinr_db=self.ul_sinr_db,
            ul_ch_est_latency_us=self.ul_ch_est_latency_us,
            ul_ldpc_dec_latency_us=self.ul_ldpc_dec_latency_us,
            ul_fec_tput_mbps=self.ul_fec_tput_mbps,
            ip=self.ip, ts=self.ts
        )
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 13

    @staticmethod
    def schema() -> "FiveGDULowMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGDULowMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGDULowMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGDULowMetrics.from_dict(json.loads(json_str))
