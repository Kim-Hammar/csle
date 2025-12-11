import grpc
import csle_common.constants.constants as constants
import csle_collector.traffic_manager.traffic_manager_pb2_grpc
import csle_collector.traffic_manager.query_traffic_manager

if __name__ == '__main__':
    ip = "172.18.0.36"
    port = 50043

    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.traffic_manager.traffic_manager_pb2_grpc.TrafficManagerStub(channel)
        status = csle_collector.traffic_manager.query_traffic_manager.get_traffic_status(stub=stub)
        print(f"Traffic generator running: {status.running}, traffic script: {status.script}")
