import subprocess
import json
import io
import sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController
import csle_common.constants.constants as constants


#  docker update --memory="20g" --cpus=1.0 csle_cloud_ran_cu_1_2-level17-15
#  nohup iperf3 -s -p 5201 > /dev/null &

def run_iperf(du_name: str, port: int, load: int):
    """
    Generates load with iperf from a 5G UE and measures the network performance

    :param du_name: the name of the 5G DU ontainer
    :param port: the port of the iperf server
    :param load: the load to generate (Mbit/s)
    :return: the results of iperf
    """
    cmd = [
        "docker", "exec", du_name,
        "ip", "netns", "exec", "ue1",
        "iperf3", "-c", "10.45.0.1",
        "-u", "-b", f"{load}M", "-t", "180",
        "-p", str(port), "--json"
    ]
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(process.stdout)
        sum_data = data["end"]["sum"]
        return {
            "du": du_name,
            "jitter_ms": float(sum_data["jitter_ms"]),
            "throughput_bps": float(sum_data["bits_per_second"]),
            "lost_percent": float(sum_data["lost_percent"]),
            "status": "Success"
        }
    except Exception as e:
        print(f"Failed to run iperf: {e}")
        return {"du": du_name, "status": f"Error: {str(e)}"}


if __name__ == '__main__':
    # Parameters of the evaluation
    emulation = "csle-level17-090"
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=emulation)
    execution = executions[0]
    signal_strength = 10
    cpu_limit = 0.9
    memory_limit = 20.0
    num_samples = 5
    emulation_env_config = execution.emulation_env_config
    du_names = [
        "csle_cloud_ran_du_1_1-level17-15",
        "csle_cloud_ran_du_1_2-level17-15",
        "csle_cloud_ran_du_1_3-level17-15",
        "csle_cloud_ran_du_1_4-level17-15"
    ]
    cu_names = [
        "csle_cloud_ran_cu_1_1-level17-15",
        "csle_cloud_ran_cu_1_2-level17-15"
    ]
    iperf_ports = [5201, 5202, 5203, 5204]

    # Initialize statistics
    statistics = {}
    statistics["load"] = []
    statistics["signal_strength"] = []
    statistics["cpu_limit"] = []
    statistics["memory_limit"] = []
    for du in du_names:
        statistics[du] = {}
        statistics[du]["e2e_jitter_ms"] = []
        statistics[du]["e2e_throughput_bps"] = []
        statistics[du]["e2e_lost_percent"] = []
        statistics[du]["du_mac_layer_processing_latency_us"] = []
        statistics[du]["du_mac_layer_cpu_usage_percent"] = []
        statistics[du]["du_physical_layer_uplink_cpu_usage_percent"] = []
        statistics[du]["du_physical_layer_downlink_cpu_usage_percent"] = []
        statistics[du]["du_physical_layer_downlink_processing_latency_us"] = []
        statistics[du]["du_physical_layer_uplink_processing_latency_us"] = []
        statistics[du]["du_physical_layer_snr_uplink_db"] = []
        statistics[du]["du_physical_layer_channel_estimation_latency_us"] = []
        statistics[du]["du_physical_layer_uplink_throughput_mbps"] = []
        statistics[du]["du_physical_layer_downlink_throughput_mbps"] = []
        statistics[du]["du_rlc_creating_pdu_latency_ns"] = []
        statistics[du]["du_cell_scheduling_processing_latency_ms"] = []
        statistics[du]["du_cell_downlink_bitrate_bps"] = []
        statistics[du]["du_cell_uplink_bitrate_bps"] = []
        statistics[du]["du_cell_modulation_and_coding_scheme_downlink"] = []
        statistics[du]["du_cell_modulation_and_coding_scheme_uplink"] = []
        statistics[du]["du_cell_block_error_rate_percent_downlink"] = []
        statistics[du]["du_cell_block_error_rate_percent_uplink"] = []
        statistics[du]["du_cpu_usage_percent"] = []
        statistics[du]["du_memory_usage_mb"] = []
        statistics[du]["du_power_consumption_watts"] = []
    for cu in cu_names:
        statistics[cu] = {}
        statistics[cu]["cu_power_consumption_watts"] = []
        statistics[cu]["cu_cpu_usage_percent"] = []
        statistics[cu]["cu_memory_usage_mb"] = []

    # Running the performance test
    for load in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]:
        for j in range(num_samples):
            print(f"Starting experiment. Load: {load}MB. Signal strength: {signal_strength}dB, CPU limit: {cpu_limit}, "
                  f"Memory limit: {memory_limit}GB. Sample: {j+1}/{num_samples}.")
            sys.stdout.flush()
            loads = [load] * len(du_names)
            statistics["load"].append(load)
            statistics["signal_strength"].append(signal_strength)
            statistics["cpu_limit"].append(cpu_limit)
            statistics["memory_limit"].append(memory_limit)
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(run_iperf, du_names, iperf_ports, loads))

            time_series = ClusterController.get_execution_time_series_data(
                ip=execution.emulation_env_config.kafka_config.container.physical_host_ip,
                port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, minutes=2,
                ip_first_octet=execution.ip_first_octet, emulation=execution.emulation_env_config.name)
            du_rlc_creating_pdu_latency_ns = 0
            for i, du in enumerate(du_names):
                statistics[du]["e2e_jitter_ms"].append(results[i]['jitter_ms'])
                statistics[du]["e2e_throughput_bps"].append(results[i]['throughput_bps'])
                statistics[du]["e2e_lost_percent"].append(results[i]['lost_percent'])
                statistics[du]["du_mac_layer_processing_latency_us"].append(
                    np.mean(list(map(lambda x: x.average_latency_us, time_series.five_g_du_metrics[du])))
                )
                statistics[du]["du_mac_layer_cpu_usage_percent"].append(
                    np.mean(list(map(lambda x: x.cpu_usage_percent, time_series.five_g_du_metrics[du])))
                )
                statistics[du]["du_physical_layer_uplink_cpu_usage_percent"].append(
                    np.mean(list(map(lambda x: x.ul_cpu_usage_percent, time_series.five_g_du_low_metrics[du])))
                )
                statistics[du]["du_physical_layer_downlink_cpu_usage_percent"].append(
                    np.mean(list(map(lambda x: x.dl_cpu_usage_percent, time_series.five_g_du_low_metrics[du])))
                )
                statistics[du]["du_physical_layer_downlink_processing_latency_us"].append(
                    np.mean(list(map(lambda x: x.dl_avg_latency_us, time_series.five_g_du_low_metrics[du])))
                )
                statistics[du]["du_physical_layer_uplink_processing_latency_us"].append(
                    np.mean(list(map(lambda x: x.ul_avg_latency_us, time_series.five_g_du_low_metrics[du])))
                )
                statistics[du]["du_physical_layer_snr_uplink_db"].append(
                    np.mean(list(map(lambda x: x.ul_sinr_db, time_series.five_g_du_low_metrics[du])))
                )
                statistics[du]["du_physical_layer_channel_estimation_latency_us"].append(
                    np.mean(list(map(lambda x: x.ul_ch_est_latency_us, time_series.five_g_du_low_metrics[du])))
                )
                statistics[du]["du_physical_layer_uplink_throughput_mbps"].append(
                    np.mean(list(map(lambda x: x.ul_fec_tput_mbps, time_series.five_g_du_low_metrics[du])))
                )
                statistics[du]["du_physical_layer_downlink_throughput_mbps"].append(
                    np.mean(list(map(lambda x: x.dl_fec_tput_mbps, time_series.five_g_du_low_metrics[du])))
                )
                latencies = []
                for i in range(len(time_series.five_g_du_rlc_metrics[du])):
                    if time_series.five_g_du_rlc_metrics[du][i].rx_num_pdus > 0:
                        du_rlc_creating_pdu_latency_ns = (time_series.five_g_du_rlc_metrics[du][i].tx_sum_pdu_latency_ns
                                                          / time_series.five_g_du_rlc_metrics[du][i].rx_num_pdus)
                        latencies.append(du_rlc_creating_pdu_latency_ns)
                if len(latencies) > 0:
                    statistics[du]["du_rlc_creating_pdu_latency_ns"].append(np.mean(latencies))
                else:
                    statistics[du]["du_rlc_creating_pdu_latency_ns"].append(0.0)
                statistics[du]["du_cell_scheduling_processing_latency_ms"].append(
                    np.mean(list(map(lambda x: x.average_latency, time_series.five_g_du_cell_metrics[du])))
                )
                statistics[du]["du_cell_downlink_bitrate_bps"].append(
                    np.mean(list(map(lambda x: x.dl_brate, time_series.five_g_du_cell_metrics[du])))
                )
                statistics[du]["du_cell_uplink_bitrate_bps"].append(
                    np.mean(list(map(lambda x: x.ul_brate, time_series.five_g_du_cell_metrics[du])))
                )
                statistics[du]["du_cell_modulation_and_coding_scheme_downlink"].append(
                    np.mean(list(map(lambda x: x.dl_mcs, time_series.five_g_du_cell_metrics[du])))
                )
                statistics[du]["du_cell_modulation_and_coding_scheme_uplink"].append(
                    np.mean(list(map(lambda x: x.ul_mcs, time_series.five_g_du_cell_metrics[du])))
                )
                statistics[du]["du_cell_block_error_rate_percent_downlink"].append(
                    np.mean(list(map(lambda x: x.dl_bler, time_series.five_g_du_cell_metrics[du])))
                )
                statistics[du]["du_cell_block_error_rate_percent_uplink"].append(
                    np.mean(list(map(lambda x: x.ul_bler, time_series.five_g_du_cell_metrics[du])))
                )
                statistics[du]["du_cpu_usage_percent"].append(
                    np.mean(
                        list(map(lambda x: x.cpu_usage_percent, time_series.five_g_du_app_resource_usage_metrics[du])))
                )
                statistics[du]["du_memory_usage_mb"].append(
                    np.mean(
                        list(map(lambda x: x.memory_usage_mb, time_series.five_g_du_app_resource_usage_metrics[du])))
                )
                statistics[du]["du_power_consumption_watts"].append(
                    np.mean(
                        list(
                            map(lambda x: x.power_consumption_watts,
                                time_series.five_g_du_app_resource_usage_metrics[du])))
                )

            for cu in cu_names:
                statistics[cu]["cu_power_consumption_watts"].append(
                    np.mean(
                        list(
                            map(lambda x: x.power_consumption_watts,
                                time_series.five_g_cu_app_resource_usage_metrics[cu])))
                )
                statistics[cu]["cu_cpu_usage_percent"].append(
                    np.mean(
                        list(map(lambda x: x.cpu_usage_percent, time_series.five_g_cu_app_resource_usage_metrics[cu]))))
                statistics[cu]["cu_memory_usage_mb"].append(
                    np.mean(
                        list(map(lambda x: x.memory_usage_mb, time_series.five_g_cu_app_resource_usage_metrics[cu]))))
            print(statistics)
            sys.stdout.flush()
            json_str = json.dumps(statistics, indent=4, sort_keys=True)
            with io.open("/home/kim/five_g_statistics.json", 'w', encoding='utf-8') as f:
                f.write(json_str)
