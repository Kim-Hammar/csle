import csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc
import csle_collector.five_g_du_manager.five_g_du_manager_pb2
import csle_collector.constants.constants as constants


def get_five_g_du_status(
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Queries the 5G du manager for the status of the 5G du

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGDUStatusDTO describing the status of the 5G du
    """
    get_5g_du_status_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.GetFiveGDUStatusMsg()
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.getFiveGDUStatus(get_5g_du_status_msg, timeout=timeout)
    return five_g_du_status


def start_five_g_du(
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G du manager for starting the 5G du

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGDUStatusDTO describing the status of the 5G du
    """
    start_5g_du_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.StartFiveGDUMsg()
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.startFiveGDU(start_5g_du_msg, timeout=timeout)
    return five_g_du_status


def stop_five_g_du(
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G du manager for stopping the 5G du

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGDUStatusDTO describing the status of the 5G du
    """
    stop_5g_du_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.StopFiveGDUMsg()
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.stopFiveGDU(stop_5g_du_msg, timeout=timeout)
    return five_g_du_status


def start_five_g_ue(
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G DU manager for starting the 5G UE

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGDUStatusDTO describing the status of the 5G UE
    """
    start_5g_ue_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.StartFiveGUEMsg()
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.startFiveGUE(start_5g_ue_msg, timeout=timeout)
    return five_g_du_status


def stop_five_g_ue(
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G du manager for stopping the 5G UE

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGDUStatusDTO describing the status of the 5G du
    """
    stop_5g_ue_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.StopFiveGUEMsg()
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.stopFiveGUE(stop_5g_ue_msg, timeout=timeout)
    return five_g_du_status


def init_five_g_du_ue(
        cu_fronthaul_ip: str, du_fronthaul_ip: str,
        imsi: str, key: str, opc: str, imei: str,
        gnb_du_id: int, pci: int, sector_id: int,
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G DU manager for initializing the 5G UE and DU

    :param cu_fronthaul_ip: the fronthaul IP of the CU
    :param du_fronthaul_ip: the fronthaul IP of the DU
    :param imsi: IMSI of the UE subscriber
    :param key: private key of the UE subscriber
    :param opc: key of the operator of the UE subscriber
    :param imei: imei of the UE subscriber
    :param gnb_du_id: The ID of the DU
    :param pci: Physical Cell ID of the DU
    :param sector_id: Part of the cell ID
    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGDUStatusDTO describing the status of the 5G du
    """
    init_5g_du_ue_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.InitFiveGDUUEMsg(
            cu_fronthaul_ip=cu_fronthaul_ip, du_fronthaul_ip=du_fronthaul_ip,
            imsi=imsi, key=key, opc=opc, imei=imei, gnb_du_id=gnb_du_id, pci=pci, sector_id=sector_id)
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.initFiveGDUUE(init_5g_du_ue_msg, timeout=timeout)
    return five_g_du_status


def start_five_g_du_monitor(stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
                            kafka_ip: str, kafka_port: int, time_step_len_seconds: int,
                            timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G DU manager to start the 5G DU monitor thread

    :param kafka_ip: the ip of the Kafka server
    :param kafka_port: the port of the Kafka server
    :param time_step_len_seconds: the length of one time-step
    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a FiveGDUStatusDTO describing the cu status
    """
    start_du_monitor_msg = csle_collector.five_g_du_manager.five_g_du_manager_pb2.StartFiveGDUMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds)
    du_dto: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.startFiveGDUMonitor(start_du_monitor_msg, timeout=timeout)
    return du_dto


def stop_five_g_du_monitor(
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G DU manager to stop the 5G DU monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a FiveGDUStatusDTO describing the 5G DU status
    """
    stop_du_monitor_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.StopFiveGDUMonitorMsg()
    du_dto: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.stopFiveGDUMonitor(stop_du_monitor_msg, timeout=timeout)
    return du_dto
