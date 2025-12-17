from typing import List
import grpc
import csle_common.constants.constants as constants
import csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc
import csle_collector.five_g_core_manager.five_g_core_manager_pb2
import csle_collector.five_g_core_manager.query_five_g_core_manager


def get_status(ip: str, port: int):
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
        status = csle_collector.five_g_core_manager.query_five_g_core_manager.get_five_g_core_status(stub=stub)
        status_str = (f"mongo_running: {status.mongo_running},\n mme_running: {status.mme_running},\n"
                      f"sgwc_running: {status.sgwc_running},\nsmf_running: {status.smf_running},\n"
                      f"amf_running: {status.amf_running},\nsgwu_running: {status.sgwu_running},\n"
                      f"upf_running: {status.upf_running},\nhss_running: {status.hss_running},\n"
                      f"pcrf_running: {status.pcrf_running},\nnrf_running: {status.nrf_running},\n"
                      f"scp_running: {status.scp_running},\nsepp_running: {status.sepp_running},\n"
                      f"ausf_running: {status.ausf_running},\nudm_running: {status.udm_running},\n"
                      f"pcf_running: {status.pcf_running},\nnssf_running: {status.nssf_running},\n"
                      f"bsf_running: {status.bsf_running},\nudr_running: {status.udr_running},\n"
                      f"webui_running: {status.webui_running},\nip: {status.ip}")
        print(status_str)


def start_5g_core(ip: str, port: int):
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
        status = csle_collector.five_g_core_manager.query_five_g_core_manager.start_five_g_core(stub=stub)
        status_str = (f"mongo_running: {status.mongo_running},\nmme_running: {status.mme_running},\n"
                      f"sgwc_running: {status.sgwc_running},\nsmf_running: {status.smf_running},\n"
                      f"amf_running: {status.amf_running},\nsgwu_running: {status.sgwu_running},\n"
                      f"upf_running: {status.upf_running},\nhss_running: {status.hss_running},\n"
                      f"pcrf_running: {status.pcrf_running},\nnrf_running: {status.nrf_running},\n"
                      f"scp_running: {status.scp_running},\nsepp_running: {status.sepp_running},\n"
                      f"ausf_running: {status.ausf_running},\nudm_running: {status.udm_running},\n"
                      f"pcf_running: {status.pcf_running},\nnssf_running: {status.nssf_running},\n"
                      f"bsf_running: {status.bsf_running},\nudr_running: {status.udr_running},\n"
                      f"webui_running: {status.webui_running},\nip: {status.ip}")
        print(status_str)


def stop_5g_core(ip: str, port: int):
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
        status = csle_collector.five_g_core_manager.query_five_g_core_manager.stop_five_g_core(stub=stub)
        status_str = (f"mongo_running: {status.mongo_running},\nmme_running: {status.mme_running},\n"
                      f"sgwc_running: {status.sgwc_running},\nsmf_running: {status.smf_running},\n"
                      f"amf_running: {status.amf_running},\nsgwu_running: {status.sgwu_running},\n"
                      f"upf_running: {status.upf_running},\nhss_running: {status.hss_running},\n"
                      f"pcrf_running: {status.pcrf_running},\nnrf_running: {status.nrf_running},\n"
                      f"scp_running: {status.scp_running},\nsepp_running: {status.sepp_running},\n"
                      f"ausf_running: {status.ausf_running},\nudm_running: {status.udm_running},\n"
                      f"pcf_running: {status.pcf_running},\nnssf_running: {status.nssf_running},\n"
                      f"bsf_running: {status.bsf_running},\nudr_running: {status.udr_running},\n"
                      f"webui_running: {status.webui_running},\nip: {status.ip}")
        print(status_str)


def init_5g_core(
        ip: str, port: int,
        subscribers: List[csle_collector.five_g_core_manager.five_g_core_manager_pb2.SubscriberDTO],
        core_ip: str):
    with grpc.insecure_channel(f'{ip}:{port}', options=constants.GRPC_SERVERS.GRPC_OPTIONS) as channel:
        stub = csle_collector.five_g_core_manager.five_g_core_manager_pb2_grpc.FiveGCoreManagerStub(channel)
        status = csle_collector.five_g_core_manager.query_five_g_core_manager.init_five_g_core(
            stub=stub, subscribers=subscribers, core_ip=core_ip)
        status_str = (f"mongo_running: {status.mongo_running},\nmme_running: {status.mme_running},\n"
                      f"sgwc_running: {status.sgwc_running},\nsmf_running: {status.smf_running},\n"
                      f"amf_running: {status.amf_running},\nsgwu_running: {status.sgwu_running},\n"
                      f"upf_running: {status.upf_running},\nhss_running: {status.hss_running},\n"
                      f"pcrf_running: {status.pcrf_running},\nnrf_running: {status.nrf_running},\n"
                      f"scp_running: {status.scp_running},\nsepp_running: {status.sepp_running},\n"
                      f"ausf_running: {status.ausf_running},\nudm_running: {status.udm_running},\n"
                      f"pcf_running: {status.pcf_running},\nnssf_running: {status.nssf_running},\n"
                      f"bsf_running: {status.bsf_running},\nudr_running: {status.udr_running},\n"
                      f"webui_running: {status.webui_running},\nip: {status.ip}")
        print(status_str)


if __name__ == '__main__':
    ip = "172.18.0.6"
    core_ip = "15.16.3.50"
    port = 50052
    # get_status(ip, port)
    # start_5g_core(ip, port)
    stop_5g_core(ip, port)
    # from csle_common.dao.emulation_config.five_g_subscriber_config import FiveGSubscriberConfig
    # subscribers = [
    #     FiveGSubscriberConfig(
    #         imsi="001010123456780", key="00112233445566778899aabbccddeeff",
    #         opc="63BFA50EE6523365FF14C1F45F88737D", amf="8000", sqn=10
    #     )
    # ]
    # init_5g_core(ip, port, subscribers, core_ip)
