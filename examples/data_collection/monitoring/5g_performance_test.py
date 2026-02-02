import subprocess
import json
import sys
import time
import os
import csv
from typing import List, Dict, Any, Union
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController
import csle_common.constants.constants as constants


def set_docker_cpu_limit(cpu_limit: float, memory_limit: str, container_names: List[str]) -> None:
    """
    Updates the CPU and Memory limits for a list of Docker containers.

    :param cpu_limit: the CPU limit to set for the containers
    :param memory_limit: the memory limit string (e.g., "20g")
    :param container_names: list of container names to update
    :return: None
    """
    for container in container_names:
        cmd = constants.COMMANDS.DOCKER_UPDATE_COMMAND.format(memory_limit, cpu_limit, container).split()
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error updating container {container}: {e.stderr}")


def run_iperf(du_name: str, port: int, load: int, direction: str) -> Dict[str, Any]:
    """
    Generates load with iperf for a given DU container.

    :param du_name: the name of the DU container
    :param port: the port number for iperf
    :param load: the load in Mbps
    :param direction: the direction of traffic ("uplink" or "downlink")
    :return: a dictionary containing iperf results including jitter, throughput, and packet loss
    """
    iperf_cmd = constants.COMMANDS.IPERF_COMMAND.format(constants.FIVE_G.CORE_IP, load, 180, port)
    if direction == constants.FIVE_G.DOWNLINK:
        iperf_cmd += f" {constants.FIVE_G.IPERF_REVERSE_FLAG}"
    exec_cmd = constants.COMMANDS.IP_NETNS_EXEC_COMMAND.format(constants.FIVE_G.UE_NAME, iperf_cmd)
    cmd = constants.COMMANDS.DOCKER_EXEC_COMMAND.split() + [du_name] + exec_cmd.split()
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(process.stdout)
        sum_data = data[constants.FIVE_G.END_KEY][constants.FIVE_G.SUM_KEY]

        return {
            constants.FIVE_G.DU: du_name,
            constants.FIVE_G.DIRECTION: direction,
            constants.FIVE_G.JITTER_MS: float(sum_data[constants.FIVE_G.JITTER_MS_KEY]),
            constants.FIVE_G.THROUGHPUT_BPS: float(sum_data[constants.FIVE_G.BITS_PER_SECOND_KEY]),
            constants.FIVE_G.LOST_PERCENT: float(sum_data[constants.FIVE_G.LOST_PERCENT_KEY]),
            constants.FIVE_G.STATUS: constants.FIVE_G.SUCCESS
        }
    except Exception as e:
        return {
            constants.FIVE_G.DU: du_name,
            constants.FIVE_G.DIRECTION: direction,
            constants.FIVE_G.STATUS: f"Error: {str(e)}",
            constants.FIVE_G.JITTER_MS: 0.0,
            constants.FIVE_G.THROUGHPUT_BPS: 0.0,
            constants.FIVE_G.LOST_PERCENT: 100.0
        }


