from typing import Any
import pytest
import pytest_mock
from csle_collector.five_g_cu_manager.five_g_cu_manager_pb2 import FiveGCUStatusDTO
from csle_collector.five_g_cu_manager.five_g_cu_manager import FiveGCUManagerServicer
import csle_collector.five_g_cu_manager.query_five_g_cu_manager
import csle_collector.constants.constants as constants


class TestFiveGCUManagerSuite:
    """
    Test suite for the 5G cu manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc import (
            add_FiveGCUManagerServicer_to_server)
        return add_FiveGCUManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> FiveGCUManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the 5G cu manager servicer
        """
        servicer = FiveGCUManagerServicer()
        servicer.ip = "0.0.0.0"
        return servicer

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc import FiveGCUManagerStub
        return FiveGCUManagerStub

    def test_startFiveGCU(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFiveGCU grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'start_cu', return_value=None)
        mock_status_dict = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.start_five_g_cu(
            stub=grpc_stub)
        assert response.cu_running == mock_status.cu_running
        assert response.ip == mock_status.ip
        assert response.monitor_running == mock_status.monitor_running

        mock_status_dict = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.start_five_g_cu(
            stub=grpc_stub)
        assert response_2.cu_running == mock_status.cu_running
        assert response_2.ip == mock_status.ip
        assert response_2.monitor_running == mock_status.monitor_running

    def test_stopFiveGCU(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopFiveGCU grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'stop_cu', return_value=None)
        mock_status_dict = {constants.FIVE_G_CU.CU: False}
        mock_status = FiveGCUStatusDTO(cu_running=False, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.stop_five_g_cu(
            stub=grpc_stub)
        assert response.cu_running == mock_status.cu_running
        assert response.ip == mock_status.ip
        assert response.monitor_running == mock_status.monitor_running

        mock_status_dict = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.stop_five_g_cu(
            stub=grpc_stub)
        assert response_2.cu_running == mock_status.cu_running
        assert response_2.ip == mock_status.ip
        assert response_2.monitor_running == mock_status.monitor_running

    def test_getFiveGCUStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getFiveGCUStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mock_status_dict = {constants.FIVE_G_CU.CU: False}
        mock_status = FiveGCUStatusDTO(cu_running=False, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGCUStatusDTO = (csle_collector.five_g_cu_manager.query_five_g_cu_manager.
                                      get_five_g_cu_status(stub=grpc_stub))
        assert response.cu_running == mock_status.cu_running
        assert response.ip == mock_status.ip
        assert response.monitor_running == mock_status.monitor_running

        mock_status_dict = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGCUStatusDTO = (csle_collector.five_g_cu_manager.query_five_g_cu_manager.
                                        get_five_g_cu_status(stub=grpc_stub))
        assert response_2.cu_running == mock_status.cu_running
        assert response_2.ip == mock_status.ip
        assert response_2.monitor_running == mock_status.monitor_running

    def test_initFiveGCU(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the initFiveGCU grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'init_config_file', return_value=None)
        mock_status_dict = {constants.FIVE_G_CU.CU: False}
        mock_status = FiveGCUStatusDTO(cu_running=False, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.init_five_g_cu(
            core_backhaul_ip="127.0.0.1", cu_backhaul_ip="127.0.0.1", cu_fronthaul_ip="127.0.0.1", stub=grpc_stub)
        assert response.cu_running == mock_status.cu_running
        assert response.ip == mock_status.ip
        assert response.monitor_running == mock_status.monitor_running

        mock_status_dict = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.init_five_g_cu(
            core_backhaul_ip="127.0.0.1", cu_backhaul_ip="127.0.0.1", cu_fronthaul_ip="127.0.0.1", stub=grpc_stub)
        assert response_2.cu_running == mock_status.cu_running
        assert response_2.ip == mock_status.ip
        assert response_2.monitor_running == mock_status.monitor_running

    def test_stopFiveGCUMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopFiveGCUMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mock_status_dict_cu = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict_cu)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.stop_five_g_cu_monitor(
            stub=grpc_stub)
        assert response.cu_running == mock_status.cu_running
        assert not response.monitor_running
        assert response.ip == mock_status.ip

        mock_status_dict_cu = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict_cu)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.stop_five_g_cu_monitor(
            stub=grpc_stub)
        assert response_2.cu_running == mock_status.cu_running
        assert not response_2.monitor_running
        assert response_2.ip == mock_status.ip

    def test_startFiveGCUMonitor(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFiveGCUMonitor grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_cu_manager.threads.five_g_cu_monitor_thread.'
                     'FiveGCUMonitorThread.run', return_value=True)
        mocker.patch('csle_collector.five_g_cu_manager.threads.five_g_cu_monitor_thread.'
                     'FiveGCUMonitorThread.__init__', return_value=None)
        mocker.patch('csle_collector.five_g_cu_manager.threads.five_g_cu_monitor_thread.'
                     'FiveGCUMonitorThread.start', return_value=True)
        mock_status_dict_cu = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=True)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict_cu)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        kafka_ip = "test_kafka_ip"
        kafka_port = 9292
        time_step_len_seconds = 30
        response: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.start_five_g_cu_monitor(
            stub=grpc_stub, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds, kafka_ip=kafka_ip)
        assert response.cu_running == mock_status.cu_running
        assert response.monitor_running
        assert response.ip == mock_status.ip

        mock_status_dict_cu = {constants.FIVE_G_CU.CU: True}
        mock_status = FiveGCUStatusDTO(cu_running=True, ip="0.0.0.0", monitor_running=False)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil.'
                     'get_cu_status', return_value=mock_status_dict_cu)
        mocker.patch('csle_collector.five_g_cu_manager.five_g_cu_manager.FiveGCUManagerServicer.'
                     '_is_monitor_running', return_value=mock_status.monitor_running)
        response_2: FiveGCUStatusDTO = csle_collector.five_g_cu_manager.query_five_g_cu_manager.start_five_g_cu_monitor(
            stub=grpc_stub, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds, kafka_ip=kafka_ip)
        assert response_2.cu_running == mock_status.cu_running
        assert response_2.monitor_running
        assert response_2.ip == mock_status.ip
