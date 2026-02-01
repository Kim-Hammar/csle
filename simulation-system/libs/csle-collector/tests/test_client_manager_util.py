from csle_collector.client_manager.client_manager_util import ClientManagerUtil
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO


class TestClientManagerUtilSuite:
    """
    Test suite for ClientManagerUtil
    """

    def test_client_dto_to_dict(self) -> None:
        """
        Tests the client_dto_to_dict function
        """
        dto = ClientsDTO()
        dto.num_clients = 10
        dto.client_process_active = True
        dto.producer_active = False
        dto.clients_time_step_len_seconds = 5
        dto.producer_time_step_len_seconds = 2
        
        d = ClientManagerUtil.client_dto_to_dict(dto)
        assert d["num_clients"] == 10
        assert d["client_process_active"] is True
        assert d["producer_active"] is False
        assert d["clients_time_step_len_seconds"] == 5
        assert d["producer_time_step_len_seconds"] == 2

    def test_clients_dto_from_dict(self) -> None:
        """
        Tests the clients_dto_from_dict function
        """
        d = {
            "num_clients": 5,
            "client_process_active": False,
            "producer_active": True,
            "clients_time_step_len_seconds": 10,
            "producer_time_step_len_seconds": 4
        }
        dto = ClientManagerUtil.clients_dto_from_dict(d)
        assert dto.num_clients == 5
        assert dto.client_process_active is False
        assert dto.producer_active is True
        assert dto.clients_time_step_len_seconds == 10
        assert dto.producer_time_step_len_seconds == 4

    def test_clients_dto_empty(self) -> None:
        """
        Tests the clients_dto_empty function
        """
        dto = ClientManagerUtil.clients_dto_empty()
        assert dto.num_clients == 0
        assert dto.client_process_active is False
        assert dto.producer_active is False
        assert dto.clients_time_step_len_seconds == 0
        assert dto.producer_time_step_len_seconds == 0
