from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.controllers.five_g_core_controller import FiveGCoreController
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import pytest


class TestFiveGCoreControllerSuite:
    """
    Test five_g_core_controller
    """

    @pytest.fixture(autouse=True)
    def logger_setup(self) -> None:
        """
        Set up logger

        :return: None
        """
        self.logger = MagicMock()

    @patch("csle_common.controllers.five_g_core_controller.FiveGCoreController.start_five_g_core")
    def test_start_five_g_cores(self, mock_start_five_g_core, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G cores

        :param mock_start_five_g_core: mock_start_five_g_core
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES = \
            [example_emulation_env_config.containers_config.containers[0].name]
        FiveGCoreController.start_five_g_cores(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_start_five_g_core.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_common.controllers.five_g_core_controller.FiveGCoreController.stop_five_g_core")
    def test_stop_five_g_cores(self, mock_stop_five_g_core, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G cores

        :param mock_stop_five_g_core: mock_stop_five_g_core
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES = \
            [example_emulation_env_config.containers_config.containers[0].name]
        FiveGCoreController.stop_five_g_cores(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_stop_five_g_core.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_collector.five_g_core_manager.query_five_g_core_manager.start_five_g_core")
    @patch("grpc.insecure_channel")
    def test_start_five_g_core(self, mock_insecure_channel, mock_start_five_g_core,
                               example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G core on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_five_g_core: mock_start_five_g_core
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        FiveGCoreController.start_five_g_core(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Starting the 5G core on container with ip "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} in "
            f"execution {example_emulation_env_config.execution_id} "
            f"of emulation: {example_emulation_env_config.name}")
        mock_insecure_channel.assert_called()
        mock_start_five_g_core.assert_called()

    @patch("csle_collector.five_g_core_manager.query_five_g_core_manager.stop_five_g_core")
    @patch("grpc.insecure_channel")
    def test_stop_five_g_core(self, mock_insecure_channel, mock_stop_five_g_core,
                              example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G core on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_stop_five_g_core: mock_stop_five_g_core
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        FiveGCoreController.stop_five_g_core(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Stopping the 5G core on container with ip "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} in "
            f"execution {example_emulation_env_config.execution_id} "
            f"of emulation: {example_emulation_env_config.name}")
        mock_insecure_channel.assert_called()
        mock_stop_five_g_core.assert_called()

    @patch("csle_common.controllers.five_g_core_controller.FiveGCoreController.start_five_g_core_manager")
    def test_start_five_g_core_managers(self, start_five_g_core_manager,
                                        example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting 5G core managers

        :param start_five_g_core_manager: start_five_g_core_manager
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        FiveGCoreController.start_five_g_core_managers(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        start_five_g_core_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_five_g_core_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin,
                                       example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G core manager on a specific IP

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param example_emulation_env_config: example_emulation_env_config
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_connection = MagicMock()
        example_emulation_env_config.get_connection = MagicMock() # type: ignore[method-assign]
        example_emulation_env_config.get_connection.return_value = mock_connection
        mock_execute_ssh_cmd.side_effect = [
            (b"", b"", 0),  # Output for stopping old background job
            (b"", b"", 0),  # Output for starting the five_g_core_manager
        ]
        FiveGCoreController.start_five_g_core_manager(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_any_call(
            f"Starting 5G core manager on node "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}")

    @patch("csle_common.controllers.five_g_core_controller.FiveGCoreController.stop_five_g_core_manager")
    def test_stop_five_g_core_managers(self, stop_five_g_core_manager,
                                       example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping 5G core managers

        :param stop_five_g_core_manager: stop_five_g_core_manager
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        FiveGCoreController.stop_five_g_core_managers(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        stop_five_g_core_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_stop_five_g_core_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin,
                                      example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G core manager on a specific IP

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param example_emulation_env_config: example_emulation_env_config
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_connection = MagicMock()
        example_emulation_env_config.get_connection = MagicMock() # type: ignore[method-assign]
        example_emulation_env_config.get_connection.return_value = mock_connection
        mock_execute_ssh_cmd.side_effect = [(b"", b"", 0)]
        FiveGCoreController.stop_five_g_core_manager(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_any_call(
            f"Stopping 5G Core manager on node "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}")

    def test_get_five_g_core_managers_ips(self, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test a method that extracts the IPs of the 5G core managers in a given emulation

        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        ips = FiveGCoreController.get_five_g_core_managers_ips(emulation_env_config=example_emulation_env_config)
        expected_ips = [example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip]
        assert ips == expected_ips

    def test_get_five_g_core_managers_ports(self, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test a method that extracts the ports of the 5G core managers in a given emulation

        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        ports = FiveGCoreController.get_five_g_core_managers_ports(emulation_env_config=example_emulation_env_config)
        expected_ports = [50052]
        assert ports == expected_ports