def get_csv_headers(du_names: List[str], cu_names: List[str]) -> List[str]:
    """
    Generates the flat CSV header list based on DU and CU names.

    :param du_names: list of DU container names
    :param cu_names: list of CU container names
    :return: sorted list of CSV header strings
    """
    headers = [constants.FIVE_G.ROUTING_CONFIG]

    for original_name in du_names:
        friendly_name = constants.FIVE_G.NAME_MAPPING.get(original_name, original_name)

        for cfg in [constants.FIVE_G.SIGNAL_STRENGTH, constants.FIVE_G.CPU_LIMIT, constants.FIVE_G.MEMORY_LIMIT,
                    constants.FIVE_G.LOAD_UPLINK, constants.FIVE_G.LOAD_DOWNLINK, constants.FIVE_G.BANDWIDTH,
                    constants.FIVE_G.NUMBER_OF_ANTENNAS]:
            headers.append(f"{friendly_name}_{cfg}")

        for direction in [constants.FIVE_G.UPLINK, constants.FIVE_G.DOWNLINK]:
            headers.append(f"{friendly_name}_{constants.FIVE_G.E2E}_{direction}_{constants.FIVE_G.JITTER_MS}")
            headers.append(f"{friendly_name}_{constants.FIVE_G.E2E}_{direction}_{constants.FIVE_G.THROUGHPUT_BPS}")
            headers.append(f"{friendly_name}_{constants.FIVE_G.E2E}_{direction}_{constants.FIVE_G.LOST_PERCENT}")

        for key in constants.FIVE_G.DU_METRIC_KEYS:
            clean_key = key
            if key.startswith(constants.FIVE_G.DU_PREFIX):
                clean_key = key[len(constants.FIVE_G.DU_PREFIX):]
            headers.append(f"{friendly_name}_{clean_key}")

    for original_name in cu_names:
        friendly_name = constants.FIVE_G.NAME_MAPPING.get(original_name, original_name)
        for cfg in [constants.FIVE_G.SIGNAL_STRENGTH, constants.FIVE_G.CPU_LIMIT, constants.FIVE_G.MEMORY_LIMIT]:
            headers.append(f"{friendly_name}_{cfg}")
        for key in constants.FIVE_G.CU_METRIC_KEYS:
            clean_key = key
            if key.startswith(constants.FIVE_G.CU_PREFIX):
                clean_key = key[len(constants.FIVE_G.CU_PREFIX):]
            headers.append(f"{friendly_name}_{clean_key}")

    return sorted(headers)


def append_to_csv(row_data: Dict[str, Any], filepath: str, fieldnames: List[str]) -> None:
    """
    Appends a single dictionary row to the CSV file.

    :param row_data: dictionary containing the row data to append
    :param filepath: path to the CSV file
    :param fieldnames: list of field names for the CSV header
    :return: None
    """
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)


def safe_mean(data_list: List[Any]) -> float:
    """
    Computes the mean of a list safely, returning 0.0 for empty lists.

    :param data_list: list of numeric values to average
    :return: the mean value or 0.0 if the list is empty
    """
    if not data_list:
        return 0.0
    return float(np.mean(data_list))


