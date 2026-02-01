import grpc
import csle_common.constants.constants as constants
import csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc
import csle_collector.five_g_du_manager.query_five_g_du_manager


def get_status(ip: str, port: int):
    """
    Gets the status of the 5G DU

    :param ip: the IP of the 5G DU manager
    :param port: the port of the 5G DU manager
    :return: None
    """
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
        status = csle_collector.five_g_du_manager.query_five_g_du_manager.get_five_g_du_status(stub=stub)
        status_str = f"du_running: {status.du_running}, ue_running: {status.ue_running}, ip: {status.ip}"
        print(status_str)


def start_5g_du(ip: str, port: int):
    """
    Starts the 5G DU

    :param ip: the IP of the 5G DU manager
    :param port: the port of the 5G DU manager
    :return: None
    """
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
        status = csle_collector.five_g_du_manager.query_five_g_du_manager.start_five_g_du(stub=stub)
        status_str = f"du_running: {status.du_running}, ue_running: {status.ue_running}, ip: {status.ip}"
        print(status_str)


def stop_5g_du(ip: str, port: int):
    """
    Stops the 5G DU

    :param ip: the IP of the 5G DU manager
    :param port: the port of the 5G DU manager
    :return: None
    """
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
        status = csle_collector.five_g_du_manager.query_five_g_du_manager.stop_five_g_du(stub=stub)
        status_str = f"du_running: {status.du_running}, ue_running: {status.ue_running}, ip: {status.ip}"
        print(status_str)


def change_5g_signal_strength(ip: str, port: int):
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_du_manager.five_g_du_manager_pb2_grpc.FiveGDUManagerStub(channel)
        status = csle_collector.five_g_du_manager.query_five_g_du_manager.set_five_g_du_ue_signal_strength(
            stub=stub, tx_gain=10, rx_gain=10)
        status_str = f"du_running: {status.du_running}, ue_running: {status.ue_running}, ip: {status.ip}"
        print(status_str)


if __name__ == '__main__':
    ip = "172.18.0.12"
    port = 50054
    change_5g_signal_strength(ip, port)
    # get_status(ip, port)
    # start_5g_du(ip, port)
    # stop_5g_cu(ip, port)
