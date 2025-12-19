from typing import Union
import logging
import socket
import netifaces
import grpc
from concurrent import futures
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2
import csle_collector.constants.constants as constants
from csle_collector.five_g_cu_manager.five_g_cu_manager_util import FiveGCUManagerUtil
from csle_collector.five_g_cu_manager.threads.five_g_cu_monitor_thread import FiveGCUMonitorThread


class FiveGCUManagerServicer(csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerServicer):
    """
    gRPC server for managing the 5G CU
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.FIVE_G_CU_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.FIVE_G_CU_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        try:
            self.ip = netifaces.ifaddresses(constants.INTERFACES.ETH0)[netifaces.AF_INET][0][constants.INTERFACES.ADDR]
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.cu_monitor_thread: Union[None, FiveGCUMonitorThread] = None
        logging.info(f"Starting the 5G CU manager hostname: {self.hostname} ip: {self.ip}")

    def getFiveGCUStatus(
            self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.GetFiveGCUStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Gets the status of the 5G CU

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g cu
        """
        logging.info("Getting the status of the 5G CU")
        status = FiveGCUManagerUtil.get_cu_status(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def startFiveGCU(self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StartFiveGCUMsg,
                     context: grpc.ServicerContext) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Starts the 5G CU

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g cu
        """
        logging.info("Starting the 5G CU")
        FiveGCUManagerUtil.start_cu(control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        status = FiveGCUManagerUtil.get_cu_status(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def stopFiveGCU(self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StopFiveGCUMsg,
                    context: grpc.ServicerContext) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Stops the 5G CU

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g cu
        """
        logging.info("Stopping the 5G CU")
        FiveGCUManagerUtil.stop_cu(control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        status = FiveGCUManagerUtil.get_cu_status(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def initFiveGCU(self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.InitFiveGCUMsg,
                    context: grpc.ServicerContext) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Initializes the 5G CU

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g cu
        """
        logging.info("Initializing the 5G CU")
        FiveGCUManagerUtil.init_config_file(core_backhaul_ip=request.core_backhaul_ip,
                                            cu_backhaul_ip=request.cu_backhaul_ip,
                                            cu_fronthaul_ip=request.cu_fronthaul_ip)
        status = FiveGCUManagerUtil.get_cu_status(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def startFiveGCUMonitor(
            self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StartFiveGCUMonitorMsg,
            context: grpc.ServicerContext) -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Starts the 5G CU monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the CU monitor thread
        """
        logging.info(f"Starting the 5G CUMonitor thread, timestep length: {request.time_step_len_seconds}, "
                     f"kafka ip: {request.kafka_ip}, "
                     f"kafka port: {request.kafka_port}")
        if self.cu_monitor_thread is not None:
            self.cu_monitor_thread.running = False
        self.cu_monitor_thread = FiveGCUMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                      ip=self.ip, hostname=self.hostname,
                                                      time_step_len_seconds=request.time_step_len_seconds)
        self.cu_monitor_thread.start()
        logging.info("Started the 5G CU Monitor thread")

        status = FiveGCUManagerUtil.get_cu_status(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip, monitor_running=True
        )

    def stopFiveGCUMonitor(self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StopFiveGCUMonitorMsg,
                           context: grpc.ServicerContext) -> (
            csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO):
        """
        Stops the CU monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the CU monitor thread
        """
        logging.info("Stopping the 5G CU monitor")
        if self.cu_monitor_thread is not None:
            self.cu_monitor_thread.running = False
        logging.info("5G CU monitor stopped")
        status = FiveGCUManagerUtil.get_cu_status(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip, monitor_running=False
        )

    def _is_monitor_running(self) -> bool:
        """
        Utility method to check if the monitor is running

        :return: True if running else false
        """
        if self.cu_monitor_thread is not None:
            return self.cu_monitor_thread.running
        return False


def serve(port: int = 50053, log_dir: str = "/", max_workers: int = 100,
          log_file_name: str = "five_g_cu_manager.log") -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.FIVE_G_CU_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.FIVE_G_CU_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.add_FiveGCUManagerServicer_to_server(
        FiveGCUManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"5G CU Manager Server Started, Listening on port: {port}, num workers: {max_workers}, "
                 f"log file: {log_file_name}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
