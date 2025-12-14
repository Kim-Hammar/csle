import logging
from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.constants.constants as csle_collector_constants
import csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc
import csle_collector.five_g_core_manager.five_g_core_manager_pb2
import csle_collector.five_g_core_manager.query_five_g_core_manager
from csle_common.util.emulation_util import EmulationUtil


class FiveGCoreController:
    """
    Class controlling 5G cores running on nodes in the emulations, as well as 5G core managers
    """

    @staticmethod
    def start_five_g_core_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                   logger: logging.Logger) -> None:
        """
        Utility method for starting 5G core managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    FiveGCoreController.start_five_g_core_manager(emulation_env_config=emulation_env_config,
                                                                  ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_five_g_core_manager(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        Utility method for starting the 5G core manager on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Check if the manager is already running
        status = None
        not_running = False
        try:
            status = FiveGCoreController.get_five_g_core_status_by_ip_and_port(
                ip=ip, port=emulation_env_config.five_g_config.five_g_core_manager_port, timeout=5)
        except Exception:
            not_running = True
        status_str = ""
        if status is None:
            not_running = True
        else:
            status_str = (f"mongo_running: {status.mongo_running}, mme_running: {status.mme_running}, "
                          f"sgwc_running: {status.sgwc_running}, smf_running: {status.smf_running}, "
                          f"amf_running: {status.amf_running}, sgwu_running: {status.sgwu_running}, "
                          f"upf_running: {status.upf_running}, hss_running: {status.hss_running}, "
                          f"pcrf_running: {status.pcrf_running}, nrf_running: {status.nrf_running}, "
                          f"scp_running: {status.scp_running}, sepp_running: {status.sepp_running}, "
                          f"ausf_running: {status.ausf_running}, udm_running: {status.udm_running}, "
                          f"pcf_running: {status.pcf_running}, nssf_running: {status.nssf_running}, "
                          f"bsf_running: {status.bsf_running}, udr_running: {status.udr_running}, "
                          f"webui_running: {status.webui_running}, ip: {status.ip}")
        if not_running:
            logger.info(f"Starting 5G core manager on node {ip}")

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.FIVE_G_CORE_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

            # Start the 5G core manager
            cmd = constants.COMMANDS.START_FIVE_G_CORE_MANAGER.format(
                emulation_env_config.five_g_config.five_g_core_manager_port,
                emulation_env_config.five_g_config.five_g_core_manager_log_dir,
                emulation_env_config.five_g_config.five_g_core_manager_log_file,
                emulation_env_config.five_g_config.five_g_core_manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)
        else:
            logger.info(f"5G core manager was already running on node {ip}. Status: {status_str}")

    @staticmethod
    def stop_five_g_core_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                  logger: logging.Logger) -> None:
        """
        Utility method for stopping 5G core managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the IP of the physical host
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    FiveGCoreController.stop_five_g_core_manager(emulation_env_config=emulation_env_config,
                                                                 ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_five_g_core_manager(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        Utility method for stopping a 5G core manager with a speicific IP

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

        logger.info(f"Stopping 5G Core manager on node {ip}")

        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.FIVE_G_CORE_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
        time.sleep(2)

    @staticmethod
    def get_five_g_core_manager_statuses(
            emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) \
            -> List[csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO]:
        """
        A method that sends a request to the 5G core manager on every container to get the status of the
        5G core

        :param emulation_env_config: the emulation config
        :param physical_server_ip: the IP of the physical server
        :param logger: the logger to use for logging
        :return: List of monitor thread statuses
        """
        statuses = []
        FiveGCoreController.start_five_g_core_managers(emulation_env_config=emulation_env_config,
                                                       physical_server_ip=physical_server_ip, logger=logger)

        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    status = FiveGCoreController.get_five_g_core_status_by_ip_and_port(
                        port=emulation_env_config.five_g_config.five_g_core_manager_port,
                        ip=c.docker_gw_bridge_ip)
                    statuses.append(status)
        return statuses

    @staticmethod
    def get_five_g_core_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPs of the 5G core managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    ips.append(c.docker_gw_bridge_ip)
        return ips

    @staticmethod
    def get_five_g_core_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the FiveGCoreManagers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    ports.append(emulation_env_config.five_g_config.five_g_core_manager_port)
        return ports

    @staticmethod
    def get_five_g_core_status_by_ip_and_port(
            port: int, ip: str, timeout: int = csle_collector_constants.GRPC.TIMEOUT_SECONDS) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        A method that sends a request to the 5G core manager with a specific port and ip
        to get the status of the 5G core

        :param port: the port of the FiveGCoreManager
        :param ip: the ip of the FiveGCoreManager
        :param timeout: the timeout of the GRPC query
        :return: the status of the FiveGCoreManager
        """
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
            status = \
                csle_collector.five_g_core_manager.query_five_g_core_manager.get_five_g_core_status(
                    stub=stub, timeout=timeout)
            return status

    @staticmethod
    def start_five_g_cores(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                           logger: logging.Logger) -> None:
        """
        Utility method for starting the 5G cores of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    FiveGCoreController.start_five_g_core(emulation_env_config=emulation_env_config,
                                                          ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_five_g_core(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Utility method for starting the 5G core on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Starting the 5G core on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_core_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
            status = csle_collector.five_g_core_manager.query_five_g_core_manager.start_five_g_core(stub=stub)
            return status

    @staticmethod
    def stop_five_g_cores(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                          logger: logging.Logger) -> None:
        """
        Utility method for stopping the 5G cores of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    FiveGCoreController.stop_five_g_core(emulation_env_config=emulation_env_config,
                                                         ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_five_g_core(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Utility method for stopping the 5G core on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Stopping the 5G core on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_core_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
            status = csle_collector.five_g_core_manager.query_five_g_core_manager.stop_five_g_core(stub=stub)
            return status

    @staticmethod
    def init_five_g_cores(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                          logger: logging.Logger) -> None:
        """
        Utility method for initializing the 5G cores of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CORE_IMAGES:
                if ids_image in c.name:
                    FiveGCoreController.init_five_g_core(emulation_env_config=emulation_env_config,
                                                         ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def init_five_g_core(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Utility method for initializing the 5G core on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(
            f"Iniitalizing the 5G core on container with ip {ip} in execution {emulation_env_config.execution_id} "
            f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_core_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
            status = csle_collector.five_g_core_manager.query_five_g_core_manager.init_five_g_core(stub=stub)
            return status
