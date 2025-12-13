import logging
import socket
import netifaces
import grpc
from concurrent import futures
import csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc
import csle_collector.five_g_core_manager.five_g_core_manager_pb2
import csle_collector.constants.constants as constants


class FiveGCoreManagerServicer(csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.
                               FiveGCoreManagerServicer):
    """
    gRPC server for managing the 5g core
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.FIVE_G_CORE_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.FIVE_G_CORE_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        try:
            self.ip = netifaces.ifaddresses(constants.INTERFACES.ETH0)[netifaces.AF_INET][0][constants.INTERFACES.ADDR]
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        logging.info(f"Starting the 5G Core manager hostname: {self.hostname} ip: {self.ip}")

    def getFiveGCoreStatus(
            self, request: csle_collector.five_g_core_manager.five_g_core_manager_pb2.GetFiveGCoreStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Gets the status of the 5G core

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g core
        """
        return csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO(
            mongo_running=False, mme_running=False, sgwc_running=False, smf_running=False, amf_running=False,
            sgwu_running=False, upf_running=False, hss_running=False, pcrf_running=False, nrf_running=False,
            scp_running=False, sepp_running=False, ausf_running=False, udm_running=False, pcf_running=False,
            nssf_running=False, bsf_running=False, udr_running=False, webui_running=False, ip=self.ip
        )


def serve(port: int = 50052, log_dir: str = "/", max_workers: int = 100,
          log_file_name: str = "five_g_core_manager.log") -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.FIVE_G_CORE_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.FIVE_G_CORE_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.add_FiveGCoreManagerServicer_to_server(
        FiveGCoreManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"5G Core Manager Server Started, Listening on port: {port}, num workers: {max_workers}, "
                 f"log file: {log_file_name}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
