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
        subscribers: List[csle_collector.five_g_core_manager.five_g_core_manager_pb2.SubscriberDTO],
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
