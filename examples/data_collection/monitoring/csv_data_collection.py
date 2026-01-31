import subprocess
import json
import sys
import time
import os
import csv
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController
import csle_common.constants.constants as constants

# --- MAPPING & METRIC DEFINITIONS ---

NAME_MAPPING = {
    "csle_cloud_ran_du_1_1-level17-15": "DU1",
    "csle_cloud_ran_du_1_2-level17-15": "DU2",
    "csle_cloud_ran_du_1_3-level17-15": "DU3",
    "csle_cloud_ran_du_1_4-level17-15": "DU4",
    "csle_cloud_ran_cu_1_1-level17-15": "CU1",
    "csle_cloud_ran_cu_1_2-level17-15": "CU2"
}

# Metrics to extract from DU (Prefixes like 'du_' will be stripped for column names)
DU_METRIC_KEYS = [
    "du_mac_layer_processing_latency_us", "du_mac_layer_cpu_usage_percent",
    "du_physical_layer_uplink_cpu_usage_percent", "du_physical_layer_downlink_cpu_usage_percent",
    "du_physical_layer_downlink_processing_latency_us", "du_physical_layer_uplink_processing_latency_us",
    "du_physical_layer_snr_uplink_db", "du_physical_layer_channel_estimation_latency_us",
    "du_physical_layer_uplink_throughput_mbps", "du_physical_layer_downlink_throughput_mbps",
    "du_rlc_creating_pdu_latency_ns",
    "du_cell_scheduling_processing_latency_ms", "du_cell_downlink_bitrate_bps", "du_cell_uplink_bitrate_bps",
    "du_cell_modulation_and_coding_scheme_downlink", "du_cell_modulation_and_coding_scheme_uplink",
    "du_cell_block_error_rate_percent_downlink", "du_cell_block_error_rate_percent_uplink",
    "du_cpu_usage_percent", "du_memory_usage_mb", "du_power_consumption_watts"
]

CU_METRIC_KEYS = [
    "cu_power_consumption_watts", "cu_cpu_usage_percent", "cu_memory_usage_mb"
]


def set_docker_cpu_limit(cpu_limit: float, memory_limit: str, container_names: list):
    """Updates the CPU and Memory limits for a list of Docker containers."""
    for container in container_names:
        cmd = ["docker", "update", f"--memory={memory_limit}", f"--cpus={cpu_limit}", container]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error updating container {container}: {e.stderr}")


def run_iperf(du_name: str, port: int, load: int, direction: str):
    """
    Generates load with iperf.
    direction: "uplink" or "downlink"
    """
    cmd = [
        "docker", "exec", du_name,
        "ip", "netns", "exec", "ue1",
        "iperf3", "-c", "10.45.0.1",
        "-u", "-b", f"{load}M", "-t", "180",
        "-p", str(port), "--json"
    ]

    # If Downlink, add Reverse flag (-R)
    if direction == "downlink":
        cmd.append("-R")

    try:
        # print(f"Running {direction} on {du_name} port {port}")
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(process.stdout)
        sum_data = data["end"]["sum"]

        return {
            "du": du_name,
            "direction": direction,
            "jitter_ms": float(sum_data["jitter_ms"]),
            "throughput_bps": float(sum_data["bits_per_second"]),
            "lost_percent": float(sum_data["lost_percent"]),
            "status": "Success"
        }
    except Exception as e:
        # print(f"Failed to run {direction} iperf on {du_name}: {e}")
        return {
            "du": du_name,
            "direction": direction,
            "status": f"Error: {str(e)}",
            "jitter_ms": 0.0,
            "throughput_bps": 0.0,
            "lost_percent": 100.0
        }


def get_csv_headers(du_names, cu_names):
    """Generates the flat CSV header list."""
    headers = ["routing_config"]

    # Process DU Headers
    for original_name in du_names:
        friendly_name = NAME_MAPPING.get(original_name, original_name)

        # Config columns
        for cfg in ["signal_strength", "cpu_limit", "memory_limit", "load_uplink", "load_downlink", "bandwidth",
                    "number_of_antennas"]:
            headers.append(f"{friendly_name}_{cfg}")

        # E2E Metrics
        for direction in ["uplink", "downlink"]:
            headers.append(f"{friendly_name}_e2e_{direction}_jitter_ms")
            headers.append(f"{friendly_name}_e2e_{direction}_throughput_bps")
            headers.append(f"{friendly_name}_e2e_{direction}_lost_percent")

        # Infrastructure/Physical Metrics
        for key in DU_METRIC_KEYS:
            # Strip "du_" prefix safely
            clean_key = key
            if key.startswith("du_"):
                clean_key = key[3:]
            headers.append(f"{friendly_name}_{clean_key}")

    # Process CU Headers
    for original_name in cu_names:
        friendly_name = NAME_MAPPING.get(original_name, original_name)
        for cfg in ["signal_strength", "cpu_limit", "memory_limit"]:
            headers.append(f"{friendly_name}_{cfg}")
        for key in CU_METRIC_KEYS:
            clean_key = key
            if key.startswith("cu_"):
                clean_key = key[3:]
            headers.append(f"{friendly_name}_{clean_key}")

    return sorted(headers)


