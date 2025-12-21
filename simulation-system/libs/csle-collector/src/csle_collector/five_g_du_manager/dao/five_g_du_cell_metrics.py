from typing import Dict, Any, Union
import time
import datetime
from csle_base.json_serializable import JSONSerializable


class FiveGDUCellMetrics(JSONSerializable):
    """
    DTO class containing srsRAN DU Cell metrics
    """

    def __init__(self, pci: int = 0, average_latency: float = 0.0,
                 max_latency: float = 0.0, pucch_tot_rb_usage_avg: float = 0.0,
                 active_ues: int = 0, dl_brate: float = 0.0, ul_brate: float = 0.0,
                 dl_mcs: float = 0.0, ul_mcs: float = 0.0, pusch_snr_db: float = 0.0,
                 pucch_snr_db: float = 0.0, cqi: float = 0.0, dl_bler: float = 0.0,
                 ul_bler: float = 0.0, ip: Union[None, str] = None,
                 ts: Union[float, None] = None) -> None:
        """
        Initializes the DTO

        :param pci: Physical Cell ID
        :param average_latency: Average processing latency of the cell
        :param max_latency: Maximum processing latency of the cell
        :param pucch_tot_rb_usage_avg: Average PUCCH Resource Block usage
        :param active_ues: Number of active UEs connected
        :param dl_brate: Total Downlink bitrate (bps)
        :param ul_brate: Total Uplink bitrate (bps)
        :param dl_mcs: Average Downlink MCS
        :param ul_mcs: Average Uplink MCS
        :param pusch_snr_db: Average PUSCH SNR (dB)
        :param pucch_snr_db: Average PUCCH SNR (dB)
        :param cqi: Average Channel Quality Indicator
        :param dl_bler: Downlink Block Error Rate (derived from OK/NOK)
        :param ul_bler: Uplink Block Error Rate (derived from OK/NOK)
        :param ip: The IP of the DU
        :param ts: The timestamp the metrics were measured
        """
        self.pci = pci
        self.average_latency = average_latency
        self.max_latency = max_latency
        self.pucch_tot_rb_usage_avg = pucch_tot_rb_usage_avg
        self.active_ues = active_ues
        self.dl_brate = dl_brate
        self.ul_brate = ul_brate
        self.dl_mcs = dl_mcs
        self.ul_mcs = ul_mcs
        self.pusch_snr_db = pusch_snr_db
        self.pucch_snr_db = pucch_snr_db
        self.cqi = cqi
        self.dl_bler = dl_bler
        self.ul_bler = ul_bler
        self.ip = ip
        self.ts = ts

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = self.ts if self.ts else time.time()
        record_str = (f"{ts},{ip},{self.pci},{self.average_latency},"
                      f"{self.max_latency},{self.pucch_tot_rb_usage_avg},"
                      f"{self.active_ues},{self.dl_brate},{self.ul_brate},"
                      f"{self.dl_mcs},{self.ul_mcs},{self.pusch_snr_db},"
                      f"{self.pucch_snr_db},{self.cqi},{self.dl_bler},"
                      f"{self.ul_bler}")
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "FiveGDUCellMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = FiveGDUCellMetrics(
            ts=float(parts[0]),
            ip=parts[1],
            pci=int(parts[2]),
            average_latency=float(parts[3]),
            max_latency=float(parts[4]),
            pucch_tot_rb_usage_avg=float(parts[5]),
            active_ues=int(parts[6]),
            dl_brate=float(parts[7]),
            ul_brate=float(parts[8]),
            dl_mcs=float(parts[9]),
            ul_mcs=float(parts[10]),
            pusch_snr_db=float(parts[11]),
            pucch_snr_db=float(parts[12]),
            cqi=float(parts[13]),
            dl_bler=float(parts[14]),
            ul_bler=float(parts[15])
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
            self.pci = int(parts[2])
            self.average_latency = float(parts[3])
            self.max_latency = float(parts[4])
            self.pucch_tot_rb_usage_avg = float(parts[5])
            self.active_ues = int(parts[6])
            self.dl_brate = float(parts[7])
            self.ul_brate = float(parts[8])
            self.dl_mcs = float(parts[9])
            self.ul_mcs = float(parts[10])
            self.pusch_snr_db = float(parts[11])
            self.pucch_snr_db = float(parts[12])
            self.cqi = float(parts[13])
            self.dl_bler = float(parts[14])
            self.ul_bler = float(parts[15])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"ts: {self.ts}, ip: {self.ip}, pci: {self.pci}, "
                f"active_ues: {self.active_ues}, dl_brate: {self.dl_brate}, "
                f"ul_brate: {self.ul_brate}, pusch_snr: {self.pusch_snr_db}")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGDUCellMetrics":
        """
        Converts a dict representation to an instance.
        Expects the flat dictionary format produced by to_dict().

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGDUCellMetrics(
            pci=d.get("pci", 0),
            average_latency=d.get("average_latency", 0.0),
            max_latency=d.get("max_latency", 0.0),
            pucch_tot_rb_usage_avg=d.get("pucch_tot_rb_usage_avg", 0.0),
            active_ues=d.get("active_ues", 0),
            dl_brate=d.get("dl_brate", 0.0),
            ul_brate=d.get("ul_brate", 0.0),
            dl_mcs=d.get("dl_mcs", 0.0),
            ul_mcs=d.get("ul_mcs", 0.0),
            pusch_snr_db=d.get("pusch_snr_db", 0.0),
            pucch_snr_db=d.get("pucch_snr_db", 0.0),
            cqi=d.get("cqi", 0.0),
            dl_bler=d.get("dl_bler", 0.0),
            ul_bler=d.get("ul_bler", 0.0),
            ip=d.get("ip"),
            ts=d.get("ts")
        )
        return obj

    @staticmethod
    def from_ws_dict(d: Dict[str, Any], ip: str) -> "FiveGDUCellMetrics":
        """
        Converts the raw dictionary from the WebSocket JSON stream to an instance.
        Handles the nested "cells" list and aggregates UE metrics.

        :param d: the raw dictionary from srsRAN WebSocket
        :param ip: the IP of the source DU
        :return: the created instance
        """
        ts = time.time()
        if "timestamp" in d and d["timestamp"] is not None:
            try:
                dt = datetime.datetime.fromisoformat(d["timestamp"])
                ts = dt.timestamp()
            except Exception:
                pass

        cell_data = {}
        ue_list = []
        if "cells" in d and len(d["cells"]) > 0:
            cell_data = d["cells"][0].get("cell_metrics", {})
            ue_list = d["cells"][0].get("ue_list", [])

        # Aggregation logic
        active_ues = len(ue_list)
        total_dl_brate = 0.0
        total_ul_brate = 0.0
        sum_dl_mcs = 0.0
        sum_ul_mcs = 0.0
        sum_pusch_snr = 0.0
        sum_pucch_snr = 0.0
        sum_cqi = 0.0
        total_dl_ok = 0
        total_dl_nok = 0
        total_ul_ok = 0
        total_ul_nok = 0

        for ue in ue_list:
            total_dl_brate += ue.get("dl_brate", 0.0)
            total_ul_brate += ue.get("ul_brate", 0.0)
            sum_dl_mcs += ue.get("dl_mcs", 0)
            sum_ul_mcs += ue.get("ul_mcs", 0)
            sum_pusch_snr += ue.get("pusch_snr_db", 0.0)
            sum_pucch_snr += ue.get("pucch_snr_db", 0.0)
            sum_cqi += ue.get("cqi", 0)
            total_dl_ok += ue.get("dl_nof_ok", 0)
            total_dl_nok += ue.get("dl_nof_nok", 0)
            total_ul_ok += ue.get("ul_nof_ok", 0)
            total_ul_nok += ue.get("ul_nof_nok", 0)

        avg_dl_mcs = sum_dl_mcs / active_ues if active_ues > 0 else 0.0
        avg_ul_mcs = sum_ul_mcs / active_ues if active_ues > 0 else 0.0
        avg_pusch_snr = sum_pusch_snr / active_ues if active_ues > 0 else 0.0
        avg_pucch_snr = sum_pucch_snr / active_ues if active_ues > 0 else 0.0
        avg_cqi = sum_cqi / active_ues if active_ues > 0 else 0.0

        # BLER Calculation
        dl_bler = 0.0
        if (total_dl_ok + total_dl_nok) > 0:
            dl_bler = total_dl_nok / (total_dl_ok + total_dl_nok)

        ul_bler = 0.0
        if (total_ul_ok + total_ul_nok) > 0:
            ul_bler = total_ul_nok / (total_ul_ok + total_ul_nok)

        obj = FiveGDUCellMetrics(
            pci=cell_data.get("pci", 0),
            average_latency=cell_data.get("average_latency", 0.0),
            max_latency=cell_data.get("max_latency", 0.0),
            pucch_tot_rb_usage_avg=cell_data.get("pucch_tot_rb_usage_avg", 0.0),
            active_ues=active_ues,
            dl_brate=total_dl_brate,
            ul_brate=total_ul_brate,
            dl_mcs=avg_dl_mcs,
            ul_mcs=avg_ul_mcs,
            pusch_snr_db=avg_pusch_snr,
            pucch_snr_db=avg_pucch_snr,
            cqi=avg_cqi,
            dl_bler=dl_bler,
            ul_bler=ul_bler,
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
        d["pci"] = self.pci
        d["average_latency"] = self.average_latency
        d["max_latency"] = self.max_latency
        d["pucch_tot_rb_usage_avg"] = self.pucch_tot_rb_usage_avg
        d["active_ues"] = self.active_ues
        d["dl_brate"] = self.dl_brate
        d["ul_brate"] = self.ul_brate
        d["dl_mcs"] = self.dl_mcs
        d["ul_mcs"] = self.ul_mcs
        d["pusch_snr_db"] = self.pusch_snr_db
        d["pucch_snr_db"] = self.pucch_snr_db
        d["cqi"] = self.cqi
        d["dl_bler"] = self.dl_bler
        d["ul_bler"] = self.ul_bler
        return d

    def copy(self) -> "FiveGDUCellMetrics":
        """
        :return: a copy of the object
        """
        c = FiveGDUCellMetrics(
            pci=self.pci, average_latency=self.average_latency,
            max_latency=self.max_latency,
            pucch_tot_rb_usage_avg=self.pucch_tot_rb_usage_avg,
            active_ues=self.active_ues, dl_brate=self.dl_brate,
            ul_brate=self.ul_brate, dl_mcs=self.dl_mcs, ul_mcs=self.ul_mcs,
            pusch_snr_db=self.pusch_snr_db, pucch_snr_db=self.pucch_snr_db,
            cqi=self.cqi, dl_bler=self.dl_bler, ul_bler=self.ul_bler,
            ip=self.ip, ts=self.ts
        )
        return c

    def num_attributes(self) -> int:
        """
        :return: The number of attributes of the DTO
        """
        return 16

    @staticmethod
    def schema() -> "FiveGDUCellMetrics":
        """
        :return: get the schema of the DTO
        """
        return FiveGDUCellMetrics()

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGDUCellMetrics":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGDUCellMetrics.from_dict(json.loads(json_str))
