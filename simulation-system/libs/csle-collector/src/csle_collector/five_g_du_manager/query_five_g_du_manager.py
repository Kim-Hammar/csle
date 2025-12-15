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
    :return: a FiveGDUStatusDTO describing the status of the 5G du
    """
    stop_5g_ue_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.StopFiveGUEMsg()
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.stopFiveGUE(stop_5g_ue_msg, timeout=timeout)
    return five_g_du_status


def init_five_g_ue(
        stub: csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub,
        timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
    """
    Sends a request to the 5G du manager for initializing the 5G UE

    :param stub: the stub to send the remote gRPC to the server
    :return: a FiveGDUStatusDTO describing the status of the 5G du
    """
    init_5g_ue_msg = \
        csle_collector.five_g_du_manager.five_g_du_manager_pb2.InitFiveGUEMsg()
    five_g_du_status: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO = \
        stub.initFiveGUE(init_5g_ue_msg, timeout=timeout)
    return five_g_du_status