def append_to_csv(row_data, filepath, fieldnames):
    """Appends a single dictionary row to the CSV."""
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        # extrasaction='ignore' prevents crashing if a key is present in data but missing in headers
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)


def safe_mean(data_list):
    """Helper to average lists safely."""
    if not data_list:
        return 0.0
    return np.mean(data_list)


if __name__ == '__main__':
    # ==========================================
    # --- CONTROL VARIABLES & CONFIGURATION ---
    # ==========================================

    # Traffic Direction Control
    RUN_UPLINK = True
    RUN_DOWNLINK = True

    OUTPUT_CSV_PATH = "/home/kim/five_g_merged_dataset_simultaneous_3.csv"

    emulation = "csle-level17-090"
    signal_strength = 30
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

    # Ports for UPLINK (Standard)
    iperf_ports_ul = [5201, 5202, 5203, 5204]

    # Ports for DOWNLINK (Shifted by 1000 to avoid conflicts on the server)
    # Ensure your traffic sink/server is listening on these ports too!
    iperf_ports_dl = [6201, 6202, 6203, 6204]

    cpu_limits = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                  2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
    load_levels = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]

    # ==========================================
    # --- EXECUTION LOGIC ---
    # ==========================================

    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=emulation)
    execution = executions[0]
    all_target_containers = du_names + cu_names

    csv_headers = get_csv_headers(du_names, cu_names)
    print(f"Initializing data collection. Output: {OUTPUT_CSV_PATH}")
    print(f"Modes: Uplink={RUN_UPLINK}, Downlink={RUN_DOWNLINK}")

    for current_cpu in cpu_limits:
        print(f"\n--- Setting CPU Limit to {current_cpu} ---")
        set_docker_cpu_limit(current_cpu, memory_limit_docker, all_target_containers)
        time.sleep(5)  # Stabilization time

        for load in load_levels:
            for j in range(num_samples):
                print(f"Experiment: CPU={current_cpu}, Load={load}M, Sample={j + 1}/{num_samples}, signal: {signal_strength}")
                sys.stdout.flush()

                # --- 1. Prepare iperf Tasks ---
                iperf_tasks = []

                # Assign Uplink and Downlink tasks with DISTINCT ports
                for k, du in enumerate(du_names):
                    if RUN_UPLINK:
                        iperf_tasks.append((du, iperf_ports_ul[k], load, "uplink"))
                    if RUN_DOWNLINK:
                        iperf_tasks.append((du, iperf_ports_dl[k], load, "downlink"))

                # --- 2. Run iperf in Parallel ---
                total_workers = len(iperf_tasks)
                if total_workers > 0:
                    with ThreadPoolExecutor(max_workers=total_workers) as executor:
                        futures = [executor.submit(run_iperf, t[0], t[1], t[2], t[3]) for t in iperf_tasks]
                        iperf_results = [f.result() for f in futures]
                else:
                    iperf_results = []

                # --- 3. Retrieve System Metrics ---
                time_series = ClusterController.get_execution_time_series_data(
                    ip=execution.emulation_env_config.kafka_config.container.physical_host_ip,
                    port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, minutes=2,
                    ip_first_octet=execution.ip_first_octet, emulation=execution.emulation_env_config.name)

                # --- 4. Build CSV Row ---
                row = {"routing_config": 1}

                # Map results for easy lookup
                results_map = {name: {"uplink": None, "downlink": None} for name in du_names}
                for res in iperf_results:
                    if res["du"] in results_map:
                        results_map[res["du"]][res["direction"]] = res

                # --- PROCESS DUs ---
                for du in du_names:
                    fname = NAME_MAPPING.get(du, du)

                    # A. Configs
                    row[f"{fname}_signal_strength"] = signal_strength
                    row[f"{fname}_cpu_limit"] = current_cpu
                    row[f"{fname}_memory_limit"] = memory_limit_gb
                    row[f"{fname}_load_uplink"] = load if RUN_UPLINK else 0.0
                    row[f"{fname}_load_downlink"] = load if RUN_DOWNLINK else 0.0
                    row[f"{fname}_bandwidth"] = 5
                    row[f"{fname}_number_of_antennas"] = 1

                    # B. E2E Metrics (Uplink)
                    if RUN_UPLINK and results_map[du]["uplink"]:
                        res = results_map[du]["uplink"]
                        row[f"{fname}_e2e_uplink_jitter_ms"] = res['jitter_ms']
                        row[f"{fname}_e2e_uplink_throughput_bps"] = res['throughput_bps']
                        row[f"{fname}_e2e_uplink_lost_percent"] = res['lost_percent']
                    else:
                        row[f"{fname}_e2e_uplink_jitter_ms"] = 0.0
                        row[f"{fname}_e2e_uplink_throughput_bps"] = 0.0
                        row[f"{fname}_e2e_uplink_lost_percent"] = 0.0

                    # C. E2E Metrics (Downlink)
                    if RUN_DOWNLINK and results_map[du]["downlink"]:
                        res = results_map[du]["downlink"]
                        row[f"{fname}_e2e_downlink_jitter_ms"] = res['jitter_ms']
                        row[f"{fname}_e2e_downlink_throughput_bps"] = res['throughput_bps']
                        row[f"{fname}_e2e_downlink_lost_percent"] = res['lost_percent']
                    else:
                        row[f"{fname}_e2e_downlink_jitter_ms"] = 0.0
                        row[f"{fname}_e2e_downlink_throughput_bps"] = 0.0
                        row[f"{fname}_e2e_downlink_lost_percent"] = 0.0

                    # D. Internal DU Metrics
                    row[f"{fname}_mac_layer_processing_latency_us"] = safe_mean(
                        [x.average_latency_us for x in time_series.five_g_du_metrics[du]])
                    row[f"{fname}_mac_layer_cpu_usage_percent"] = safe_mean(
                        [x.cpu_usage_percent for x in time_series.five_g_du_metrics[du]])

                    row[f"{fname}_physical_layer_uplink_cpu_usage_percent"] = safe_mean(
                        [x.ul_cpu_usage_percent for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_physical_layer_downlink_cpu_usage_percent"] = safe_mean(
                        [x.dl_cpu_usage_percent for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_physical_layer_downlink_processing_latency_us"] = safe_mean(
                        [x.dl_avg_latency_us for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_physical_layer_uplink_processing_latency_us"] = safe_mean(
                        [x.ul_avg_latency_us for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_physical_layer_snr_uplink_db"] = safe_mean(
                        [x.ul_sinr_db for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_physical_layer_channel_estimation_latency_us"] = safe_mean(
                        [x.ul_ch_est_latency_us for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_physical_layer_uplink_throughput_mbps"] = safe_mean(
                        [x.ul_fec_tput_mbps for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_physical_layer_downlink_throughput_mbps"] = safe_mean(
                        [x.dl_fec_tput_mbps for x in time_series.five_g_du_low_metrics[du]])

                    # RLC Latency
                    rlc_latencies = []
                    for m in time_series.five_g_du_rlc_metrics[du]:
                        if m.rx_num_pdus > 0:
                            rlc_latencies.append(m.tx_sum_pdu_latency_ns / m.rx_num_pdus)
                    row[f"{fname}_rlc_creating_pdu_latency_ns"] = safe_mean(rlc_latencies)

                    # Cell Metrics
                    row[f"{fname}_cell_scheduling_processing_latency_ms"] = safe_mean(
                        [x.average_latency for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_cell_downlink_bitrate_bps"] = safe_mean(
                        [x.dl_brate for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_cell_uplink_bitrate_bps"] = safe_mean(
                        [x.ul_brate for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_cell_modulation_and_coding_scheme_downlink"] = safe_mean(
                        [x.dl_mcs for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_cell_modulation_and_coding_scheme_uplink"] = safe_mean(
                        [x.ul_mcs for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_cell_block_error_rate_percent_downlink"] = safe_mean(
                        [x.dl_bler for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_cell_block_error_rate_percent_uplink"] = safe_mean(
                        [x.ul_bler for x in time_series.five_g_du_cell_metrics[du]])

                    # App Resources
                    row[f"{fname}_cpu_usage_percent"] = safe_mean(
                        [x.cpu_usage_percent for x in time_series.five_g_du_app_resource_usage_metrics[du]])
                    row[f"{fname}_memory_usage_mb"] = safe_mean(
                        [x.memory_usage_mb for x in time_series.five_g_du_app_resource_usage_metrics[du]])
                    row[f"{fname}_power_consumption_watts"] = safe_mean(
                        [x.power_consumption_watts for x in time_series.five_g_du_app_resource_usage_metrics[du]])

                # --- PROCESS CUs ---
                for cu in cu_names:
                    fname = NAME_MAPPING.get(cu, cu)
                    row[f"{fname}_signal_strength"] = signal_strength
                    row[f"{fname}_cpu_limit"] = current_cpu
                    row[f"{fname}_memory_limit"] = memory_limit_gb
                    row[f"{fname}_cpu_usage_percent"] = safe_mean(
                        [x.cpu_usage_percent for x in time_series.five_g_cu_app_resource_usage_metrics[cu]])
                    row[f"{fname}_memory_usage_mb"] = safe_mean(
                        [x.memory_usage_mb for x in time_series.five_g_cu_app_resource_usage_metrics[cu]])
                    row[f"{fname}_power_consumption_watts"] = safe_mean(
                        [x.power_consumption_watts for x in time_series.five_g_cu_app_resource_usage_metrics[cu]])

                # 5. Save Row
                append_to_csv(row, OUTPUT_CSV_PATH, csv_headers)

    print("\n--- All Experiments Complete. Data saved to CSV. ---")