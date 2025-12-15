from typing import List, Dict, Any
import csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc
import csle_collector.five_g_du_manager.five_g_du_manager_pb2
import csle_collector.five_g_du_manager.five_g_du_manager_util as five_g_du_manager_util
from csle_base.json_serializable import JSONSerializable


class FiveGDUManagersInfo(JSONSerializable):
    """
    DTO containing the status of the 5G DU managers for a given emulation execution
    """

    def __init__(
            self, ips: List[str], ports: List[int], emulation_name: str, execution_id: int,
            five_g_du_managers_statuses: List[
                csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO],
            five_g_du_managers_running: List[bool]):
        """
        Initializes the DTO

        :param five_g_du_managers_running: list of booleans that indicate whether the 5G DU managers are running
        :param ips: the list of IPs of the running 5G DU managers
        :param ports: the list of ports of the running 5G DU managers
        :param emulation_name: the name of the corresponding emulation
        :param execution_id: the ID of the corresponding emulation execution
        :param five_g_du_managers_statuses: a list of statuses of the 5G DU managers
        """
        self.five_g_du_managers_running = five_g_du_managers_running
        self.ips = ips
        self.ports = ports
        self.emulation_name = emulation_name
        self.execution_id = execution_id
        self.five_g_du_managers_statuses = five_g_du_managers_statuses

    def __str__(self):
        """
        :return: a string representation of the DTO
        """
        return f"five_g_du_managers_running: {self.five_g_du_managers_running}, " \
               f"ips: {list(map(lambda x: str(x), self.ips))}, " \
               f"emulation_name: {self.emulation_name}, " \
               f"execution_id: {self.execution_id}, " \
               f"five_g_du_managers_statuses: {list(map(lambda x: str(x), self.five_g_du_managers_statuses))}," \
               f" ports: {list(map(lambda x: str(x), self.ports))}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["five_g_du_managers_running"] = self.five_g_du_managers_running
        d["ips"] = self.ips
        d["ports"] = self.ports
        d["emulation_name"] = self.emulation_name
        d["execution_id"] = self.execution_id
        d["five_g_du_managers_statuses"] = list(map(
            lambda x: five_g_du_manager_util.FiveGDUManagerUtil.five_g_du_status_dto_to_dict(x),
            self.five_g_du_managers_statuses))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGDUManagersInfo":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = FiveGDUManagersInfo(
            five_g_du_managers_running=d["five_g_du_managers_running"], ips=d["ips"], ports=d["ports"],
            emulation_name=d["emulation_name"], execution_id=d["execution_id"],
            five_g_du_managers_statuses=list(map(
                lambda x: five_g_du_manager_util.FiveGDUManagerUtil.five_g_du_status_dto_from_dict(x),
                d["five_g_du_managers_statuses"])))
        return dto

    @staticmethod
    def get_empty_dto() -> "FiveGDUManagersInfo":
        """
        :return: an empty version of the DTO
        """
        return FiveGDUManagersInfo(
            ips=[], ports=[], emulation_name="", execution_id=-1, five_g_du_managers_statuses=[],
            five_g_du_managers_running=[])

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGDUManagersInfo":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGDUManagersInfo.from_dict(json.loads(json_str))
