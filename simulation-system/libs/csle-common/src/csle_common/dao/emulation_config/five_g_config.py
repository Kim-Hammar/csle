from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable


class FiveGConfig(JSONSerializable):
    """
    Represents the configuration of the 5G services and managers in a CSLE emulation
    """

    def __init__(self, five_g_core_manager_log_file: str, five_g_core_manager_log_dir: str,
                 five_g_core_manager_max_workers: int,
                 five_g_cu_manager_log_file: str, five_g_cu_manager_log_dir: str,
                 five_g_cu_manager_max_workers: int,
                 five_g_du_manager_log_file: str, five_g_du_manager_log_dir: str,
                 five_g_du_manager_max_workers: int,
                 time_step_len_seconds: int = 15, five_g_core_manager_port: int = 50052,
                 five_g_cu_manager_port: int = 50053, five_g_du_manager_port: int = 50054,
                 version: str = "0.0.1") -> None:
        """
        Initializes the DTO

        :param time_step_len_seconds: the length of a time-step (period for logging)
        :param version: the version
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
            five_g_du_manager_port=d["five_g_du_manager_port"]
        )
        return obj

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int]] = {}
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
                f"five_g_du_manager_port: {self.five_g_du_manager_port}")

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
            five_g_du_manager_max_workers=10
        )
