import grpc
import csle_common.constants.constants as constants
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc
import csle_collector.five_g_cu_manager.query_five_g_cu_manager


def get_status(ip: str, port: int):
    """
    Gets the status of the 5G CU

    :param ip: the IP of the 5G CU manager
    :param port: the port of the 5G CU manager
    :return: None
    """
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub(channel)
        status = csle_collector.five_g_cu_manager.query_five_g_cu_manager.get_five_g_cu_status(stub=stub)
        status_str = f"cu_running: {status.cu_running}, ip: {status.ip}"
        print(status_str)


def start_5g_cu(ip: str, port: int):
    """
    Starts the 5G CU

    :param ip: the IP of the 5G CU manager
    :param port: the port of the 5G CU manager
    :return: None
    """
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub(channel)
        status = csle_collector.five_g_cu_manager.query_five_g_cu_manager.start_five_g_cu(stub=stub)
        status_str = f"cu_running: {status.cu_running}, ip: {status.ip}"
        print(status_str)


def stop_5g_cu(ip: str, port: int):
    """
    Stops the 5G CU

    :param ip: the IP of the 5G CU manager
    :param port: the port of the 5G CU manager
    :return: None
    """
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2_grpc.FiveGCUManagerStub(channel)
        status = csle_collector.five_g_cu_manager.query_five_g_cu_manager.stop_five_g_cu(stub=stub)
        status_str = f"cu_running: {status.cu_running}, ip: {status.ip}"
        print(status_str)


if __name__ == '__main__':
    ip = "172.18.0.7"
    port = 50053
    # get_status(ip, port)
    start_5g_cu(ip, port)
    # stop_5g_cu(ip, port)
