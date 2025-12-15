import logging
from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.constants.constants as csle_collector_constants
import csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc
import csle_collector.five_g_du_manager.five_g_du_manager_pb2
import csle_collector.five_g_du_manager.query_five_g_du_manager
from csle_common.util.emulation_util import EmulationUtil


class FiveGDUController:
    """
    Class controlling 5G dus running on nodes in the emulations, as well as 5G DU managers
    """

    @staticmethod
    def start_five_g_du_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                 logger: logging.Logger) -> None:
        """
        Utility method for starting 5G DU managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    FiveGDUController.start_five_g_du_manager(emulation_env_config=emulation_env_config,
                                                              ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_five_g_du_manager(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        Utility method for starting the 5G DU manager on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Check if the manager is already running
        status = None
        not_running = False
        try:
            status = FiveGDUController.get_five_g_du_status_by_ip_and_port(
                ip=ip, port=emulation_env_config.five_g_config.five_g_du_manager_port, timeout=5)
        except Exception:
            not_running = True
        status_str = ""
        if status is None:
            not_running = True
        else:
            status_str = f"du_running: {status.du_running}, ip: {status.ip}"
        if not_running:
            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.FIVE_G_DU_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

            logger.info(f"Starting 5G DU manager on node {ip}")

            # Start the 5G DU manager
            cmd = constants.COMMANDS.START_FIVE_G_DU_MANAGER.format(
                emulation_env_config.five_g_config.five_g_du_manager_port,
                emulation_env_config.five_g_config.five_g_du_manager_log_dir,
                emulation_env_config.five_g_config.five_g_du_manager_log_file,
                emulation_env_config.five_g_config.five_g_du_manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)
        else:
            logger.info(f"5G du manager was already running on node {ip}. Status: {status_str}")

    @staticmethod
    def stop_five_g_du_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                logger: logging.Logger) -> None:
        """
        Utility method for stopping 5G DU managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the IP of the physical host
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    FiveGDUController.stop_five_g_du_manager(emulation_env_config=emulation_env_config,
                                                             ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_five_g_du_manager(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        Utility method for stopping a 5G DU manager with a specific IP

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

        logger.info(f"Stopping 5G DU manager on node {ip}")

        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.FIVE_G_DU_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
        time.sleep(2)

    @staticmethod
    def get_five_g_du_manager_statuses(
            emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) \
            -> List[csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO]:
        """
        A method that sends a request to the 5G DU manager on every container to get the status of the
        5G du

        :param emulation_env_config: the emulation config
        :param physical_server_ip: the IP of the physical server
        :param logger: the logger to use for logging
        :return: List of monitor thread statuses
        """
        statuses = []
        FiveGDUController.start_five_g_du_managers(emulation_env_config=emulation_env_config,
                                                   physical_server_ip=physical_server_ip, logger=logger)

        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    status = FiveGDUController.get_five_g_du_status_by_ip_and_port(
                        port=emulation_env_config.five_g_config.five_g_du_manager_port,
                        ip=c.docker_gw_bridge_ip)
                    statuses.append(status)
        return statuses

    @staticmethod
    def get_five_g_du_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPs of the 5G DU managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    ips.append(c.docker_gw_bridge_ip)
        return ips

    @staticmethod
    def get_five_g_du_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the FiveGDUManagers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    ports.append(emulation_env_config.five_g_config.five_g_du_manager_port)
        return ports

    @staticmethod
    def get_five_g_du_status_by_ip_and_port(
            port: int, ip: str, timeout: int = csle_collector_constants.GRPC.TIMEOUT_SECONDS) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        A method that sends a request to the 5G DU manager with a specific port and ip
        to get the status of the 5G DU

        :param port: the port of the FiveGDUManager
        :param ip: the ip of the FiveGDUManager
        :param timeout: the timeout of the GRPC query
        :return: the status of the FiveGDUManager
        """
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
            status = \
                csle_collector.five_g_du_manager.query_five_g_du_manager.get_five_g_du_status(
                    stub=stub, timeout=timeout)
            return status

    @staticmethod
    def start_five_g_dus(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                         logger: logging.Logger) -> None:
        """
        Utility method for starting the 5G DUs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    FiveGDUController.start_five_g_du(emulation_env_config=emulation_env_config,
                                                      ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_five_g_du(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Utility method for starting the 5G DU on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Starting the 5G DU on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_du_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
            status = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du(stub=stub)
            return status

    @staticmethod
    def stop_five_g_dus(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                        logger: logging.Logger) -> None:
        """
        Utility method for stopping the 5G DUs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    FiveGDUController.stop_five_g_du(emulation_env_config=emulation_env_config,
                                                     ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_five_g_du(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Utility method for stopping the 5G DU on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Stopping the 5G DU on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_du_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
            status = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du(stub=stub)
            return status

    # UE
    @staticmethod
    def start_five_g_ues(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                         logger: logging.Logger) -> None:
        """
        Utility method for starting the 5G UEs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    FiveGDUController.start_five_g_ue(emulation_env_config=emulation_env_config,
                                                      ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_five_g_ue(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Utility method for starting the 5G UE on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Starting the 5G UE on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_du_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
            status = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_ue(stub=stub)
            return status

    @staticmethod
    def stop_five_g_ues(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                        logger: logging.Logger) -> None:
        """
        Utility method for stopping the 5G UEs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    FiveGDUController.stop_five_g_ue(emulation_env_config=emulation_env_config,
                                                     ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_five_g_ue(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Utility method for stopping the 5G UE on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Stopping the 5G UE on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_du_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
            status = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_ue(stub=stub)
            return status

    @staticmethod
    def init_five_g_ues(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                        logger: logging.Logger) -> None:
        """
        Utility method for initializing the 5G UEs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_DU_IMAGES:
                if ids_image in c.name:
                    FiveGDUController.init_five_g_ue(emulation_env_config=emulation_env_config,
                                                     ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def init_five_g_ue(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Utility method for initializing the 5G UE on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(
            f"Initializing the 5G UE on container with ip {ip} in execution {emulation_env_config.execution_id} "
            f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_du_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
            status = csle_collector.five_g_du_manager.query_five_g_du_manager.init_five_g_ue(stub=stub)
            return status
