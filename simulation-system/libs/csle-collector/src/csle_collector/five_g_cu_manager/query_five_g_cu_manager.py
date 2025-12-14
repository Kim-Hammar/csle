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
    :return: a FiveGCUStatusDTO describing the status of the 5G cu
    """
    stop_5g_cu_msg = \
        csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.StopFiveGCUMsg()
    five_g_cu_status: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO = \
        stub.stopFiveGCU(stop_5g_cu_msg, timeout=timeout)
    return five_g_cu_status
