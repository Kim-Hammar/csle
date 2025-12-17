from typing import Dict, Any, Union
from csle_base.json_serializable import JSONSerializable
from csle_collector.five_g_core_manager.five_g_core_manager_pb2 import SubscriberDTO


class FiveGSubscriberConfig(JSONSerializable):
    """
    DTO representing the configuration of a 5G subscriber
    """

    def __init__(self, imsi: str, key: str, opc: str, amf: str, sqn: int) -> None:
        """
        Initializes the DTO

        :param imsi: the imsi of the subscriber (International Mobile Subscriber Identity)
        :param key: the private key of the subscriber
        :param opc: the operator key
        :param amf: the AMF (Authentication Management Field)
        :param sqn: the sequence number (SQN)
        """
        self.imsi = imsi
        self.key = key
        self.opc = opc
        self.amf = amf
        self.sqn = sqn

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "FiveGSubscriberConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = FiveGSubscriberConfig(imsi=d["imsi"], key=d["key"], opc=d["opc"], amf=d["amf"], sqn=d["sqn"])
        return obj

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int]] = {}
        d["imsi"] = self.imsi
        d["key"] = self.key
        d["opc"] = self.opc
        d["amf"] = self.amf
        d["sqn"] = self.sqn
        return d

    def to_subscriber_dto(self) -> SubscriberDTO:
        """
        Converts the object to a SubscriberDTO

        :return: the created SubscriberDTO
        """
        return SubscriberDTO(imsi=self.imsi, key=self.key, opc=self.opc, amf=self.amf, sqn=self.sqn)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"imsi: {self.imsi}, key: {self.key}, opc: {self.opc}, amf: {self.amf}, sqn: {self.sqn}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "FiveGSubscriberConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return FiveGSubscriberConfig.from_dict(json.loads(json_str))

    def copy(self) -> "FiveGSubscriberConfig":
        """
        :return: a copy of the DTO
        """
        return FiveGSubscriberConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "FiveGSubscriberConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        return config

    @staticmethod
    def schema() -> "FiveGSubscriberConfig":
        """
        :return: get the schema of the DTO
        """
        return FiveGSubscriberConfig(
            imsi="001010123456780", key="00112233445566778899aabbccddeeff", opc="63BFA50EE6523365FF14C1F45F88737D",
            amf="8000", sqn=10
        )
