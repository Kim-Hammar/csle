from unittest.mock import patch, MagicMock
import csle_common.constants.constants as constants
from csle_common.controllers.five_g_du_controller import FiveGDUController
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import pytest


class TestFiveGDUControllerSuite:
    """
    Test five_g_du_controller
    """

    @pytest.fixture(autouse=True)
    def logger_setup(self) -> None:
        """
        Set up logger

        :return: None
        """
        self.logger = MagicMock()

    @patch("csle_common.controllers.five_g_du_controller.FiveGDUController.start_five_g_du")
    def test_start_five_g_dus(self, mock_start_five_g_du, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G DUs

        :param mock_start_five_g_du: mock_start_five_g_du
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES = \
            [example_emulation_env_config.containers_config.containers[0].name]
        FiveGDUController.start_five_g_dus(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_start_five_g_du.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_common.controllers.five_g_du_controller.FiveGDUController.stop_five_g_du")
    def test_stop_five_g_dus(self, mock_stop_five_g_du, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G DUs

        :param mock_stop_five_g_du: mock_stop_five_g_du
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES = \
            [example_emulation_env_config.containers_config.containers[0].name]
        FiveGDUController.stop_five_g_dus(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_stop_five_g_du.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du")
    @patch("grpc.insecure_channel")
    def test_start_five_g_du(self, mock_insecure_channel, mock_start_five_g_du,
                             example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G DU on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_five_g_du: mock_start_five_g_du
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        FiveGDUController.start_five_g_du(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Starting the 5G DU on container with ip "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} in "
            f"execution {example_emulation_env_config.execution_id} "
            f"of emulation: {example_emulation_env_config.name}")
        mock_insecure_channel.assert_called()
        mock_start_five_g_du.assert_called()

    @patch("csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du")
    @patch("grpc.insecure_channel")
    def test_stop_five_g_du(self, mock_insecure_channel, mock_stop_five_g_du,
                            example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G DU on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_stop_five_g_du: mock_stop_five_g_du
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        FiveGDUController.stop_five_g_du(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Stopping the 5G DU on container with ip "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} in "
            f"execution {example_emulation_env_config.execution_id} "
            f"of emulation: {example_emulation_env_config.name}")
        mock_insecure_channel.assert_called()
        mock_stop_five_g_du.assert_called()

    @patch("csle_common.controllers.five_g_du_controller.FiveGDUController.start_five_g_du_manager")
    def test_start_five_g_du_managers(self, start_five_g_du_manager,
                                      example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting 5G DU managers

        :param start_five_g_du_manager: start_five_g_du_manager
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        FiveGDUController.start_five_g_du_managers(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        start_five_g_du_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_start_five_g_du_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin,
                                     example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G Du manager on a specific IP

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param example_emulation_env_config: example_emulation_env_config
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_connection = MagicMock()
        example_emulation_env_config.get_connection = MagicMock()  # type: ignore[method-assign]
        example_emulation_env_config.get_connection.return_value = mock_connection
        mock_execute_ssh_cmd.side_effect = [
            (b"", b"", 0),  # Output for stopping old background job
            (b"", b"", 0),  # Output for starting the five_g_du_manager
        ]
        FiveGDUController.start_five_g_du_manager(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_any_call(
            f"Starting 5G DU manager on node "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}")

    @patch("csle_common.controllers.five_g_du_controller.FiveGDUController.stop_five_g_du_manager")
    def test_stop_five_g_du_managers(self, stop_five_g_du_manager,
                                     example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping 5G DU managers

        :param stop_five_g_du_manager: stop_five_g_du_manager
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        FiveGDUController.stop_five_g_du_managers(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        stop_five_g_du_manager.assert_called()

    @patch("csle_common.util.emulation_util.EmulationUtil.connect_admin")
    @patch("csle_common.util.emulation_util.EmulationUtil.execute_ssh_cmd")
    @patch("time.sleep", return_value=None)
    def test_stop_five_g_du_manager(self, mock_sleep, mock_execute_ssh_cmd, mock_connect_admin,
                                    example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G DU manager on a specific IP

        :param mock_execute_ssh_cmd: mock_execute_ssh_cmd
        :param mock_connect_admin: mock_connect_admin
        :param example_emulation_env_config: example_emulation_env_config
        :param mock_sleep: mock_sleep
        :return: None
        """
        mock_connection = MagicMock()
        example_emulation_env_config.get_connection = MagicMock()  # type: ignore[method-assign]
        example_emulation_env_config.get_connection.return_value = mock_connection
        mock_execute_ssh_cmd.side_effect = [(b"", b"", 0)]
        FiveGDUController.stop_five_g_du_manager(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip, logger=self.logger)
        mock_connect_admin.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip)
        mock_execute_ssh_cmd.assert_called()
        self.logger.info.assert_any_call(
            f"Stopping 5G DU manager on node "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip}")

    def test_get_five_g_du_managers_ips(self, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test a method that extracts the IPs of the 5G DU managers in a given emulation

        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        ips = FiveGDUController.get_five_g_du_managers_ips(emulation_env_config=example_emulation_env_config)
        expected_ips = [example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip]
        assert ips == expected_ips

    def test_get_five_g_du_managers_ports(self, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test a method that extracts the ports of the 5G Du managers in a given emulation

        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        ports = FiveGDUController.get_five_g_du_managers_ports(emulation_env_config=example_emulation_env_config)
        expected_ports = [50054]
        assert ports == expected_ports

    @patch("csle_common.controllers.five_g_du_controller.FiveGDUController.stop_five_g_ue")
    def test_stop_five_g_ues(self, mock_stop_five_g_ue, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G UEs

        :param mock_stop_five_g_ue: mock_stop_five_g_ue
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES = \
            [example_emulation_env_config.containers_config.containers[0].name]
        FiveGDUController.stop_five_g_ues(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_stop_five_g_ue.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_ue")
    @patch("grpc.insecure_channel")
    def test_stop_five_g_ue(self, mock_insecure_channel, mock_stop_five_g_ue,
                            example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for stopping the 5G UE on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_stop_five_g_ue: mock_stop_five_g_ue
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        FiveGDUController.stop_five_g_ue(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Stopping the 5G UE on container with ip "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} in "
            f"execution {example_emulation_env_config.execution_id} "
            f"of emulation: {example_emulation_env_config.name}")
        mock_insecure_channel.assert_called()
        mock_stop_five_g_ue.assert_called()

    @patch("csle_common.controllers.five_g_du_controller.FiveGDUController.start_five_g_ue")
    def test_start_five_g_ues(self, mock_start_five_g_ue, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G UEs

        :param mock_start_five_g_ue: mock_start_five_g_ue
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES = \
            [example_emulation_env_config.containers_config.containers[0].name]
        FiveGDUController.start_five_g_ues(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_start_five_g_ue.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_ue")
    @patch("grpc.insecure_channel")
    def test_start_five_g_ue(self, mock_insecure_channel, mock_start_five_g_ue,
                             example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for starting the 5G UE on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_start_five_g_ue: mock_start_five_g_ue
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        FiveGDUController.start_five_g_ue(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Starting the 5G UE on container with ip "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} in "
            f"execution {example_emulation_env_config.execution_id} "
            f"of emulation: {example_emulation_env_config.name}")
        mock_insecure_channel.assert_called()
        mock_start_five_g_ue.assert_called()

    @patch("csle_common.controllers.five_g_du_controller.FiveGDUController.init_five_g_ue")
    def test_init_five_g_ues(self, mock_init_five_g_ue, example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for initializing the 5G UEs

        :param mock_init_five_g_ue: mock_init_five_g_ue
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES = \
            [example_emulation_env_config.containers_config.containers[0].name]
        FiveGDUController.init_five_g_ues(
            emulation_env_config=example_emulation_env_config,
            physical_server_ip=example_emulation_env_config.containers_config.containers[0].physical_host_ip,
            logger=self.logger)
        mock_init_five_g_ue.assert_called_once_with(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)

    @patch("csle_collector.five_g_du_manager.query_five_g_du_manager.init_five_g_ue")
    @patch("grpc.insecure_channel")
    def test_init_five_g_ue(self, mock_insecure_channel, mock_init_five_g_ue,
                            example_emulation_env_config: EmulationEnvConfig) -> None:
        """
        Test utility function for initializing the 5G UE on a specific IP

        :param mock_insecure_channel: mock_insecure_channel
        :param mock_init_five_g_ue: mock_init_five_g_ue
        :param example_emulation_env_config: example_emulation_env_config
        :return: None
        """
        constants.GRPC_SERVERS.GRPC_OPTIONS = []
        mock_channel = MagicMock()
        mock_insecure_channel.return_value = mock_channel
        mock_stub = MagicMock()
        mock_channel.__enter__.return_value = mock_stub
        FiveGDUController.init_five_g_ue(
            emulation_env_config=example_emulation_env_config,
            ip=example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip,
            logger=self.logger)
        self.logger.info.assert_called_once_with(
            f"Initializing the 5G UE on container with ip "
            f"{example_emulation_env_config.containers_config.containers[0].docker_gw_bridge_ip} in "
            f"execution {example_emulation_env_config.execution_id} "
            f"of emulation: {example_emulation_env_config.name}")
        mock_insecure_channel.assert_called()
        mock_init_five_g_ue.assert_called()
