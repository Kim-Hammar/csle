import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2
import csle_collector.constants.constants as constants


def get_five_g_cu_status(
        stub: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
    """
    Queries the 5G cu manager for the status of the 5G cu

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCUStatusDTO describing the status of the 5G cu
    """
    get_5g_cu_status_msg = \
        csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.GetFiveGCUStatusMsg()
    five_g_cu_status: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO = \
        stub.getFiveGCUStatus(get_5g_cu_status_msg, timeout=timeout)
    return five_g_cu_status


def start_five_g_cu(
        stub: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
    """
    Sends a request to the 5G cu manager for starting the 5G cu

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCUStatusDTO describing the status of the 5G cu
    """
    start_5g_cu_msg = \
        csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StartFiveGCUMsg()
    five_g_cu_status: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO = \
        stub.startFiveGCU(start_5g_cu_msg, timeout=timeout)
    return five_g_cu_status


def stop_five_g_cu(
        stub: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
    """
    Sends a request to the 5G cu manager for stopping the 5G cu

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCUStatusDTO describing the status of the 5G cu
    """
    stop_5g_cu_msg = \
        csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StopFiveGCUMsg()
    five_g_cu_status: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO = \
        stub.stopFiveGCU(stop_5g_cu_msg, timeout=timeout)
    return five_g_cu_status


def init_five_g_cu(
        stub: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub,
        core_backhaul_ip: str, cu_backhaul_ip: str, cu_fronthaul_ip: str,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
    """
    Sends a request to the 5G cu manager for initializing the 5G cu

    :param stub: the stub to send the remote gRPC to the server
    :param core_backhaul_ip: the backhaul ip of the core network
    :param cu_backhaul_ip: the backhaul ip of the CU network
    :param cu_fronthaul_ip: the fronthaul ip of the CU network
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCUStatusDTO describing the status of the 5G cu
    """
    init_5g_cu_msg = \
        csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.InitFiveGCUMsg(
            core_backhaul_ip=core_backhaul_ip, cu_backhaul_ip=cu_backhaul_ip, cu_fronthaul_ip=cu_fronthaul_ip)
    five_g_cu_status: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO = \
        stub.initFiveGCU(init_5g_cu_msg, timeout=timeout)
    return five_g_cu_status


def start_five_g_cu_monitor(stub: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub,
                            kafka_ip: str, kafka_port: int, time_step_len_seconds: int,
                            timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
    """
    Sends a request to the 5G CU manager to start the CU monitor thread

    :param kafka_ip: the ip of the Kafka server
    :param kafka_port: the port of the Kafka server
    :param time_step_len_seconds: the length of one time-step
    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a FiveGCUStatusDTO describing the cu status
    """
    start_cu_monitor_msg = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StartFiveGCUMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds
    )
    cu_dto: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO = \
        stub.startFiveGCUMonitor(start_cu_monitor_msg, timeout=timeout)
    return cu_dto


def stop_five_g_cu_monitor(
        stub: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
    """
    Sends a request to the 5G CU manager to stop the CU monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a FiveGCUStatusDTO describing the 5G cu status
    """
    stop_cu_monitor_msg = \
        csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StopFiveGCUMonitorMsg()
    cu_dto: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO = \
        stub.stopFiveGCUMonitor(stop_cu_monitor_msg, timeout=timeout)
    return cu_dto
