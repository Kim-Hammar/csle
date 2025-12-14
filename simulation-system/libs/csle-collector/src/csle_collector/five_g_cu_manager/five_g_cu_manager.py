import logging
import socket
import netifaces
import grpc
from concurrent import futures
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2
import csle_collector.constants.constants as constants
from csle_collector.five_g_cu_manager.five_g_cu_manager_util import FiveGCUManagerUtil


class FiveGCUManagerServicer(csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.
                               FiveGCUManagerServicer):
    """
    gRPC server for managing the 5g cu
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
        logging.info(f"Starting the 5G CU manager hostname: {self.hostname} ip: {self.ip}")

    def getFiveGCUStatus(
            self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.GetFiveGCUStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Gets the status of the 5G cu

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g cu
        """
        logging.info("Getting the status of the 5G CU services")
        status = FiveGCUManagerUtil.get_script_status_map(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip
        )

    def startFiveGCU(self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StartFiveGCUMsg,
                       context: grpc.ServicerContext) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Starts the 5G cu services

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g cu
        """
        logging.info("Starting the 5G CU services")
        FiveGCUManagerUtil.start_all_services(control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        status = FiveGCUManagerUtil.get_script_status_map(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip
        )

    def stopFiveGCU(self, request: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StopFiveGCUMsg,
                      context: grpc.ServicerContext) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Stops the 5G cu services

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g cu
        """
        logging.info("Stopping the 5G CU services")
        FiveGCUManagerUtil.stop_all_services(control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        status = FiveGCUManagerUtil.get_script_status_map(
            control_script_path=constants.FIVE_G_CU.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO(
            cu_running=status.get(constants.FIVE_G_CU.CU, False),
            ip=self.ip
        )

def serve(port: int = 50052, log_dir: str = "/", max_workers: int = 100,
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
