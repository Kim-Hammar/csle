import grpc
import csle_common.constants.constants as constants
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.query_host_manager

if __name__ == '__main__':
    ip = "172.18.0.4"
    port = 50049

    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
        status = csle_collector.host_manager.query_host_manager.get_host_status(stub=stub)
        print(f"Monitor running: {status.monitor_running}, filebeat running: {status.filebeat_running}, "
              f"packetbeat running: {status.packetbeat_running}, "
              f"metricbeat running: {status.metricbeat_running}, "
              f"heartbeat running: {status.heartbeat_running}, ip: {status.ip}")
