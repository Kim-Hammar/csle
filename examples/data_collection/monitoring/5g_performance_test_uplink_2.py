import subprocess
import json
import io
import sys
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController
import csle_common.constants.constants as constants


def set_docker_cpu_limit(cpu_limit: float, memory_limit: str, container_names: list):
    """
    Updates the CPU and Memory limits for a list of Docker containers.
    """
    for container in container_names:
        cmd = ["docker", "update", f"--memory={memory_limit}", f"--cpus={cpu_limit}", container]
        try:
            print(f"Executing: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error updating container {container}: {e.stderr}")


def run_iperf(du_name: str, port: int, load: int):
    """
    Generates load with iperf from a 5G UE and measures the network performance
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
        print(f"Failed to run iperf on {du_name}: {e}")
        return {
            "du": du_name,
            "status": f"Error: {str(e)}",
            "jitter_ms": 0.0,
            "throughput_bps": 0.0,
            "lost_percent": 100.0
        }


def initialize_statistics(du_names, cu_names):
    """
    Helper to initialize the statistics dictionary structure.
    """
    stats = {
        "load": [],
        "signal_strength": [],
        "cpu_limit": [],
        "memory_limit": []
    }
    for du in du_names:
        stats[du] = {
            "e2e_uplink_jitter_ms": [],
            "e2e_uplink_throughput_bps": [],
            "e2e_uplink_lost_percent": [],
            "du_mac_layer_processing_latency_us": [],
            "du_mac_layer_cpu_usage_percent": [],
            "du_physical_layer_uplink_cpu_usage_percent": [],
            "du_physical_layer_downlink_cpu_usage_percent": [],
            "du_physical_layer_downlink_processing_latency_us": [],
            "du_physical_layer_uplink_processing_latency_us": [],
            "du_physical_layer_snr_uplink_db": [],
            "du_physical_layer_channel_estimation_latency_us": [],
            "du_physical_layer_uplink_throughput_mbps": [],
            "du_physical_layer_downlink_throughput_mbps": [],
            "du_rlc_creating_pdu_latency_ns": [],
            "du_cell_scheduling_processing_latency_ms": [],
            "du_cell_downlink_bitrate_bps": [],
            "du_cell_uplink_bitrate_bps": [],
            "du_cell_modulation_and_coding_scheme_downlink": [],
            "du_cell_modulation_and_coding_scheme_uplink": [],
            "du_cell_block_error_rate_percent_downlink": [],
            "du_cell_block_error_rate_percent_uplink": [],
            "du_cpu_usage_percent": [],
            "du_memory_usage_mb": [],
            "du_power_consumption_watts": []
        }
    for cu in cu_names:
        stats[cu] = {
            "cu_power_consumption_watts": [],
            "cu_cpu_usage_percent": [],
            "cu_memory_usage_mb": []
        }
    return stats


if __name__ == '__main__':
    # Parameters of the evaluation
    emulation = "csle-level17-090"
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=emulation)
    execution = executions[0]
    signal_strength = 50
    memory_limit_gb = 20.0
    memory_limit_docker = "20g"
    num_samples = 2

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
    all_target_containers = du_names + cu_names
    iperf_ports = [5201, 5202, 5203, 5204]

    # CPU Range: 0.5 to 3.0
    # cpu_limits = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
    # cpu_limits = [2.6, 2.7, 2.8, 2.9, 3.0]
    # cpu_limits = [0.5, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
    #               2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]

    # cpu_limits = [1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
    cpu_limits = [2.5, 2.6, 2.7, 2.8, 2.9, 3.0]

    # Initialize Global Statistics for final combined file
    combined_statistics = initialize_statistics(du_names, cu_names)

    # Main Experiment Loop
    for current_cpu in cpu_limits:
        # Initialize Individual CPU Statistics
        cpu_stats = initialize_statistics(du_names, cu_names)

        # Format CPU string for filename (0.5 -> 0_5)
        cpu_label = str(float(current_cpu)).replace('.', '_')
        individual_filename = f"/home/kim/five_g_statistics_uplink_cpu_{cpu_label}_gain_{signal_strength}_memory_{int(memory_limit_gb)}.json"

        # Update Docker containers with the new limit
        print(f"\n--- Setting CPU Limit to {current_cpu} ---")
        set_docker_cpu_limit(current_cpu, memory_limit_docker, all_target_containers)
        time.sleep(5)  # Stabilization time

        for load in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]:
            for j in range(num_samples):
                print(f"Experiment: CPU={current_cpu}, Load={load}M, Sample={j + 1}/{num_samples}, Gain: {signal_strength}")
                sys.stdout.flush()

                # Metadata updates
                for stats_dict in [cpu_stats, combined_statistics]:
                    stats_dict["load"].append(load)
                    stats_dict["signal_strength"].append(signal_strength)
                    stats_dict["cpu_limit"].append(current_cpu)
                    stats_dict["memory_limit"].append(memory_limit_gb)

                # Run iperf in parallel
                loads = [load] * len(du_names)
                with ThreadPoolExecutor(max_workers=4) as executor:
                    results = list(executor.map(run_iperf, du_names, iperf_ports, loads))

                # Retrieve time series data
                time_series = ClusterController.get_execution_time_series_data(
                    ip=execution.emulation_env_config.kafka_config.container.physical_host_ip,
                    port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, minutes=2,
                    ip_first_octet=execution.ip_first_octet, emulation=execution.emulation_env_config.name)

                # Process DU metrics
                for i, du in enumerate(du_names):
                    for stats_dict in [cpu_stats, combined_statistics]:
                        stats_dict[du]["e2e_uplink_jitter_ms"].append(results[i]['jitter_ms'])
                        stats_dict[du]["e2e_uplink_throughput_bps"].append(results[i]['throughput_bps'])
                        stats_dict[du]["e2e_uplink_lost_percent"].append(results[i]['lost_percent'])

                        stats_dict[du]["du_mac_layer_processing_latency_us"].append(
                            np.mean(list(map(lambda x: x.average_latency_us, time_series.five_g_du_metrics[du])))
                        )
                        stats_dict[du]["du_mac_layer_cpu_usage_percent"].append(
                            np.mean(list(map(lambda x: x.cpu_usage_percent, time_series.five_g_du_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_uplink_cpu_usage_percent"].append(
                            np.mean(list(map(lambda x: x.ul_cpu_usage_percent, time_series.five_g_du_low_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_downlink_cpu_usage_percent"].append(
                            np.mean(list(map(lambda x: x.dl_cpu_usage_percent, time_series.five_g_du_low_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_downlink_processing_latency_us"].append(
                            np.mean(list(map(lambda x: x.dl_avg_latency_us, time_series.five_g_du_low_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_uplink_processing_latency_us"].append(
                            np.mean(list(map(lambda x: x.ul_avg_latency_us, time_series.five_g_du_low_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_snr_uplink_db"].append(
                            np.mean(list(map(lambda x: x.ul_sinr_db, time_series.five_g_du_low_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_channel_estimation_latency_us"].append(
                            np.mean(list(map(lambda x: x.ul_ch_est_latency_us, time_series.five_g_du_low_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_uplink_throughput_mbps"].append(
                            np.mean(list(map(lambda x: x.ul_fec_tput_mbps, time_series.five_g_du_low_metrics[du])))
                        )
                        stats_dict[du]["du_physical_layer_downlink_throughput_mbps"].append(
                            np.mean(list(map(lambda x: x.dl_fec_tput_mbps, time_series.five_g_du_low_metrics[du])))
                        )

                        # RLC Latency
                        latencies = []
                        for k in range(len(time_series.five_g_du_rlc_metrics[du])):
                            if time_series.five_g_du_rlc_metrics[du][k].rx_num_pdus > 0:
                                val = (time_series.five_g_du_rlc_metrics[du][k].tx_sum_pdu_latency_ns
                                       / time_series.five_g_du_rlc_metrics[du][k].rx_num_pdus)
                                latencies.append(val)
                        stats_dict[du]["du_rlc_creating_pdu_latency_ns"].append(
                            np.mean(latencies) if latencies else 0.0)

                        stats_dict[du]["du_cell_scheduling_processing_latency_ms"].append(
                            np.mean(list(map(lambda x: x.average_latency, time_series.five_g_du_cell_metrics[du])))
                        )
                        stats_dict[du]["du_cell_downlink_bitrate_bps"].append(
                            np.mean(list(map(lambda x: x.dl_brate, time_series.five_g_du_cell_metrics[du])))
                        )
                        stats_dict[du]["du_cell_uplink_bitrate_bps"].append(
                            np.mean(list(map(lambda x: x.ul_brate, time_series.five_g_du_cell_metrics[du])))
                        )
                        stats_dict[du]["du_cell_modulation_and_coding_scheme_downlink"].append(
                            np.mean(list(map(lambda x: x.dl_mcs, time_series.five_g_du_cell_metrics[du])))
                        )
                        stats_dict[du]["du_cell_modulation_and_coding_scheme_uplink"].append(
                            np.mean(list(map(lambda x: x.ul_mcs, time_series.five_g_du_cell_metrics[du])))
                        )
                        stats_dict[du]["du_cell_block_error_rate_percent_downlink"].append(
                            np.mean(list(map(lambda x: x.dl_bler, time_series.five_g_du_cell_metrics[du])))
                        )
                        stats_dict[du]["du_cell_block_error_rate_percent_uplink"].append(
                            np.mean(list(map(lambda x: x.ul_bler, time_series.five_g_du_cell_metrics[du])))
                        )
                        stats_dict[du]["du_cpu_usage_percent"].append(
                            np.mean(list(map(lambda x: x.cpu_usage_percent,
                                             time_series.five_g_du_app_resource_usage_metrics[du])))
                        )
                        stats_dict[du]["du_memory_usage_mb"].append(
                            np.mean(list(
                                map(lambda x: x.memory_usage_mb, time_series.five_g_du_app_resource_usage_metrics[du])))
                        )
                        stats_dict[du]["du_power_consumption_watts"].append(
                            np.mean(list(map(lambda x: x.power_consumption_watts,
                                             time_series.five_g_du_app_resource_usage_metrics[du])))
                        )

                # Process CU metrics
                for cu in cu_names:
                    for stats_dict in [cpu_stats, combined_statistics]:
                        stats_dict[cu]["cu_power_consumption_watts"].append(
                            np.mean(list(map(lambda x: x.power_consumption_watts,
                                             time_series.five_g_cu_app_resource_usage_metrics[cu])))
                        )
                        stats_dict[cu]["cu_cpu_usage_percent"].append(
                            np.mean(list(map(lambda x: x.cpu_usage_percent,
                                             time_series.five_g_cu_app_resource_usage_metrics[cu])))
                        )
                        stats_dict[cu]["cu_memory_usage_mb"].append(
                            np.mean(list(
                                map(lambda x: x.memory_usage_mb, time_series.five_g_cu_app_resource_usage_metrics[cu])))
                        )

                # Checkpoint: Save individual CPU file after each experiment
                with io.open(individual_filename, 'w', encoding='utf-8') as f:
                    json.dump(cpu_stats, f, indent=4, sort_keys=True)

                sys.stdout.flush()

    # Final Combined Save
    print("\n--- All Experiments Complete. Saving final combined data. ---")