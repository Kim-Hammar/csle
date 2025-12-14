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
    :return: an FiveGCoreStatusDTO describing the status of the 5G core
    """
    get_5g_core_status_msg = \
        csle_collector.five_g_core_manager.five_g_core_manager_pb2.GetFiveGCoreStatusMsg()
    five_g_core_status: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO = \
        stub.getFiveGCoreStatus(get_5g_core_status_msg, timeout=timeout)
    return five_g_core_status
