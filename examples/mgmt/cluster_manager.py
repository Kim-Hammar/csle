import grpc
import csle_common.constants.constants as constants
import csle_cluster.cluster_manager.cluster_manager_pb2_grpc
import csle_cluster.cluster_manager.query_cluster_manager


def get_five_g_du_status(ip: str, port: int, emulation: str, ip_first_octet: int):
    """
    Gets the status of the 5G DU managers in the cluster

    :param ip: the IP of the cluster manager
    :param port: the port of the cluster manager
    :param emulation: the name of the emulation
    :param ip_first_octet: the first octet of the IP range of the emulation
    :return: None
    """
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_cluster.cluster_manager.cluster_manager_pb2_grpc.ClusterManagerStub(channel)
        info = csle_cluster.cluster_manager.query_cluster_manager.get_five_g_du_managers_info(
            stub=stub, emulation=emulation, ip_first_octet=ip_first_octet)
        print(info)


if __name__ == '__main__':
    ip = "172.31.212.92"
    port = 50041
    emulation = "csle-level16-090"
    ip_first_octet = 15
    get_five_g_du_status(ip=ip, port=port, emulation=emulation, ip_first_octet=ip_first_octet)
