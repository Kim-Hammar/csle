from typing import Any
import pytest
import pytest_mock
from csle_collector.five_g_du_manager.five_g_du_manager_pb2 import FiveGDUStatusDTO
from csle_collector.five_g_du_manager.five_g_du_manager import FiveGDUManagerServicer
import csle_collector.five_g_du_manager.query_five_g_du_manager
import csle_collector.constants.constants as constants


class TestFiveGDUManagerSuite:
    """
    Test suite for the 5G DU manager
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
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du(
            stub=grpc_stub)
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.monitor_running == mock_status.monitor_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: True}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du(
            stub=grpc_stub)
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert response_2.monitor_running == mock_status.monitor_running
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
        mock_status = FiveGDUStatusDTO(du_running=False, ue_running=False, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du(
            stub=grpc_stub)
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.monitor_running == mock_status.monitor_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du(
            stub=grpc_stub)
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert response_2.monitor_running == mock_status.monitor_running
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
        mock_status = FiveGDUStatusDTO(du_running=False, ue_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGDUStatusDTO = (csle_collector.five_g_du_manager.query_five_g_du_manager.
                                      get_five_g_du_status(stub=grpc_stub))
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.monitor_running == mock_status.monitor_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGDUStatusDTO = (csle_collector.five_g_du_manager.query_five_g_du_manager.
                                        get_five_g_du_status(stub=grpc_stub))
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert response_2.ip == mock_status.ip
        assert response_2.monitor_running == mock_status.monitor_running

    def test_initFiveGDUUE(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the initFiveGDUUE grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'init_du_config_file', return_value=None)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'init_ue', return_value=None)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'init_ue_config_file', return_value=None)
        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        cu_fronthaul_ip = "127.0.0.1"
        du_fronthaul_ip = "127.0.0.1"
        imsi = "imsi"
        key = "key"
        opc = "opc"
        imei = "353490069873319"
        gnb_du_id = 0
        pci = 1
        sector_id = 0
        response: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.init_five_g_du_ue(
            stub=grpc_stub, cu_fronthaul_ip=cu_fronthaul_ip, du_fronthaul_ip=du_fronthaul_ip, imsi=imsi, key=key,
            opc=opc, imei=imei, gnb_du_id=gnb_du_id, pci=pci, sector_id=sector_id)
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.ip == mock_status.ip
        assert response.monitor_running == mock_status.monitor_running

    def test_stopFiveGDUMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopFiveGDUMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du_monitor(
            stub=grpc_stub)
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert not response.monitor_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: True}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du_monitor(
            stub=grpc_stub)
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert not response_2.monitor_running
        assert response_2.ip == mock_status.ip

    def test_startFiveGDUMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFiveGDUMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_du_manager.threads.five_g_du_monitor_thread.'
                     'FiveGDUMonitorThread.run', return_value=True)
        mocker.patch('csle_collector.five_g_du_manager.threads.five_g_du_monitor_thread.'
                     'FiveGDUMonitorThread.__init__', return_value=None)
        mocker.patch('csle_collector.five_g_du_manager.threads.five_g_du_monitor_thread.'
                     'FiveGDUMonitorThread.start', return_value=True)
        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: False}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=False, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        kafka_ip = "test_kafka_ip"
        kafka_port = 9292
        time_step_len_seconds = 30
        response: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du_monitor(
            stub=grpc_stub, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds, kafka_ip=kafka_ip)
        assert response.du_running == mock_status.du_running
        assert response.ue_running == mock_status.ue_running
        assert response.monitor_running
        assert response.ip == mock_status.ip

        mock_status_dict_du = {constants.FIVE_G_DU.DU: True}
        mock_status_dict_ue = {constants.FIVE_G_DU.UE: True}
        mock_status = FiveGDUStatusDTO(du_running=True, ue_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_du_status', return_value=mock_status_dict_du)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager_util.FiveGDUManagerUtil.'
                     'get_ue_status', return_value=mock_status_dict_ue)
        mocker.patch('csle_collector.five_g_du_manager.five_g_du_manager.FiveGDUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGDUStatusDTO = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du_monitor(
            stub=grpc_stub, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds, kafka_ip=kafka_ip)
        assert response_2.du_running == mock_status.du_running
        assert response_2.ue_running == mock_status.ue_running
        assert response_2.monitor_running
        assert response_2.ip == mock_status.ip