def run() -> None:
    """
    Runs 5G performance experiments by varying CPU limits and load levels,
    collecting metrics from DU and CU containers, and saving results to CSV.

    :return: None
    """
    run_uplink = True
    run_downlink = True
    output_csv_path = "/home/kim/five_g_merged_dataset_simultaneous_4.csv"
    emulation = "csle-level17-090"
    signal_strength = 40
    memory_limit_gb = 20.0
    memory_limit_docker = "20g"
    num_samples = 2
    du_names = constants.FIVE_G.DU_NAMES
    cu_names = constants.FIVE_G.CU_NAMES
    iperf_ports_ul = [5201, 5202, 5203, 5204]
    iperf_ports_dl = [6201, 6202, 6203, 6204]
    cpu_limits = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                  2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0]
    load_levels = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=emulation)
    execution = executions[0]
    all_target_containers = du_names + cu_names

    csv_headers = get_csv_headers(du_names, cu_names)
    print(f"Initializing data collection. Output: {output_csv_path}")
    print(f"Modes: Uplink={run_uplink}, Downlink={run_downlink}")

    for current_cpu in cpu_limits:
        print(f"\n--- Setting CPU Limit to {current_cpu} ---")
        set_docker_cpu_limit(current_cpu, memory_limit_docker, all_target_containers)
        time.sleep(5)

        for load in load_levels:
            for j in range(num_samples):
                print(f"Experiment: CPU={current_cpu}, Load={load}M, Sample={j + 1}/{num_samples}, "
                      f"signal: {signal_strength}")
                sys.stdout.flush()

                iperf_tasks = []
                for k, du in enumerate(du_names):
                    if run_uplink:
                        iperf_tasks.append((du, iperf_ports_ul[k], load, constants.FIVE_G.UPLINK))
                    if run_downlink:
                        iperf_tasks.append((du, iperf_ports_dl[k], load, constants.FIVE_G.DOWNLINK))

                total_workers = len(iperf_tasks)
                if total_workers > 0:
                    with ThreadPoolExecutor(max_workers=total_workers) as executor:
                        futures = [executor.submit(run_iperf, t[0], t[1], t[2], t[3]) for t in iperf_tasks]
                        iperf_results = [f.result() for f in futures]
                else:
                    iperf_results = []

                time_series = ClusterController.get_execution_time_series_data(
                    ip=execution.emulation_env_config.kafka_config.container.physical_host_ip,
                    port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, minutes=2,
                    ip_first_octet=execution.ip_first_octet, emulation=execution.emulation_env_config.name)

                row: Dict[str, Union[float, int]] = {constants.FIVE_G.ROUTING_CONFIG: 1}
                results_map = {name: {constants.FIVE_G.UPLINK: None, constants.FIVE_G.DOWNLINK: None}
                               for name in du_names}
                for res in iperf_results:
                    if res[constants.FIVE_G.DU] in results_map:
                        results_map[res[constants.FIVE_G.DU]][res[constants.FIVE_G.DIRECTION]] = res

                for du in du_names:
                    fname = constants.FIVE_G.NAME_MAPPING.get(du, du)
                    row[f"{fname}_{constants.FIVE_G.SIGNAL_STRENGTH}"] = signal_strength
                    row[f"{fname}_{constants.FIVE_G.CPU_LIMIT}"] = current_cpu
                    row[f"{fname}_{constants.FIVE_G.MEMORY_LIMIT}"] = memory_limit_gb
                    row[f"{fname}_{constants.FIVE_G.LOAD_UPLINK}"] = load if run_uplink else 0.0
                    row[f"{fname}_{constants.FIVE_G.LOAD_DOWNLINK}"] = load if run_downlink else 0.0
                    row[f"{fname}_{constants.FIVE_G.BANDWIDTH}"] = 5
                    row[f"{fname}_{constants.FIVE_G.NUMBER_OF_ANTENNAS}"] = 1

                    if run_uplink and results_map[du][constants.FIVE_G.UPLINK]:
                        res = results_map[du][constants.FIVE_G.UPLINK]
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.UPLINK}_"
                            f"{constants.FIVE_G.JITTER_MS}"] = res[constants.FIVE_G.JITTER_MS]
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.UPLINK}_"
                            f"{constants.FIVE_G.THROUGHPUT_BPS}"] = res[constants.FIVE_G.THROUGHPUT_BPS]
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.UPLINK}_"
                            f"{constants.FIVE_G.LOST_PERCENT}"] = res[constants.FIVE_G.LOST_PERCENT]
                    else:
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.UPLINK}_"
                            f"{constants.FIVE_G.JITTER_MS}"] = 0.0
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.UPLINK}_"
                            f"{constants.FIVE_G.THROUGHPUT_BPS}"] = 0.0
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.UPLINK}_"
                            f"{constants.FIVE_G.LOST_PERCENT}"] = 0.0

                    if run_downlink and results_map[du][constants.FIVE_G.DOWNLINK]:
                        res = results_map[du][constants.FIVE_G.DOWNLINK]
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.DOWNLINK}_"
                            f"{constants.FIVE_G.JITTER_MS}"] = res[constants.FIVE_G.JITTER_MS]
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.DOWNLINK}_"
                            f"{constants.FIVE_G.THROUGHPUT_BPS}"] = res[constants.FIVE_G.THROUGHPUT_BPS]
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.DOWNLINK}_"
                            f"{constants.FIVE_G.LOST_PERCENT}"] = res[constants.FIVE_G.LOST_PERCENT]
                    else:
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.DOWNLINK}_"
                            f"{constants.FIVE_G.JITTER_MS}"] = 0.0
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.DOWNLINK}_"
                            f"{constants.FIVE_G.THROUGHPUT_BPS}"] = 0.0
                        row[f"{fname}_{constants.FIVE_G.E2E}_{constants.FIVE_G.DOWNLINK}_"
                            f"{constants.FIVE_G.LOST_PERCENT}"] = 0.0

                    row[f"{fname}_{constants.FIVE_G.MAC_LAYER_PROCESSING_LATENCY_US}"] = safe_mean(
                        [x.average_latency_us for x in time_series.five_g_du_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.MAC_LAYER_CPU_USAGE_PERCENT}"] = safe_mean(
                        [x.cpu_usage_percent for x in time_series.five_g_du_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_UPLINK_CPU_USAGE_PERCENT}"] = safe_mean(
                        [x.ul_cpu_usage_percent for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_DOWNLINK_CPU_USAGE_PERCENT}"] = safe_mean(
                        [x.dl_cpu_usage_percent for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_DOWNLINK_PROCESSING_LATENCY_US}"] = safe_mean(
                        [x.dl_avg_latency_us for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_UPLINK_PROCESSING_LATENCY_US}"] = safe_mean(
                        [x.ul_avg_latency_us for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_SNR_UPLINK_DB}"] = safe_mean(
                        [x.ul_sinr_db for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_CHANNEL_ESTIMATION_LATENCY_US}"] = safe_mean(
                        [x.ul_ch_est_latency_us for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_UPLINK_THROUGHPUT_MBPS}"] = safe_mean(
                        [x.ul_fec_tput_mbps for x in time_series.five_g_du_low_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.PHYSICAL_LAYER_DOWNLINK_THROUGHPUT_MBPS}"] = safe_mean(
                        [x.dl_fec_tput_mbps for x in time_series.five_g_du_low_metrics[du]])

                    rlc_latencies = []
                    for m in time_series.five_g_du_rlc_metrics[du]:
                        if m.rx_num_pdus > 0:
                            rlc_latencies.append(m.tx_sum_pdu_latency_ns / m.rx_num_pdus)
                    row[f"{fname}_{constants.FIVE_G.RLC_CREATING_PDU_LATENCY_NS}"] = safe_mean(rlc_latencies)

                    row[f"{fname}_{constants.FIVE_G.CELL_SCHEDULING_PROCESSING_LATENCY_MS}"] = safe_mean(
                        [x.average_latency for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.CELL_DOWNLINK_BITRATE_BPS}"] = safe_mean(
                        [x.dl_brate for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.CELL_UPLINK_BITRATE_BPS}"] = safe_mean(
                        [x.ul_brate for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.CELL_MODULATION_AND_CODING_SCHEME_DOWNLINK}"] = safe_mean(
                        [x.dl_mcs for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.CELL_MODULATION_AND_CODING_SCHEME_UPLINK}"] = safe_mean(
                        [x.ul_mcs for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.CELL_BLOCK_ERROR_RATE_PERCENT_DOWNLINK}"] = safe_mean(
                        [x.dl_bler for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.CELL_BLOCK_ERROR_RATE_PERCENT_UPLINK}"] = safe_mean(
                        [x.ul_bler for x in time_series.five_g_du_cell_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.CPU_USAGE_PERCENT}"] = safe_mean(
                        [x.cpu_usage_percent for x in time_series.five_g_du_app_resource_usage_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.MEMORY_USAGE_MB}"] = safe_mean(
                        [x.memory_usage_mb for x in time_series.five_g_du_app_resource_usage_metrics[du]])
                    row[f"{fname}_{constants.FIVE_G.POWER_CONSUMPTION_WATTS}"] = safe_mean(
                        [x.power_consumption_watts for x in time_series.five_g_du_app_resource_usage_metrics[du]])

                for cu in cu_names:
                    fname = constants.FIVE_G.NAME_MAPPING.get(cu, cu)
                    row[f"{fname}_{constants.FIVE_G.SIGNAL_STRENGTH}"] = signal_strength
                    row[f"{fname}_{constants.FIVE_G.CPU_LIMIT}"] = current_cpu
                    row[f"{fname}_{constants.FIVE_G.MEMORY_LIMIT}"] = memory_limit_gb
                    row[f"{fname}_{constants.FIVE_G.CPU_USAGE_PERCENT}"] = safe_mean(
                        [x.cpu_usage_percent for x in time_series.five_g_cu_app_resource_usage_metrics[cu]])
                    row[f"{fname}_{constants.FIVE_G.MEMORY_USAGE_MB}"] = safe_mean(
                        [x.memory_usage_mb for x in time_series.five_g_cu_app_resource_usage_metrics[cu]])
                    row[f"{fname}_{constants.FIVE_G.POWER_CONSUMPTION_WATTS}"] = safe_mean(
                        [x.power_consumption_watts for x in time_series.five_g_cu_app_resource_usage_metrics[cu]])

                append_to_csv(row, output_csv_path, csv_headers)

    print("\n--- All Experiments Complete. ---")


if __name__ == '__main__':
    run()
