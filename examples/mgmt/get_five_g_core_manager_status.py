import grpc
import csle_common.constants.constants as constants
import csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc
import csle_collector.five_g_core_manager.query_five_g_core_manager

if __name__ == '__main__':
    ip = "172.18.0.6"
    port = 50052

    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
        status = csle_collector.five_g_core_manager.query_five_g_core_manager.get_five_g_core_status(stub=stub)
        status_str = (f"mongo_running: {status.mongo_running},\n mme_running: {status.mme_running},\n "
                      f"sgwc_running: {status.sgwc_running},\n smf_running: {status.smf_running},\n "
                      f"amf_running: {status.amf_running},\n sgwu_running: {status.sgwu_running},\n "
                      f"upf_running: {status.upf_running},\n hss_running: {status.hss_running},\n "
                      f"pcrf_running: {status.pcrf_running}\n, nrf_running: {status.nrf_running},\n "
                      f"scp_running: {status.scp_running}\n, sepp_running: {status.sepp_running},\n "
                      f"ausf_running: {status.ausf_running}\n, udm_running: {status.udm_running},\n "
                      f"pcf_running: {status.pcf_running}\n, nssf_running: {status.nssf_running},\n "
                      f"bsf_running: {status.bsf_running}\n, udr_running: {status.udr_running},\n "
                      f"webui_running: {status.webui_running}\n, ip: {status.ip}")
        print(status_str)
