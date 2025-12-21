from typing import Union
import logging
import socket
import netifaces
import grpc
from concurrent import futures
import csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc
import csle_collector.five_g_core_manager.five_g_core_manager_pb2
import csle_collector.constants.constants as constants
from csle_collector.five_g_core_manager.five_g_core_manager_util import FiveGCoreManagerUtil
from csle_collector.five_g_core_manager.threads.five_g_core_monitor_thread import FiveGCoreMonitorThread


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
        self.core_monitor_thread: Union[None, FiveGCoreMonitorThread] = None
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
        logging.info("Getting the status of the 5G Core services")
        status = FiveGCoreManagerUtil.get_core_status(
            control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO(
            mongo_running=status.get(constants.FIVE_G_CORE.MONGO, False),
            mme_running=status.get(constants.FIVE_G_CORE.MME, False),
            sgwc_running=status.get(constants.FIVE_G_CORE.SGWC, False),
            smf_running=status.get(constants.FIVE_G_CORE.SMF, False),
            amf_running=status.get(constants.FIVE_G_CORE.AMF, False),
            sgwu_running=status.get(constants.FIVE_G_CORE.SGWU, False),
            upf_running=status.get(constants.FIVE_G_CORE.UPF, False),
            hss_running=status.get(constants.FIVE_G_CORE.HSS, False),
            pcrf_running=status.get(constants.FIVE_G_CORE.PCRF, False),
            nrf_running=status.get(constants.FIVE_G_CORE.NRF, False),
            scp_running=status.get(constants.FIVE_G_CORE.SCP, False),
            sepp_running=status.get(constants.FIVE_G_CORE.SEPP, False),
            ausf_running=status.get(constants.FIVE_G_CORE.AUSF, False),
            udm_running=status.get(constants.FIVE_G_CORE.UDM, False),
            pcf_running=status.get(constants.FIVE_G_CORE.PCF, False),
            nssf_running=status.get(constants.FIVE_G_CORE.NSSF, False),
            bsf_running=status.get(constants.FIVE_G_CORE.BSF, False),
            udr_running=status.get(constants.FIVE_G_CORE.UDR, False),
            webui_running=status.get(constants.FIVE_G_CORE.WEBUI, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def startFiveGCore(self, request: csle_collector.five_g_core_manager.five_g_core_manager_pb2.StartFiveGCoreMsg,
                       context: grpc.ServicerContext) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Starts the 5G core services

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g core
        """
        logging.info("Starting the 5G Core services")
        FiveGCoreManagerUtil.start_all_core_services(control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        status = FiveGCoreManagerUtil.get_core_status(
            control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO(
            mongo_running=status.get(constants.FIVE_G_CORE.MONGO, False),
            mme_running=status.get(constants.FIVE_G_CORE.MME, False),
            sgwc_running=status.get(constants.FIVE_G_CORE.SGWC, False),
            smf_running=status.get(constants.FIVE_G_CORE.SMF, False),
            amf_running=status.get(constants.FIVE_G_CORE.AMF, False),
            sgwu_running=status.get(constants.FIVE_G_CORE.SGWU, False),
            upf_running=status.get(constants.FIVE_G_CORE.UPF, False),
            hss_running=status.get(constants.FIVE_G_CORE.HSS, False),
            pcrf_running=status.get(constants.FIVE_G_CORE.PCRF, False),
            nrf_running=status.get(constants.FIVE_G_CORE.NRF, False),
            scp_running=status.get(constants.FIVE_G_CORE.SCP, False),
            sepp_running=status.get(constants.FIVE_G_CORE.SEPP, False),
            ausf_running=status.get(constants.FIVE_G_CORE.AUSF, False),
            udm_running=status.get(constants.FIVE_G_CORE.UDM, False),
            pcf_running=status.get(constants.FIVE_G_CORE.PCF, False),
            nssf_running=status.get(constants.FIVE_G_CORE.NSSF, False),
            bsf_running=status.get(constants.FIVE_G_CORE.BSF, False),
            udr_running=status.get(constants.FIVE_G_CORE.UDR, False),
            webui_running=status.get(constants.FIVE_G_CORE.WEBUI, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def stopFiveGCore(self, request: csle_collector.five_g_core_manager.five_g_core_manager_pb2.StopFiveGCoreMsg,
                      context: grpc.ServicerContext) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Stops the 5G core services

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g core
        """
        logging.info("Stopping the 5G Core services")
        FiveGCoreManagerUtil.stop_all_core_services(control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        status = FiveGCoreManagerUtil.get_core_status(
            control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO(
            mongo_running=status.get(constants.FIVE_G_CORE.MONGO, False),
            mme_running=status.get(constants.FIVE_G_CORE.MME, False),
            sgwc_running=status.get(constants.FIVE_G_CORE.SGWC, False),
            smf_running=status.get(constants.FIVE_G_CORE.SMF, False),
            amf_running=status.get(constants.FIVE_G_CORE.AMF, False),
            sgwu_running=status.get(constants.FIVE_G_CORE.SGWU, False),
            upf_running=status.get(constants.FIVE_G_CORE.UPF, False),
            hss_running=status.get(constants.FIVE_G_CORE.HSS, False),
            pcrf_running=status.get(constants.FIVE_G_CORE.PCRF, False),
            nrf_running=status.get(constants.FIVE_G_CORE.NRF, False),
            scp_running=status.get(constants.FIVE_G_CORE.SCP, False),
            sepp_running=status.get(constants.FIVE_G_CORE.SEPP, False),
            ausf_running=status.get(constants.FIVE_G_CORE.AUSF, False),
            udm_running=status.get(constants.FIVE_G_CORE.UDM, False),
            pcf_running=status.get(constants.FIVE_G_CORE.PCF, False),
            nssf_running=status.get(constants.FIVE_G_CORE.NSSF, False),
            bsf_running=status.get(constants.FIVE_G_CORE.BSF, False),
            udr_running=status.get(constants.FIVE_G_CORE.UDR, False),
            webui_running=status.get(constants.FIVE_G_CORE.WEBUI, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def initFiveGCore(self, request: csle_collector.five_g_core_manager.five_g_core_manager_pb2.InitFiveGCoreMsg,
                      context: grpc.ServicerContext) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Initializes the 5G core services

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the 5g core
        """
        logging.info("Initializing the 5G Core services")
        FiveGCoreManagerUtil.init_all_core_services(control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        FiveGCoreManagerUtil.init_subscriber_data(
            control_script_path=constants.FIVE_G_CORE.SUBSCRIBER_CONTROL_SCRIPT_PATH,
            subscribers=list(request.subscribers))
        FiveGCoreManagerUtil.init_config_files(ip=request.core_backhaul_ip)
        status = FiveGCoreManagerUtil.get_core_status(
            control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO(
            mongo_running=status.get(constants.FIVE_G_CORE.MONGO, False),
            mme_running=status.get(constants.FIVE_G_CORE.MME, False),
            sgwc_running=status.get(constants.FIVE_G_CORE.SGWC, False),
            smf_running=status.get(constants.FIVE_G_CORE.SMF, False),
            amf_running=status.get(constants.FIVE_G_CORE.AMF, False),
            sgwu_running=status.get(constants.FIVE_G_CORE.SGWU, False),
            upf_running=status.get(constants.FIVE_G_CORE.UPF, False),
            hss_running=status.get(constants.FIVE_G_CORE.HSS, False),
            pcrf_running=status.get(constants.FIVE_G_CORE.PCRF, False),
            nrf_running=status.get(constants.FIVE_G_CORE.NRF, False),
            scp_running=status.get(constants.FIVE_G_CORE.SCP, False),
            sepp_running=status.get(constants.FIVE_G_CORE.SEPP, False),
            ausf_running=status.get(constants.FIVE_G_CORE.AUSF, False),
            udm_running=status.get(constants.FIVE_G_CORE.UDM, False),
            pcf_running=status.get(constants.FIVE_G_CORE.PCF, False),
            nssf_running=status.get(constants.FIVE_G_CORE.NSSF, False),
            bsf_running=status.get(constants.FIVE_G_CORE.BSF, False),
            udr_running=status.get(constants.FIVE_G_CORE.UDR, False),
            webui_running=status.get(constants.FIVE_G_CORE.WEBUI, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def startFiveGCoreMonitor(
            self, request: csle_collector.five_g_core_manager.five_g_core_manager_pb2.StartFiveGCoreMonitorMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Starts the 5G Core monitor thread

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Core monitor thread
        """
        logging.info(f"Starting the 5G CoreMonitor thread, timestep length: {request.time_step_len_seconds}, "
                     f"kafka ip: {request.kafka_ip}, "
                     f"kafka port: {request.kafka_port}")
        if self.core_monitor_thread is not None:
            self.core_monitor_thread.running = False
        self.core_monitor_thread = FiveGCoreMonitorThread(kafka_ip=request.kafka_ip, kafka_port=request.kafka_port,
                                                          ip=self.ip, hostname=self.hostname,
                                                          time_step_len_seconds=request.time_step_len_seconds)
        self.core_monitor_thread.start()
        logging.info("Started the 5G CoreMonitor thread")

        status = FiveGCoreManagerUtil.get_core_status(
            control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO(
            mongo_running=status.get(constants.FIVE_G_CORE.MONGO, False),
            mme_running=status.get(constants.FIVE_G_CORE.MME, False),
            sgwc_running=status.get(constants.FIVE_G_CORE.SGWC, False),
            smf_running=status.get(constants.FIVE_G_CORE.SMF, False),
            amf_running=status.get(constants.FIVE_G_CORE.AMF, False),
            sgwu_running=status.get(constants.FIVE_G_CORE.SGWU, False),
            upf_running=status.get(constants.FIVE_G_CORE.UPF, False),
            hss_running=status.get(constants.FIVE_G_CORE.HSS, False),
            pcrf_running=status.get(constants.FIVE_G_CORE.PCRF, False),
            nrf_running=status.get(constants.FIVE_G_CORE.NRF, False),
            scp_running=status.get(constants.FIVE_G_CORE.SCP, False),
            sepp_running=status.get(constants.FIVE_G_CORE.SEPP, False),
            ausf_running=status.get(constants.FIVE_G_CORE.AUSF, False),
            udm_running=status.get(constants.FIVE_G_CORE.UDM, False),
            pcf_running=status.get(constants.FIVE_G_CORE.PCF, False),
            nssf_running=status.get(constants.FIVE_G_CORE.NSSF, False),
            bsf_running=status.get(constants.FIVE_G_CORE.BSF, False),
            udr_running=status.get(constants.FIVE_G_CORE.UDR, False),
            webui_running=status.get(constants.FIVE_G_CORE.WEBUI, False),
            ip=self.ip, monitor_running=self._is_monitor_running()
        )

    def stopFiveGCoreMonitor(
            self, request: csle_collector.five_g_core_manager.five_g_core_manager_pb2.StopFiveGCoreMonitorMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Stops the Core monitor thread if it is running

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a DTO with the status of the Core monitor thread
        """
        logging.info("Stopping the 5G core monitor")
        if self.core_monitor_thread is not None:
            self.core_monitor_thread.running = False
        logging.info("5G Core monitor stopped")
        status = FiveGCoreManagerUtil.get_core_status(
            control_script_path=constants.FIVE_G_CORE.CONTROL_SCRIPT_PATH)
        return csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO(
            mongo_running=status.get(constants.FIVE_G_CORE.MONGO, False),
            mme_running=status.get(constants.FIVE_G_CORE.MME, False),
            sgwc_running=status.get(constants.FIVE_G_CORE.SGWC, False),
            smf_running=status.get(constants.FIVE_G_CORE.SMF, False),
            amf_running=status.get(constants.FIVE_G_CORE.AMF, False),
            sgwu_running=status.get(constants.FIVE_G_CORE.SGWU, False),
            upf_running=status.get(constants.FIVE_G_CORE.UPF, False),
            hss_running=status.get(constants.FIVE_G_CORE.HSS, False),
            pcrf_running=status.get(constants.FIVE_G_CORE.PCRF, False),
            nrf_running=status.get(constants.FIVE_G_CORE.NRF, False),
            scp_running=status.get(constants.FIVE_G_CORE.SCP, False),
            sepp_running=status.get(constants.FIVE_G_CORE.SEPP, False),
            ausf_running=status.get(constants.FIVE_G_CORE.AUSF, False),
            udm_running=status.get(constants.FIVE_G_CORE.UDM, False),
            pcf_running=status.get(constants.FIVE_G_CORE.PCF, False),
            nssf_running=status.get(constants.FIVE_G_CORE.NSSF, False),
            bsf_running=status.get(constants.FIVE_G_CORE.BSF, False),
            udr_running=status.get(constants.FIVE_G_CORE.UDR, False),
            webui_running=status.get(constants.FIVE_G_CORE.WEBUI, False),
            ip=self.ip, monitor_running=False
        )

    def _is_monitor_running(self) -> bool:
        """
        Utility method to check if the monitor is running

        :return: True if running else false
        """
        if self.core_monitor_thread is not None:
            return self.core_monitor_thread.running
        return False


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
