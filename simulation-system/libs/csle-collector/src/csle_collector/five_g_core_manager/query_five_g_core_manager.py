from typing import List
import csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc
import csle_collector.five_g_core_manager.five_g_core_manager_pb2
import csle_collector.constants.constants as constants


def get_five_g_core_status(
        stub: csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
    """
    Queries the 5G core manager for the status of the 5G core

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCoreStatusDTO describing the status of the 5G core
    """
    get_5g_core_status_msg = \
        csle_collector.five_g_core_manager.five_g_core_manager_pb2.GetFiveGCoreStatusMsg()
    five_g_core_status: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO = \
        stub.getFiveGCoreStatus(get_5g_core_status_msg, timeout=timeout)
    return five_g_core_status


def start_five_g_core(
        stub: csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
    """
    Sends a request to the 5G core manager for starting the 5G core services

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCoreStatusDTO describing the status of the 5G core
    """
    start_5g_core_msg = \
        csle_collector.five_g_core_manager.five_g_core_manager_pb2.StartFiveGCoreMsg()
    five_g_core_status: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO = \
        stub.startFiveGCore(start_5g_core_msg, timeout=timeout)
    return five_g_core_status


def stop_five_g_core(
        stub: csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
    """
    Sends a request to the 5G core manager for stopping the 5G core services

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCoreStatusDTO describing the status of the 5G core
    """
    stop_5g_core_msg = \
        csle_collector.five_g_core_manager.five_g_core_manager_pb2.StopFiveGCoreMsg()
    five_g_core_status: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO = \
        stub.stopFiveGCore(stop_5g_core_msg, timeout=timeout)
    return five_g_core_status


def init_five_g_core(
        stub: csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub,
        subscribers: List[csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGSubscriberDTO],
        core_backhaul_ip: str, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
    """
    Sends a request to the 5G core manager for stopping the 5G core services

    :param stub: the stub to send the remote gRPC to the server
    :param subscribers: list of subscribers
    :param core_backhaul_ip: The backhaul IP of the core network
    :param timeout: the timeout for the gRRPC call
    :return: a FiveGCoreStatusDTO describing the status of the 5G core
    """
    init_5g_core_msg = csle_collector.five_g_core_manager.five_g_core_manager_pb2.InitFiveGCoreMsg(
        subscribers=subscribers, core_backhaul_ip=core_backhaul_ip)
    five_g_core_status: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO = \
        stub.initFiveGCore(init_5g_core_msg, timeout=timeout)
    return five_g_core_status


def start_five_g_core_monitor(
        stub: csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub,
        kafka_ip: str, kafka_port: int, time_step_len_seconds: int, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
    """
    Sends a request to the 5G core manager to start the core monitor thread

    :param kafka_ip: the ip of the Kafka server
    :param kafka_port: the port of the Kafka server
    :param time_step_len_seconds: the length of one time-step
    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a FiveGCoreStatusDTO describing the core status
    """
    start_core_monitor_msg = csle_collector.five_g_core_manager.five_g_core_manager_pb2.StartFiveGCoreMonitorMsg(
        kafka_ip=kafka_ip, kafka_port=kafka_port, time_step_len_seconds=time_step_len_seconds
    )
    core_dto: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO = \
        stub.startFiveGCoreMonitor(start_core_monitor_msg, timeout=timeout)
    return core_dto


def stop_five_g_core_monitor(
        stub: csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
    """
    Sends a request to the 5G Core manager to stop the 5G Core monitor thread

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a FiveGCoreStatusDTO describing the 5G core status
    """
    stop_core_monitor_msg = \
        csle_collector.five_g_core_manager.five_g_core_manager_pb2.StopFiveGCoreMonitorMsg()
    core_dto: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO = \
        stub.stopFiveGCoreMonitor(stop_core_monitor_msg, timeout=timeout)
    return core_dto
