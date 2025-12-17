import logging
from typing import List
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.five_g_cu_managers_info import FiveGCUManagersInfo
import csle_common.constants.constants as constants
import csle_collector.constants.constants as csle_collector_constants
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2
import csle_collector.five_g_cu_manager.five_g_cu_manager_util
import csle_collector.five_g_cu_manager.query_five_g_cu_manager
from csle_common.util.emulation_util import EmulationUtil


class FiveGCUController:
    """
    Class controlling 5G cus running on nodes in the emulations, as well as 5G CU managers
    """

    @staticmethod
    def start_five_g_cu_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                 logger: logging.Logger) -> None:
        """
        Utility method for starting 5G CU managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    FiveGCUController.start_five_g_cu_manager(emulation_env_config=emulation_env_config,
                                                              ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_five_g_cu_manager(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        Utility method for starting the 5G CU manager on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Check if the manager is already running
        status = None
        not_running = False
        try:
            status = FiveGCUController.get_five_g_cu_status_by_ip_and_port(
                ip=ip, port=emulation_env_config.five_g_config.five_g_cu_manager_port, timeout=5)
        except Exception:
            not_running = True
        status_str = ""
        if status is None:
            not_running = True
        else:
            status_str = f"cu_running: {status.cu_running}, ip: {status.ip}"
        if not_running:
            logger.info(f"Starting 5G CU manager on node {ip}")

            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

            # Stop old background job if running
            cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
                   constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.FIVE_G_CU_MANAGER_FILE_NAME)
            o, e, _ = EmulationUtil.execute_ssh_cmd(
                cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))

            # Start the 5G cu manager
            cmd = constants.COMMANDS.START_FIVE_G_CU_MANAGER.format(
                emulation_env_config.five_g_config.five_g_cu_manager_port,
                emulation_env_config.five_g_config.five_g_cu_manager_log_dir,
                emulation_env_config.five_g_config.five_g_cu_manager_log_file,
                emulation_env_config.five_g_config.five_g_cu_manager_max_workers)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
            time.sleep(2)
        else:
            logger.info(f"5G CU manager was already running on node {ip}. Status: {status_str}")

    @staticmethod
    def stop_five_g_cu_managers(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                                logger: logging.Logger) -> None:
        """
        Utility method for stopping 5G CU managers

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the IP of the physical host
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    FiveGCUController.stop_five_g_cu_manager(emulation_env_config=emulation_env_config,
                                                             ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_five_g_cu_manager(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) -> None:
        """
        Utility method for stopping a 5G CU manager with a specific IP

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        # Connect
        EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=ip)

        logger.info(f"Stopping 5G CU manager on node {ip}")

        cmd = (constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL +
               constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.FIVE_G_CU_MANAGER_FILE_NAME)
        o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=ip))
        time.sleep(2)

    @staticmethod
    def get_five_g_cu_manager_statuses(
            emulation_env_config: EmulationEnvConfig, physical_server_ip: str, logger: logging.Logger) \
            -> List[csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO]:
        """
        A method that sends a request to the 5G CU manager on every container to get the status of the
        5G CU

        :param emulation_env_config: the emulation config
        :param physical_server_ip: the IP of the physical server
        :param logger: the logger to use for logging
        :return: List of monitor thread statuses
        """
        statuses = []
        FiveGCUController.start_five_g_cu_managers(emulation_env_config=emulation_env_config,
                                                   physical_server_ip=physical_server_ip, logger=logger)

        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    status = FiveGCUController.get_five_g_cu_status_by_ip_and_port(
                        port=emulation_env_config.five_g_config.five_g_cu_manager_port,
                        ip=c.docker_gw_bridge_ip)
                    statuses.append(status)
        return statuses

    @staticmethod
    def get_five_g_cu_managers_ips(emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        A method that extracts the IPs of the 5G CU managers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of IP addresses
        """
        ips = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    ips.append(c.docker_gw_bridge_ip)
        return ips

    @staticmethod
    def get_five_g_cu_managers_ports(emulation_env_config: EmulationEnvConfig) -> List[int]:
        """
        A method that extracts the ports of the FiveGCUManagers in a given emulation

        :param emulation_env_config: the emulation env config
        :return: the list of ports
        """
        ports = []
        for c in emulation_env_config.containers_config.containers:
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    ports.append(emulation_env_config.five_g_config.five_g_cu_manager_port)
        return ports

    @staticmethod
    def get_five_g_cu_status_by_ip_and_port(
            port: int, ip: str, timeout: int = csle_collector_constants.GRPC.TIMEOUT_SECONDS) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        A method that sends a request to the 5G Cu manager with a specific port and ip
        to get the status of the 5G CU

        :param port: the port of the FiveGCUManager
        :param ip: the ip of the FiveGCUManager
        :param timeout: the timeout of the GRPC query
        :return: the status of the FiveGCUManager
        """
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub(channel)
            status = \
                csle_collector.five_g_cu_manager.query_five_g_cu_manager.get_five_g_cu_status(
                    stub=stub, timeout=timeout)
            return status

    @staticmethod
    def start_five_g_cus(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                         logger: logging.Logger) -> None:
        """
        Utility method for starting the 5G CUs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    FiveGCUController.start_five_g_cu(emulation_env_config=emulation_env_config,
                                                      ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def start_five_g_cu(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Utility method for starting the 5G CU on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Starting the 5G CU on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_cu_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub(channel)
            status = csle_collector.five_g_cu_manager.query_five_g_cu_manager.start_five_g_cu(stub=stub)
            return status

    @staticmethod
    def stop_five_g_cus(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                        logger: logging.Logger) -> None:
        """
        Utility method for stopping the 5G CUs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    FiveGCUController.stop_five_g_cu(emulation_env_config=emulation_env_config,
                                                     ip=c.docker_gw_bridge_ip, logger=logger)

    @staticmethod
    def stop_five_g_cu(emulation_env_config: EmulationEnvConfig, ip: str, logger: logging.Logger) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Utility method for stopping the 5G cu on a specific container

        :param emulation_env_config: the emulation env config
        :param ip: the ip of the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Stopping the 5G CU on container with ip {ip} in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_cu_manager_port
        with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub(channel)
            status = csle_collector.five_g_cu_manager.query_five_g_cu_manager.stop_five_g_cu(stub=stub)
            return status

    @staticmethod
    def get_five_g_cu_managers_info(emulation_env_config: EmulationEnvConfig, active_ips: List[str],
                                    logger: logging.Logger, physical_server_ip: str) -> FiveGCUManagersInfo:
        """
        Extracts the information of the 5G CU managers for a given emulation

        :param emulation_env_config: the configuration of the emulation
        :param active_ips: list of active IPs
        :param physical_server_ip: the IP of the physical server
        :param logger: the logger to use for logging
        :return: a DTO with the status of the 5G core managers
        """
        five_g_cu_managers_ips = FiveGCUController.get_five_g_cu_managers_ips(
            emulation_env_config=emulation_env_config)
        five_g_core_managers_ports = FiveGCUController.get_five_g_cu_managers_ports(
            emulation_env_config=emulation_env_config)
        five_g_cu_managers_statuses = []
        five_g_cu_managers_running = []
        for ip in five_g_cu_managers_ips:
            if ip not in active_ips or not EmulationUtil.physical_ip_match(
                    emulation_env_config=emulation_env_config, ip=ip, physical_host_ip=physical_server_ip):
                continue
            running = False
            status = None
            try:
                status = FiveGCUController.get_five_g_cu_status_by_ip_and_port(
                    port=emulation_env_config.five_g_config.five_g_cu_manager_port, ip=ip)
                running = True
            except Exception as e:
                logger.debug(
                    f"Could not fetch 5G CU manager status on IP:{ip}, error: {str(e)}, {repr(e)}")
            if status is not None:
                five_g_cu_managers_statuses.append(status)
            else:
                util = csle_collector.five_g_cu_manager.five_g_cu_manager_util.FiveGCUManagerUtil
                five_g_cu_managers_statuses.append(util.five_g_cu_status_dto_empty())
            five_g_cu_managers_running.append(running)
        execution_id = emulation_env_config.execution_id
        emulation_name = emulation_env_config.name
        five_g_core_manager_info_dto = FiveGCUManagersInfo(
            five_g_cu_managers_running=five_g_cu_managers_running, ips=five_g_cu_managers_ips,
            ports=five_g_core_managers_ports, execution_id=execution_id, emulation_name=emulation_name,
            five_g_cu_managers_statuses=five_g_cu_managers_statuses)
        return five_g_core_manager_info_dto

    @staticmethod
    def init_five_g_cus(emulation_env_config: EmulationEnvConfig, physical_server_ip: str,
                        logger: logging.Logger) -> None:
        """
        Utility method for initializing the 5G CUs of a specific execution

        :param emulation_env_config: the emulation env config
        :param physical_server_ip: the ip of the physical server
        :param logger: the logger to use for logging
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            if c.physical_host_ip != physical_server_ip:
                continue
            for ids_image in constants.CONTAINER_IMAGES.FIVE_G_CU_IMAGES:
                if ids_image in c.name:
                    FiveGCUController.init_five_g_cu(emulation_env_config=emulation_env_config,
                                                     container=c, logger=logger)

    @staticmethod
    def init_five_g_cu(emulation_env_config: EmulationEnvConfig, container: NodeContainerConfig,
                       logger: logging.Logger) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Utility method for initializing the 5G CU on a specific container

        :param emulation_env_config: the emulation env config
        :param container: the container
        :param logger: the logger to use for logging
        :return: None
        """
        logger.info(f"Initializing the 5G CU on container with ip {container.docker_gw_bridge_ip} "
                    f"in execution {emulation_env_config.execution_id} "
                    f"of emulation: {emulation_env_config.name}")
        port = emulation_env_config.five_g_config.five_g_cu_manager_port
        core_backhaul_ip = emulation_env_config.five_g_config.core_backhaul_ip
        cu_backhaul_ip = ""
        for cu_ip in emulation_env_config.five_g_config.cu_backhaul_ips:
            if cu_ip in container.get_ips():
                cu_backhaul_ip = cu_ip
        if cu_backhaul_ip == "":
            raise ValueError("Could not find cu backhaul ip")
        with grpc.insecure_channel(f'{container.docker_gw_bridge_ip}:{port}',
                                   options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
            stub = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub(channel)
            status = csle_collector.five_g_cu_manager.query_five_g_cu_manager.init_five_g_cu(
                core_backhaul_ip=core_backhaul_ip, cu_backhaul_ip=cu_backhaul_ip, stub=stub)
            return status
