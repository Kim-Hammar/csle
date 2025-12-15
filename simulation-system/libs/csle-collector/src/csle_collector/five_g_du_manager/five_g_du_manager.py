import logging
import socket
import netifaces
import grpc
from concurrent import futures
import csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc
import csle_collector.five_g_du_manager.five_g_du_manager_pb2
import csle_collector.constants.constants as constants
from csle_collector.five_g_du_manager.five_g_du_manager_util import FiveGDUManagerUtil


class FiveGDUManagerServicer(csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerServicer):
    """
    gRPC server for managing the 5G DU
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.FIVE_G_DU_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.FIVE_G_DU_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        try:
            self.ip = netifaces.ifaddresses(constants.INTERFACES.ETH0)[netifaces.AF_INET][0][constants.INTERFACES.ADDR]
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.ip}:{constants.KAFKA.PORT}",
                     constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        logging.info(f"Starting the 5G DU manager hostname: {self.hostname} ip: {self.ip}")

    def getFiveGDUStatus(
            self, request: csle_collector.five_g_du_manager.five_g_du_manager_pb2.GetFiveGDUStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Gets the status of the 5G DU

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g du
        """
        logging.info("Getting the status of the 5G DU")
        status_du = FiveGDUManagerUtil.get_du_status(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_ue = FiveGDUManagerUtil.get_ue_status(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO(
            du_running=status_du.get(constants.FIVE_G_DU.DU, False),
            ue_running=status_ue.get(constants.FIVE_G_DU.UE, False),
            ip=self.ip
        )

    def startFiveGDU(self, request: csle_collector.five_g_du_manager.five_g_du_manager_pb2.StartFiveGDUMsg,
                     context: grpc.ServicerContext) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Starts the 5G DU

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g du
        """
        logging.info("Starting the 5G DU")
        FiveGDUManagerUtil.start_du(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_du = FiveGDUManagerUtil.get_du_status(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_ue = FiveGDUManagerUtil.get_ue_status(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO(
            du_running=status_du.get(constants.FIVE_G_DU.DU, False),
            ue_running=status_ue.get(constants.FIVE_G_DU.UE, False),
            ip=self.ip
        )

    def stopFiveGDU(self, request: csle_collector.five_g_du_manager.five_g_du_manager_pb2.StopFiveGDUMsg,
                    context: grpc.ServicerContext) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Stops the 5G DU

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g du
        """
        logging.info("Stopping the 5G DU")
        FiveGDUManagerUtil.stop_du(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_du = FiveGDUManagerUtil.get_du_status(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_ue = FiveGDUManagerUtil.get_ue_status(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO(
            du_running=status_du.get(constants.FIVE_G_DU.DU, False),
            ue_running=status_ue.get(constants.FIVE_G_DU.UE, False),
            ip=self.ip
        )

    def stopFiveGUE(self, request: csle_collector.five_g_du_manager.five_g_du_manager_pb2.StopFiveGUEMsg,
                    context: grpc.ServicerContext) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Stops the 5G UE

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g DU
        """
        logging.info("Stopping the 5G UE")
        FiveGDUManagerUtil.stop_ue(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        status_du = FiveGDUManagerUtil.get_du_status(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_ue = FiveGDUManagerUtil.get_ue_status(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO(
            du_running=status_du.get(constants.FIVE_G_DU.DU, False),
            ue_running=status_ue.get(constants.FIVE_G_DU.UE, False),
            ip=self.ip
        )

    def startFiveGUE(self, request: csle_collector.five_g_du_manager.five_g_du_manager_pb2.StartFiveGUEMsg,
                     context: grpc.ServicerContext) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Starts the 5G UE

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g DU
        """
        logging.info("Starting the 5G UE")
        FiveGDUManagerUtil.start_ue(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        status_du = FiveGDUManagerUtil.get_du_status(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_ue = FiveGDUManagerUtil.get_ue_status(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO(
            du_running=status_du.get(constants.FIVE_G_DU.DU, False),
            ue_running=status_ue.get(constants.FIVE_G_DU.UE, False),
            ip=self.ip
        )

    def initFiveGUE(self, request: csle_collector.five_g_du_manager.five_g_du_manager_pb2.InitFiveGUEMsg,
                    context: grpc.ServicerContext) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Initializes the 5G UE

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g DU
        """
        logging.info("Initializing the 5G UE")
        FiveGDUManagerUtil.init_ue(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        status_du = FiveGDUManagerUtil.get_du_status(control_script_path=constants.FIVE_G_DU.CONTROL_SCRIPT_PATH)
        status_ue = FiveGDUManagerUtil.get_ue_status(control_script_path=constants.FIVE_G_DU.UE_CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO(
            du_running=status_du.get(constants.FIVE_G_DU.DU, False),
            ue_running=status_ue.get(constants.FIVE_G_DU.UE, False),
            ip=self.ip
        )


def serve(port: int = 50054, log_dir: str = "/", max_workers: int = 100,
          log_file_name: str = "five_g_du_manager.log") -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.FIVE_G_DU_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.FIVE_G_DU_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.add_FiveGDUManagerServicer_to_server(
        FiveGDUManagerServicer(), server)
    server.add_insedure_port(f'[::]:{port}')
    server.start()
    logging.info(f"5G DU Manager Server Started, Listening on port: {port}, num workers: {max_workers}, "
                 f"log file: {log_file_name}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
