from typing import Any
import pytest
import pytest_mock
from csle_collector.five_g_du_manager.five_g_du_manager_pb2 import FiveGDUStatusDTO
from csle_collector.five_g_du_manager.five_g_du_manager import FiveGDUManagerServicer
import csle_collector.five_g_du_manager.query_five_g_du_manager
import csle_collector.constants.constants as constants


class TestFiveGDUManagerSuite:
    """
    Test suite for the 5G du manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc import (
            add_FiveGDUManagerServicer_to_server)
        return add_FiveGDUManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> FiveGDUManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the 5G du manager servicer
        """
        servicer = FiveGDUManagerServicer()
        servicer.ip = "0.0.0.0"
        return servicer

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc import FiveGDUManagerStub
        return FiveGDUManagerStub

    def test_startFiveGDU(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFiveGDU grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'start_du', return_value=None)
        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        response: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du(
            stub=grpc_stub)
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: True}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=True, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        response_2: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du(
            stub=grpc_stub)
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert response_2.ip == mock_status.ip

    def test_stopFiveGDU(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopFiveGDU grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'stop_du', return_value=None)
        mock_status_dict_du = {constants.FIVE_G_DU.DU: False}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=False, ue_running=False, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        response: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du(
            stub=grpc_stub)
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        response_2: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du(
            stub=grpc_stub)
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert response_2.ip == mock_status.ip

    def test_getFiveGDUStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getFiveGDUStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mock_status_dict_du = {constants.FIVE_G_DU.DU: False}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: True}
        mock_status = FiveGDUStatusDTO(du_running=False, ue_running=True, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        response: FiveGDUStatusDTO = (csle_collector.five_g_du_manager.query_five_g_du_manager.
                                      get_five_g_du_status(stub=grpc_stub))
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        response_2: FiveGDUStatusDTO = (csle_collector.five_g_du_manager.query_five_g_du_manager.
                                        get_five_g_du_status(stub=grpc_stub))
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert response_2.ip == mock_status.ip
