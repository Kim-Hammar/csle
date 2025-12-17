from typing import Dict, Any, Union, List
from csle_base.json_serializable import JSONSerializable
from csle_common.dao.emulation_config.five_g_subscriber_config import FiveGSubscriberConfig
from csle_common.util.general_util import GeneralUtil


class FiveGConfig(JSONSerializable):
    """
    Represents the configuration of the 5G services and managers in a CSLE emulation
    """

    def __init__(self, five_g_core_manager_log_file: str, five_g_core_manager_log_dir: str,
                 five_g_core_manager_max_workers: int,
                 five_g_cu_manager_log_file: str, five_g_cu_manager_log_dir: str,
                 five_g_cu_manager_max_workers: int,
                 five_g_du_manager_log_file: str, five_g_du_manager_log_dir: str,
                 five_g_du_manager_max_workers: int, subscribers: List[FiveGSubscriberConfig],
                 core_backhaul_ip: str,
                 cu_backhaul_ips: List[str], cu_fronthaul_ips: List[str],
                 du_fronthaul_ips: List[str], du_cus: List[str],
                 time_step_len_seconds: int = 15, five_g_core_manager_port: int = 50052,
                 five_g_cu_manager_port: int = 50053, five_g_du_manager_port: int = 50054,
                 version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param version: the version
        :param subscribers: the 5G subscribers
        :param core_backhaul_ip: the IP of the core network as seen to the RAN
        :param cu_backhaul_ips: the backhaul IPs of the CUs
        :param cu_fronthaul_ips: the fronthaul IPs of the CUs
        :param du_fronthaul_ips: the fronthaul IPs of the DUs
        :param du_cus: the CUs for each DU
        :param five_g_core_manager_port: the GRPC port of the 5G core manager
        :param five_g_core_manager_log_file: Log file of the 5G core manager
        :param five_g_core_manager_log_dir: Log dir of the 5G core manager
        :param five_g_core_manager_max_workers: Max GRPC workers of the 5G core manager
        :param five_g_cu_manager_port: the GRPC port of the 5G cu manager
        :param five_g_cu_manager_log_file: Log file of the 5G cu manager
        :param five_g_cu_manager_log_dir: Log dir of the 5G cu manager
        :param five_g_cu_manager_max_workers: Max GRPC workers of the 5G cu manager
        :param five_g_du_manager_port: the GRPC port of the 5G du manager
        :param five_g_du_manager_log_file: Log file of the 5G du manager
        :param five_g_du_manager_log_dir: Log dir of the 5G du manager
        :param five_g_du_manager_max_workers: Max GRPC workers of the 5G du manager
        """
        self.time_step_len_seconds = time_step_len_seconds
        self.version = version

        self.five_g_core_manager_port = five_g_core_manager_port
        self.five_g_core_manager_log_file = five_g_core_manager_log_file
        self.five_g_core_manager_log_dir = five_g_core_manager_log_dir
        self.five_g_core_manager_max_workers = five_g_core_manager_max_workers

        self.five_g_cu_manager_port = five_g_cu_manager_port
        self.five_g_cu_manager_log_file = five_g_cu_manager_log_file
        self.five_g_cu_manager_log_dir = five_g_cu_manager_log_dir
        self.five_g_cu_manager_max_workers = five_g_cu_manager_max_workers

        self.five_g_du_manager_port = five_g_du_manager_port
        self.five_g_du_manager_log_file = five_g_du_manager_log_file
        self.five_g_du_manager_log_dir = five_g_du_manager_log_dir
        self.five_g_du_manager_max_workers = five_g_du_manager_max_workers

        self.subscribers = subscribers
        self.core_backhaul_ip = core_backhaul_ip
        self.cu_backhaul_ips = cu_backhaul_ips
        self.cu_fronthaul_ips = cu_fronthaul_ips
        self.du_fronthaul_ips = du_fronthaul_ips
        self.du_cus = du_cus

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGConfig(
            time_step_len_seconds=d["time_step_len_seconds"], version=d["version"],
            five_g_core_manager_log_file=d["five_g_core_manager_log_file"],
            five_g_core_manager_log_dir=d["five_g_core_manager_log_dir"],
            five_g_core_manager_max_workers=d["five_g_core_manager_max_workers"],
            five_g_core_manager_port=d["five_g_core_manager_port"],
            five_g_cu_manager_log_file=d["five_g_cu_manager_log_file"],
            five_g_cu_manager_log_dir=d["five_g_cu_manager_log_dir"],
            five_g_cu_manager_max_workers=d["five_g_cu_manager_max_workers"],
            five_g_cu_manager_port=d["five_g_cu_manager_port"],
            five_g_du_manager_log_file=d["five_g_du_manager_log_file"],
            five_g_du_manager_log_dir=d["five_g_du_manager_log_dir"],
            five_g_du_manager_max_workers=d["five_g_du_manager_max_workers"],
            five_g_du_manager_port=d["five_g_du_manager_port"],
            subscribers=list(map(lambda x: FiveGSubscriberConfig.from_dict(x), d["subscribers"])),
            core_backhaul_ip=d["core_backhaul_ip"],
            cu_backhaul_ips=d["cu_backhaul_ips"],
            cu_fronthaul_ips=d["cu_fronthaul_ips"],
            du_fronthaul_ips=d["du_fronthaul_ips"],
            du_cus=d["du_cus"]
        )
        return obj

    def to_dict(self) -> Dict[str, Union[str, int, List[str], List[Dict[str, Union[str, int]]]]]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int, List[str], List[Dict[str, Union[str, int]]]]] = {}
        d["time_step_len_seconds"] = self.time_step_len_seconds
        d["version"] = self.version
        d["five_g_core_manager_log_file"] = self.five_g_core_manager_log_file
        d["five_g_core_manager_log_dir"] = self.five_g_core_manager_log_dir
        d["five_g_core_manager_max_workers"] = self.five_g_core_manager_max_workers
        d["five_g_core_manager_port"] = self.five_g_core_manager_port
        d["five_g_cu_manager_log_file"] = self.five_g_cu_manager_log_file
        d["five_g_cu_manager_log_dir"] = self.five_g_cu_manager_log_dir
        d["five_g_cu_manager_max_workers"] = self.five_g_cu_manager_max_workers
        d["five_g_cu_manager_port"] = self.five_g_cu_manager_port
        d["five_g_du_manager_log_file"] = self.five_g_du_manager_log_file
        d["five_g_du_manager_log_dir"] = self.five_g_du_manager_log_dir
        d["five_g_du_manager_max_workers"] = self.five_g_du_manager_max_workers
        d["five_g_du_manager_port"] = self.five_g_du_manager_port
        d["subscribers"] = list(map(lambda x: x.to_dict(), self.subscribers))
        d["core_backhaul_ip"] = self.core_backhaul_ip
        d["cu_backhaul_ips"] = self.cu_backhaul_ips
        d["cu_fronthaul_ips"] = self.cu_fronthaul_ips
        d["du_fronthaul_ips"] = self.du_fronthaul_ips
        d["du_cus"] = self.du_cus
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return (f"time_step_len_seconds: {self.time_step_len_seconds}, version: {self.version}, "
                f"five_g_core_manager_log_file: {self.five_g_core_manager_log_file}, "
                f"five_g_core_manager_log_dir: {self.five_g_core_manager_log_dir}, "
                f"five_g_core_manager_max_workers: {self.five_g_core_manager_max_workers}, "
                f"five_g_core_manager_port: {self.five_g_core_manager_port}"
                f"five_g_cu_manager_log_file: {self.five_g_cu_manager_log_file}, "
                f"five_g_cu_manager_log_dir: {self.five_g_cu_manager_log_dir}, "
                f"five_g_cu_manager_max_workers: {self.five_g_cu_manager_max_workers}, "
                f"five_g_cu_manager_port: {self.five_g_cu_manager_port}"
                f"five_g_du_manager_log_file: {self.five_g_du_manager_log_file}, "
                f"five_g_du_manager_log_dir: {self.five_g_du_manager_log_dir}, "
                f"five_g_du_manager_max_workers: {self.five_g_du_manager_max_workers}, "
                f"five_g_du_manager_port: {self.five_g_du_manager_port}, "
                f"subscribers: {self.subscribers}, core_backhaul_ip: {self.core_backhaul_ip},"
                f"cu_backhaul_ips: {self.cu_backhaul_ips}, cu_fronthaul_ips: {self.cu_fronthaul_ips}, "
                f"du_fronthaul_ips: {self.du_fronthaul_ips}, du_cus: {self.du_cus}")

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGConfig.from_dict(json.loads(json_str))

    def copy(self) -> "FiveGConfig":
        """
        :return: a copy of the DTO
        """
        return FiveGConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "FiveGConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.core_backhaul_ip = GeneralUtil.replace_first_octet_of_ip(ip=config.core_backhaul_ip,
                                                                        ip_first_octet=ip_first_octet)
        config.cu_backhaul_ips = list(
            map(lambda x: GeneralUtil.replace_first_octet_of_ip(ip=x, ip_first_octet=ip_first_octet),
                config.cu_backhaul_ips))
        config.cu_fronthaul_ips = list(
            map(lambda x: GeneralUtil.replace_first_octet_of_ip(ip=x, ip_first_octet=ip_first_octet),
                config.cu_fronthaul_ips))
        config.du_fronthaul_ips = list(
            map(lambda x: GeneralUtil.replace_first_octet_of_ip(ip=x, ip_first_octet=ip_first_octet),
                config.du_fronthaul_ips))
        config.du_cus = list(
            map(lambda x: GeneralUtil.replace_first_octet_of_ip(ip=x, ip_first_octet=ip_first_octet),
                config.du_cus))
        return config

    @staticmethod
    def schema() -> "FiveGConfig":
        """
        :return: get the schema of the DTO
        """
        return FiveGConfig(
            version="0.0.1", time_step_len_seconds=15,
            five_g_core_manager_log_file="five_g_core_manager.log",
            five_g_core_manager_port=50052,
            five_g_core_manager_log_dir="/",
            five_g_core_manager_max_workers=10,
            five_g_cu_manager_log_file="five_g_cu_manager.log",
            five_g_cu_manager_port=50052,
            five_g_cu_manager_log_dir="/",
            five_g_cu_manager_max_workers=10,
            five_g_du_manager_log_file="five_g_du_manager.log",
            five_g_du_manager_port=50052,
            five_g_du_manager_log_dir="/",
            five_g_du_manager_max_workers=10,
            subscribers=[], core_backhaul_ip="127.0.0.1",
            cu_backhaul_ips=["127.0.0.1"], cu_fronthaul_ips=["127.0.0.1"],
            du_fronthaul_ips=["127.0.0.1"], du_cus=["127.0.0.1"]
        )
