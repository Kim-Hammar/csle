from typing import Any
import pytest
import pytest_mock
from csle_collector.five_g_core_manager.five_g_core_manager_pb2 import FiveGCoreStatusDTO
from csle_collector.five_g_core_manager.five_g_core_manager import FiveGCoreManagerServicer
import csle_collector.five_g_core_manager.query_five_g_core_manager
import csle_collector.constants.constants as constants


class TestFiveGCoreManagerSuite:
    """
    Test suite for the 5G core manager
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self) -> Any:
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc import (
            add_FiveGCoreManagerServicer_to_server)
        return add_FiveGCoreManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> FiveGCoreManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the 5G core manager servicer
        """
        servicer = FiveGCoreManagerServicer()
        servicer.ip = "0.0.0.0"
        return servicer

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        from csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc import FiveGCoreManagerStub
        return FiveGCoreManagerStub

    def test_startFiveGCore(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the startFiveGCore grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'start_all_core_services', return_value=None)
        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: True,
            constants.FIVE_G_CORE.MME: True,
            constants.FIVE_G_CORE.SGWC: True,
            constants.FIVE_G_CORE.SMF: True,
            constants.FIVE_G_CORE.AMF: True,
            constants.FIVE_G_CORE.SGWU: True,
            constants.FIVE_G_CORE.UPF: True,
            constants.FIVE_G_CORE.HSS: True,
            constants.FIVE_G_CORE.PCRF: True,
            constants.FIVE_G_CORE.NRF: True,
            constants.FIVE_G_CORE.SCP: True,
            constants.FIVE_G_CORE.SEPP: True,
            constants.FIVE_G_CORE.AUSF: True,
            constants.FIVE_G_CORE.UDM: True,
            constants.FIVE_G_CORE.PCF: True,
            constants.FIVE_G_CORE.NSSF: True,
            constants.FIVE_G_CORE.BSF: True,
            constants.FIVE_G_CORE.UDR: True,
            constants.FIVE_G_CORE.WEBUI: True
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=True, mme_running=True, sgwc_running=True, smf_running=True, amf_running=True,
            sgwu_running=True, upf_running=True, hss_running=True, pcrf_running=True, nrf_running=True,
            scp_running=True, sepp_running=True, ausf_running=True, udm_running=True, pcf_running=True,
            nssf_running=True, bsf_running=True, udr_running=True, webui_running=True, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response: FiveGCoreStatusDTO = csle_collector.five_g_core_manager.query_five_g_core_manager.start_five_g_core(
            stub=grpc_stub)
        assert response.mongo_running == mock_status.mongo_running
        assert response.mme_running == mock_status.mme_running
        assert response.sgwc_running == mock_status.sgwc_running
        assert response.smf_running == mock_status.smf_running
        assert response.amf_running == mock_status.amf_running
        assert response.sgwu_running == mock_status.sgwu_running
        assert response.upf_running == mock_status.upf_running
        assert response.hss_running == mock_status.hss_running
        assert response.pcrf_running == mock_status.pcrf_running
        assert response.nrf_running == mock_status.nrf_running
        assert response.scp_running == mock_status.scp_running
        assert response.sepp_running == mock_status.sepp_running
        assert response.ausf_running == mock_status.ausf_running
        assert response.udm_running == mock_status.udm_running
        assert response.pcf_running == mock_status.pcf_running
        assert response.nssf_running == mock_status.nssf_running
        assert response.bsf_running == mock_status.bsf_running
        assert response.udr_running == mock_status.udr_running
        assert response.webui_running == mock_status.webui_running
        assert response.ip == mock_status.ip

        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: True,
            constants.FIVE_G_CORE.MME: True,
            constants.FIVE_G_CORE.SGWC: True,
            constants.FIVE_G_CORE.SMF: True,
            constants.FIVE_G_CORE.AMF: False,
            constants.FIVE_G_CORE.SGWU: True,
            constants.FIVE_G_CORE.UPF: True,
            constants.FIVE_G_CORE.HSS: True,
            constants.FIVE_G_CORE.PCRF: True,
            constants.FIVE_G_CORE.NRF: True,
            constants.FIVE_G_CORE.SCP: True,
            constants.FIVE_G_CORE.SEPP: True,
            constants.FIVE_G_CORE.AUSF: False,
            constants.FIVE_G_CORE.UDM: True,
            constants.FIVE_G_CORE.PCF: True,
            constants.FIVE_G_CORE.NSSF: True,
            constants.FIVE_G_CORE.BSF: True,
            constants.FIVE_G_CORE.UDR: True,
            constants.FIVE_G_CORE.WEBUI: True
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=True, mme_running=True, sgwc_running=True, smf_running=True, amf_running=False,
            sgwu_running=True, upf_running=True, hss_running=True, pcrf_running=True, nrf_running=True,
            scp_running=True, sepp_running=True, ausf_running=False, udm_running=True, pcf_running=True,
            nssf_running=True, bsf_running=True, udr_running=True, webui_running=True, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response_2: FiveGCoreStatusDTO = csle_collector.five_g_core_manager.query_five_g_core_manager.start_five_g_core(
            stub=grpc_stub)
        assert response_2.mongo_running == mock_status.mongo_running
        assert response_2.mme_running == mock_status.mme_running
        assert response_2.sgwc_running == mock_status.sgwc_running
        assert response_2.smf_running == mock_status.smf_running
        assert response_2.amf_running == mock_status.amf_running
        assert response_2.sgwu_running == mock_status.sgwu_running
        assert response_2.upf_running == mock_status.upf_running
        assert response_2.hss_running == mock_status.hss_running
        assert response_2.pcrf_running == mock_status.pcrf_running
        assert response_2.nrf_running == mock_status.nrf_running
        assert response_2.scp_running == mock_status.scp_running
        assert response_2.sepp_running == mock_status.sepp_running
        assert response_2.ausf_running == mock_status.ausf_running
        assert response_2.udm_running == mock_status.udm_running
        assert response_2.pcf_running == mock_status.pcf_running
        assert response_2.nssf_running == mock_status.nssf_running
        assert response_2.bsf_running == mock_status.bsf_running
        assert response_2.udr_running == mock_status.udr_running
        assert response_2.webui_running == mock_status.webui_running
        assert response_2.ip == mock_status.ip

    def test_stopFiveGCore(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the stopFiveGCore grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'stop_all_core_services', return_value=None)
        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: False,
            constants.FIVE_G_CORE.MME: False,
            constants.FIVE_G_CORE.SGWC: False,
            constants.FIVE_G_CORE.SMF: False,
            constants.FIVE_G_CORE.AMF: False,
            constants.FIVE_G_CORE.SGWU: False,
            constants.FIVE_G_CORE.UPF: False,
            constants.FIVE_G_CORE.HSS: False,
            constants.FIVE_G_CORE.PCRF: False,
            constants.FIVE_G_CORE.NRF: False,
            constants.FIVE_G_CORE.SCP: False,
            constants.FIVE_G_CORE.SEPP: False,
            constants.FIVE_G_CORE.AUSF: False,
            constants.FIVE_G_CORE.UDM: False,
            constants.FIVE_G_CORE.PCF: False,
            constants.FIVE_G_CORE.NSSF: False,
            constants.FIVE_G_CORE.BSF: False,
            constants.FIVE_G_CORE.UDR: False,
            constants.FIVE_G_CORE.WEBUI: False
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=False, mme_running=False, sgwc_running=False, smf_running=False, amf_running=False,
            sgwu_running=False, upf_running=False, hss_running=False, pcrf_running=False, nrf_running=False,
            scp_running=False, sepp_running=False, ausf_running=False, udm_running=False, pcf_running=False,
            nssf_running=False, bsf_running=False, udr_running=False, webui_running=False, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response: FiveGCoreStatusDTO = csle_collector.five_g_core_manager.query_five_g_core_manager.stop_five_g_core(
            stub=grpc_stub)
        assert response.mongo_running == mock_status.mongo_running
        assert response.mme_running == mock_status.mme_running
        assert response.sgwc_running == mock_status.sgwc_running
        assert response.smf_running == mock_status.smf_running
        assert response.amf_running == mock_status.amf_running
        assert response.sgwu_running == mock_status.sgwu_running
        assert response.upf_running == mock_status.upf_running
        assert response.hss_running == mock_status.hss_running
        assert response.pcrf_running == mock_status.pcrf_running
        assert response.nrf_running == mock_status.nrf_running
        assert response.scp_running == mock_status.scp_running
        assert response.sepp_running == mock_status.sepp_running
        assert response.ausf_running == mock_status.ausf_running
        assert response.udm_running == mock_status.udm_running
        assert response.pcf_running == mock_status.pcf_running
        assert response.nssf_running == mock_status.nssf_running
        assert response.bsf_running == mock_status.bsf_running
        assert response.udr_running == mock_status.udr_running
        assert response.webui_running == mock_status.webui_running
        assert response.ip == mock_status.ip

        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: True,
            constants.FIVE_G_CORE.MME: True,
            constants.FIVE_G_CORE.SGWC: True,
            constants.FIVE_G_CORE.SMF: True,
            constants.FIVE_G_CORE.AMF: False,
            constants.FIVE_G_CORE.SGWU: True,
            constants.FIVE_G_CORE.UPF: True,
            constants.FIVE_G_CORE.HSS: True,
            constants.FIVE_G_CORE.PCRF: True,
            constants.FIVE_G_CORE.NRF: True,
            constants.FIVE_G_CORE.SCP: True,
            constants.FIVE_G_CORE.SEPP: True,
            constants.FIVE_G_CORE.AUSF: False,
            constants.FIVE_G_CORE.UDM: True,
            constants.FIVE_G_CORE.PCF: True,
            constants.FIVE_G_CORE.NSSF: True,
            constants.FIVE_G_CORE.BSF: True,
            constants.FIVE_G_CORE.UDR: True,
            constants.FIVE_G_CORE.WEBUI: True
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=True, mme_running=True, sgwc_running=True, smf_running=True, amf_running=False,
            sgwu_running=True, upf_running=True, hss_running=True, pcrf_running=True, nrf_running=True,
            scp_running=True, sepp_running=True, ausf_running=False, udm_running=True, pcf_running=True,
            nssf_running=True, bsf_running=True, udr_running=True, webui_running=True, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response_2: FiveGCoreStatusDTO = csle_collector.five_g_core_manager.query_five_g_core_manager.stop_five_g_core(
            stub=grpc_stub)
        assert response_2.mongo_running == mock_status.mongo_running
        assert response_2.mme_running == mock_status.mme_running
        assert response_2.sgwc_running == mock_status.sgwc_running
        assert response_2.smf_running == mock_status.smf_running
        assert response_2.amf_running == mock_status.amf_running
        assert response_2.sgwu_running == mock_status.sgwu_running
        assert response_2.upf_running == mock_status.upf_running
        assert response_2.hss_running == mock_status.hss_running
        assert response_2.pcrf_running == mock_status.pcrf_running
        assert response_2.nrf_running == mock_status.nrf_running
        assert response_2.scp_running == mock_status.scp_running
        assert response_2.sepp_running == mock_status.sepp_running
        assert response_2.ausf_running == mock_status.ausf_running
        assert response_2.udm_running == mock_status.udm_running
        assert response_2.pcf_running == mock_status.pcf_running
        assert response_2.nssf_running == mock_status.nssf_running
        assert response_2.bsf_running == mock_status.bsf_running
        assert response_2.udr_running == mock_status.udr_running
        assert response_2.webui_running == mock_status.webui_running
        assert response_2.ip == mock_status.ip

    def test_getFiveGCUStatus(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the getFiveGCUStatus grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: False,
            constants.FIVE_G_CORE.MME: False,
            constants.FIVE_G_CORE.SGWC: False,
            constants.FIVE_G_CORE.SMF: False,
            constants.FIVE_G_CORE.AMF: False,
            constants.FIVE_G_CORE.SGWU: False,
            constants.FIVE_G_CORE.UPF: False,
            constants.FIVE_G_CORE.HSS: False,
            constants.FIVE_G_CORE.PCRF: False,
            constants.FIVE_G_CORE.NRF: False,
            constants.FIVE_G_CORE.SCP: False,
            constants.FIVE_G_CORE.SEPP: False,
            constants.FIVE_G_CORE.AUSF: False,
            constants.FIVE_G_CORE.UDM: False,
            constants.FIVE_G_CORE.PCF: False,
            constants.FIVE_G_CORE.NSSF: False,
            constants.FIVE_G_CORE.BSF: False,
            constants.FIVE_G_CORE.UDR: False,
            constants.FIVE_G_CORE.WEBUI: False
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=False, mme_running=False, sgwc_running=False, smf_running=False, amf_running=False,
            sgwu_running=False, upf_running=False, hss_running=False, pcrf_running=False, nrf_running=False,
            scp_running=False, sepp_running=False, ausf_running=False, udm_running=False, pcf_running=False,
            nssf_running=False, bsf_running=False, udr_running=False, webui_running=False, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response: FiveGCoreStatusDTO = (csle_collector.five_g_core_manager.query_five_g_core_manager.
                                        get_five_g_core_status(stub=grpc_stub))
        assert response.mongo_running == mock_status.mongo_running
        assert response.mme_running == mock_status.mme_running
        assert response.sgwc_running == mock_status.sgwc_running
        assert response.smf_running == mock_status.smf_running
        assert response.amf_running == mock_status.amf_running
        assert response.sgwu_running == mock_status.sgwu_running
        assert response.upf_running == mock_status.upf_running
        assert response.hss_running == mock_status.hss_running
        assert response.pcrf_running == mock_status.pcrf_running
        assert response.nrf_running == mock_status.nrf_running
        assert response.scp_running == mock_status.scp_running
        assert response.sepp_running == mock_status.sepp_running
        assert response.ausf_running == mock_status.ausf_running
        assert response.udm_running == mock_status.udm_running
        assert response.pcf_running == mock_status.pcf_running
        assert response.nssf_running == mock_status.nssf_running
        assert response.bsf_running == mock_status.bsf_running
        assert response.udr_running == mock_status.udr_running
        assert response.webui_running == mock_status.webui_running
        assert response.ip == mock_status.ip

        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: True,
            constants.FIVE_G_CORE.MME: True,
            constants.FIVE_G_CORE.SGWC: True,
            constants.FIVE_G_CORE.SMF: True,
            constants.FIVE_G_CORE.AMF: False,
            constants.FIVE_G_CORE.SGWU: True,
            constants.FIVE_G_CORE.UPF: True,
            constants.FIVE_G_CORE.HSS: True,
            constants.FIVE_G_CORE.PCRF: True,
            constants.FIVE_G_CORE.NRF: True,
            constants.FIVE_G_CORE.SCP: True,
            constants.FIVE_G_CORE.SEPP: True,
            constants.FIVE_G_CORE.AUSF: False,
            constants.FIVE_G_CORE.UDM: True,
            constants.FIVE_G_CORE.PCF: True,
            constants.FIVE_G_CORE.NSSF: True,
            constants.FIVE_G_CORE.BSF: True,
            constants.FIVE_G_CORE.UDR: True,
            constants.FIVE_G_CORE.WEBUI: True
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=True, mme_running=True, sgwc_running=True, smf_running=True, amf_running=False,
            sgwu_running=True, upf_running=True, hss_running=True, pcrf_running=True, nrf_running=True,
            scp_running=True, sepp_running=True, ausf_running=False, udm_running=True, pcf_running=True,
            nssf_running=True, bsf_running=True, udr_running=True, webui_running=True, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response_2: FiveGCoreStatusDTO = (csle_collector.five_g_core_manager.query_five_g_core_manager.
                                          get_five_g_core_status(stub=grpc_stub))
        assert response_2.mongo_running == mock_status.mongo_running
        assert response_2.mme_running == mock_status.mme_running
        assert response_2.sgwc_running == mock_status.sgwc_running
        assert response_2.smf_running == mock_status.smf_running
        assert response_2.amf_running == mock_status.amf_running
        assert response_2.sgwu_running == mock_status.sgwu_running
        assert response_2.upf_running == mock_status.upf_running
        assert response_2.hss_running == mock_status.hss_running
        assert response_2.pcrf_running == mock_status.pcrf_running
        assert response_2.nrf_running == mock_status.nrf_running
        assert response_2.scp_running == mock_status.scp_running
        assert response_2.sepp_running == mock_status.sepp_running
        assert response_2.ausf_running == mock_status.ausf_running
        assert response_2.udm_running == mock_status.udm_running
        assert response_2.pcf_running == mock_status.pcf_running
        assert response_2.nssf_running == mock_status.nssf_running
        assert response_2.bsf_running == mock_status.bsf_running
        assert response_2.udr_running == mock_status.udr_running
        assert response_2.webui_running == mock_status.webui_running
        assert response_2.ip == mock_status.ip

    def test_initFiveGCore(self, grpc_stub, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the initFiveGCore grpc

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :return: None
        """
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'init_all_core_services', return_value=None)
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'init_subscriber_data', return_value=None)
        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: False,
            constants.FIVE_G_CORE.MME: False,
            constants.FIVE_G_CORE.SGWC: False,
            constants.FIVE_G_CORE.SMF: False,
            constants.FIVE_G_CORE.AMF: False,
            constants.FIVE_G_CORE.SGWU: False,
            constants.FIVE_G_CORE.UPF: False,
            constants.FIVE_G_CORE.HSS: False,
            constants.FIVE_G_CORE.PCRF: False,
            constants.FIVE_G_CORE.NRF: False,
            constants.FIVE_G_CORE.SCP: False,
            constants.FIVE_G_CORE.SEPP: False,
            constants.FIVE_G_CORE.AUSF: False,
            constants.FIVE_G_CORE.UDM: False,
            constants.FIVE_G_CORE.PCF: False,
            constants.FIVE_G_CORE.NSSF: False,
            constants.FIVE_G_CORE.BSF: False,
            constants.FIVE_G_CORE.UDR: False,
            constants.FIVE_G_CORE.WEBUI: False
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=False, mme_running=False, sgwc_running=False, smf_running=False, amf_running=False,
            sgwu_running=False, upf_running=False, hss_running=False, pcrf_running=False, nrf_running=False,
            scp_running=False, sepp_running=False, ausf_running=False, udm_running=False, pcf_running=False,
            nssf_running=False, bsf_running=False, udr_running=False, webui_running=False, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response: FiveGCoreStatusDTO = csle_collector.five_g_core_manager.query_five_g_core_manager.init_five_g_core(
            stub=grpc_stub)
        assert response.mongo_running == mock_status.mongo_running
        assert response.mme_running == mock_status.mme_running
        assert response.sgwc_running == mock_status.sgwc_running
        assert response.smf_running == mock_status.smf_running
        assert response.amf_running == mock_status.amf_running
        assert response.sgwu_running == mock_status.sgwu_running
        assert response.upf_running == mock_status.upf_running
        assert response.hss_running == mock_status.hss_running
        assert response.pcrf_running == mock_status.pcrf_running
        assert response.nrf_running == mock_status.nrf_running
        assert response.scp_running == mock_status.scp_running
        assert response.sepp_running == mock_status.sepp_running
        assert response.ausf_running == mock_status.ausf_running
        assert response.udm_running == mock_status.udm_running
        assert response.pcf_running == mock_status.pcf_running
        assert response.nssf_running == mock_status.nssf_running
        assert response.bsf_running == mock_status.bsf_running
        assert response.udr_running == mock_status.udr_running
        assert response.webui_running == mock_status.webui_running
        assert response.ip == mock_status.ip

        mock_status_dict = {
            constants.FIVE_G_CORE.MONGO: True,
            constants.FIVE_G_CORE.MME: True,
            constants.FIVE_G_CORE.SGWC: True,
            constants.FIVE_G_CORE.SMF: True,
            constants.FIVE_G_CORE.AMF: False,
            constants.FIVE_G_CORE.SGWU: True,
            constants.FIVE_G_CORE.UPF: True,
            constants.FIVE_G_CORE.HSS: True,
            constants.FIVE_G_CORE.PCRF: True,
            constants.FIVE_G_CORE.NRF: True,
            constants.FIVE_G_CORE.SCP: True,
            constants.FIVE_G_CORE.SEPP: True,
            constants.FIVE_G_CORE.AUSF: False,
            constants.FIVE_G_CORE.UDM: True,
            constants.FIVE_G_CORE.PCF: True,
            constants.FIVE_G_CORE.NSSF: True,
            constants.FIVE_G_CORE.BSF: True,
            constants.FIVE_G_CORE.UDR: True,
            constants.FIVE_G_CORE.WEBUI: True
        }
        mock_status = FiveGCoreStatusDTO(
            mongo_running=True, mme_running=True, sgwc_running=True, smf_running=True, amf_running=False,
            sgwu_running=True, upf_running=True, hss_running=True, pcrf_running=True, nrf_running=True,
            scp_running=True, sepp_running=True, ausf_running=False, udm_running=True, pcf_running=True,
            nssf_running=True, bsf_running=True, udr_running=True, webui_running=True, ip="0.0.0.0")
        mocker.patch('csle_collector.five_g_core_manager.five_g_core_manager_util.FiveGCoreManagerUtil.'
                     'get_core_status', return_value=mock_status_dict)
        response_2: FiveGCoreStatusDTO = csle_collector.five_g_core_manager.query_five_g_core_manager.init_five_g_core(
            stub=grpc_stub)
        assert response_2.mongo_running == mock_status.mongo_running
        assert response_2.mme_running == mock_status.mme_running
        assert response_2.sgwc_running == mock_status.sgwc_running
        assert response_2.smf_running == mock_status.smf_running
        assert response_2.amf_running == mock_status.amf_running
        assert response_2.sgwu_running == mock_status.sgwu_running
        assert response_2.upf_running == mock_status.upf_running
        assert response_2.hss_running == mock_status.hss_running
        assert response_2.pcrf_running == mock_status.pcrf_running
        assert response_2.nrf_running == mock_status.nrf_running
        assert response_2.scp_running == mock_status.scp_running
        assert response_2.sepp_running == mock_status.sepp_running
        assert response_2.ausf_running == mock_status.ausf_running
        assert response_2.udm_running == mock_status.udm_running
        assert response_2.pcf_running == mock_status.pcf_running
        assert response_2.nssf_running == mock_status.nssf_running
        assert response_2.bsf_running == mock_status.bsf_running
        assert response_2.udr_running == mock_status.udr_running
        assert response_2.webui_running == mock_status.webui_running
        assert response_2.ip == mock_status.ip
