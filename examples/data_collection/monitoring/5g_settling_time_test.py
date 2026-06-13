import subprocess
import json
import time
import os
import csv
import math
import logging
from typing import List, Dict, Any, Callable, Tuple
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.five_g_du_controller import FiveGDUController
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


def run_iperf(du_name: str, port: int, load: int, direction: str, duration: int) -> Dict[str, Any]:
    """
    Generates load with iperf for a given DU container for a fixed duration.

    :param du_name: the name of the DU container
    :param port: the port number for iperf
    :param load: the load in Mbps
    :param direction: the direction of traffic ("uplink" or "downlink")
    :param duration: the duration of the iperf test in seconds
    :return: a dictionary containing iperf results including jitter, throughput, and packet loss
    """
    iperf_cmd = constants.COMMANDS.IPERF_COMMAND.format(constants.FIVE_G.CORE_IP, load, duration, port)
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
            constants.FIVE_G.THROUGHPUT_BPS: float(sum_data[constants.FIVE_G.BITS_PER_SECOND_KEY]),
            constants.FIVE_G.STATUS: constants.FIVE_G.SUCCESS
        }
    except Exception as e:
        return {
            constants.FIVE_G.DU: du_name,
            constants.FIVE_G.DIRECTION: direction,
            constants.FIVE_G.STATUS: f"Error: {str(e)}",
            constants.FIVE_G.THROUGHPUT_BPS: 0.0
        }


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


def set_du_monitor_interval(execution: Any, du_ip: str, interval: int, logger: logging.Logger) -> None:
    """
    Restarts the 5G DU monitor thread on a given DU container with a custom Kafka push interval.

    The monitor thread reads its push cadence from
    emulation_env_config.kafka_config.time_step_len_seconds when it is (re)started, so this
    function updates that field and then stops and starts the monitor thread for the DU.

    :param execution: the emulation execution
    :param du_ip: the docker gateway bridge IP of the DU container
    :param interval: the desired metric push interval in seconds
    :param logger: the logger to use for logging
    :return: None
    """
    emulation_env_config = execution.emulation_env_config
    emulation_env_config.kafka_config.time_step_len_seconds = interval
    FiveGDUController.stop_five_g_du_monitor_thread(emulation_env_config=emulation_env_config, ip=du_ip, logger=logger)
    time.sleep(2)
    FiveGDUController.start_five_g_du_monitor_thread(emulation_env_config=emulation_env_config, ip=du_ip, logger=logger)
    print(f"Restarted DU monitor on {du_ip} with a {interval}s push interval")


def compute_settling_time(per_l_means: Dict[int, float], delta: float,
                          steady_tail_ls: List[int]) -> Tuple[float, float]:
    """
    Computes the settling time for a single metric from its expected value per time unit.

    The steady-state value U^a is estimated as the mean of E{U_l} over the tail time units.
    The settling time is the smallest l0 >= 0 such that |E{U_l} - U^a| <= delta * |U^a| for all
    l >= l0.

    :param per_l_means: mapping from relative time unit l (>= 0) to E{U_l}
    :param delta: the settling tolerance (e.g., 0.02)
    :param steady_tail_ls: the list of time units l used to estimate the steady-state value U^a
    :return: a tuple (tau, u_steady) where tau is the settling time (NaN if never settles)
    """
    ls = sorted(l for l in per_l_means.keys() if l >= 0)
    if not ls:
        return float("nan"), float("nan")
    tail_vals = [per_l_means[l] for l in steady_tail_ls if l in per_l_means]
    u_steady = float(np.mean(tail_vals)) if tail_vals else per_l_means[ls[-1]]
    band = delta * abs(u_steady)
    tau = float("nan")
    # Scan from the last time unit backwards to find the smallest l0 after which we stay in band
    for i, l in enumerate(ls):
        if all(abs(per_l_means[lj] - u_steady) <= band for lj in ls[i:]):
            tau = float(l)
            break
    return tau, u_steady


def collect_timeseries(execution: Any, du_name: str, output_csv: str, fieldnames: List[str],
                       metrics: List[Tuple[str, Callable[[Any], float]]], scenarios: List[Tuple[float, float]],
                       num_trials: int, memory_limit_docker: str, offered_load_mbps: int, ul_port: int, dl_port: int,
                       warmup_seconds: int, pre_window_seconds: int, settle_window_seconds: int,
                       sample_interval_seconds: int) -> None:
    """
    Runs the settling-time trials and writes the fine-grained metric time series to CSV.

    For each (from_cpu, to_cpu) scenario and trial, the DU is brought to from_cpu under constant
    load, the CPU limit is changed to to_cpu (the action), and the physical-layer metrics are
    sampled around the action and written to CSV with a relative time unit l.

    The relative time l is derived from the *sample order* and the known push cadence, NOT from the
    sample timestamp: the gRPC transport stores the timestamp as a 32-bit float, which quantizes
    epoch timestamps to ~128s and is therefore useless for sub-minute timing. Since the monitor
    pushes at a fixed cadence and the samples are returned in time order, the last
    settle_window/interval samples correspond to the post-action window (l >= 0) and the preceding
    pre_window/interval samples to the baseline (l < 0).

    :param execution: the emulation execution
    :param du_name: the name of the DU container under test
    :param output_csv: path to the time-series CSV to write
    :param fieldnames: the CSV header
    :param metrics: list of (column_name, accessor) extracting metrics from a FiveGDULowMetrics sample
    :param scenarios: list of (from_cpu, to_cpu) CPU-limit transitions to measure
    :param num_trials: number of trials per scenario
    :param memory_limit_docker: docker memory limit string (e.g., "20g")
    :param offered_load_mbps: constant offered load per direction in Mbps
    :param ul_port: the iperf uplink port
    :param dl_port: the iperf downlink port
    :param warmup_seconds: time to wait at from_cpu before recording the baseline
    :param pre_window_seconds: duration of the baseline window before the action (l < 0)
    :param settle_window_seconds: observation window after the action (l >= 0)
    :param sample_interval_seconds: the metric push cadence in seconds (one sample per interval)
    :return: None
    """
    kafka_host_ip = execution.emulation_env_config.kafka_config.container.physical_host_ip
    load_duration = warmup_seconds + pre_window_seconds + settle_window_seconds + 10
    read_minutes = math.ceil((pre_window_seconds + settle_window_seconds + 30) / 60) + 1
    n_pre = max(1, round(pre_window_seconds / sample_interval_seconds))
    n_post = max(1, round(settle_window_seconds / sample_interval_seconds))

    for from_cpu, to_cpu in scenarios:
        for trial in range(num_trials):
            print(f"\n--- Scenario {from_cpu}->{to_cpu} cores, trial {trial + 1}/{num_trials} ---")
            set_docker_cpu_limit(from_cpu, memory_limit_docker, [du_name])

            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [
                    executor.submit(run_iperf, du_name, ul_port, offered_load_mbps,
                                    constants.FIVE_G.UPLINK, load_duration),
                    executor.submit(run_iperf, du_name, dl_port, offered_load_mbps,
                                    constants.FIVE_G.DOWNLINK, load_duration),
                ]
                time.sleep(warmup_seconds + pre_window_seconds)
                print(f"Applying action: CPU limit {from_cpu} -> {to_cpu} on {du_name}")
                set_docker_cpu_limit(to_cpu, memory_limit_docker, [du_name])
                time.sleep(settle_window_seconds)
                for f in futures:
                    f.result()

            time_series = ClusterController.get_execution_time_series_data(
                ip=kafka_host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, minutes=read_minutes,
                ip_first_octet=execution.ip_first_octet, emulation=execution.emulation_env_config.name)

            # Samples are returned in time order; the fetch happens right at action + settle_window,
            # so the last n_post samples are the post-action window and the preceding n_pre are the
            # baseline. l = 0 is anchored at the action.
            samples = list(time_series.five_g_du_low_metrics.get(du_name, []))
            if not samples:
                print("WARNING: no samples returned for the DU; skipping trial")
                continue
            tail = samples[-(n_pre + n_post):]
            action_idx = max(0, len(tail) - n_post)
            print(f"Collected {len(tail)} samples in the measurement window (out of {len(samples)} total)")
            for i, m in enumerate(tail):
                row: Dict[str, Any] = {
                    constants.FIVE_G.DU: du_name,
                    "from_cpu": from_cpu,
                    "to_cpu": to_cpu,
                    "trial": trial,
                    "l_seconds": int((i - action_idx) * sample_interval_seconds),
                    "ts": m.ts,
                }
                for col, accessor in metrics:
                    row[col] = float(accessor(m))
                append_to_csv(row, output_csv, fieldnames)


def compute_summary(output_csv: str, summary_csv: str, metrics: List[Tuple[str, Callable[[Any], float]]],
                    scenarios: List[Tuple[float, float]], delta: float, steady_state_tail_secs: int) -> None:
    """
    Computes settling-time summaries from the collected time series and writes them to CSV.

    For each (scenario, metric) it averages over trials to estimate E{U_l} for l >= 0 and
    computes the settling time. It also computes a combined settling time per scenario using the
    infinity-norm over the configured metric vector, matching the settling-time definition.

    :param output_csv: path to the time-series CSV produced by collect_timeseries
    :param summary_csv: path to the settling-time summary CSV to write
    :param metrics: list of (column_name, accessor) for the metrics to summarize
    :param scenarios: list of (from_cpu, to_cpu) CPU-limit transitions
    :param delta: the settling tolerance (e.g., 0.02)
    :param steady_state_tail_secs: the number of seconds at the tail used to estimate U^a
    :return: None
    """
    df = pd.read_csv(output_csv)
    df = df[df["l_seconds"] >= 0]
    summary_fields = ["from_cpu", "to_cpu", "metric", "u_steady", "tau_seconds"]
    metric_cols = [c for c, _ in metrics]

    for from_cpu, to_cpu in scenarios:
        scen = df[(df["from_cpu"] == from_cpu) & (df["to_cpu"] == to_cpu)]
        if scen.empty:
            continue
        max_l = int(scen["l_seconds"].max())
        tail_ls = [l for l in range(max(0, max_l - steady_state_tail_secs + 1), max_l + 1)]

        # Per-metric expected values E{U_l} (mean across trials) and normalized deviations
        per_metric_means: Dict[str, Dict[int, float]] = {}
        per_metric_steady: Dict[str, float] = {}
        for col in metric_cols:
            means = scen.groupby("l_seconds")[col].mean().to_dict()
            means = {int(k): float(v) for k, v in means.items()}
            per_metric_means[col] = means
            tau, u_steady = compute_settling_time(means, delta, tail_ls)
            per_metric_steady[col] = u_steady
            append_to_csv({"from_cpu": from_cpu, "to_cpu": to_cpu, "metric": col,
                           "u_steady": u_steady, "tau_seconds": tau}, summary_csv, summary_fields)

        # Combined settling time over the metric vector using the infinity-norm
        common_ls = sorted(set.intersection(*[set(per_metric_means[c].keys()) for c in metric_cols]))
        u_steady_vec = np.array([per_metric_steady[c] for c in metric_cols])
        steady_norm = float(np.linalg.norm(u_steady_vec, ord=np.inf))
        combined_tau = float("nan")
        for i, l in enumerate(common_ls):
            settled = True
            for lj in common_ls[i:]:
                dev = np.array([per_metric_means[c][lj] - per_metric_steady[c] for c in metric_cols])
                if float(np.linalg.norm(dev, ord=np.inf)) > delta * steady_norm:
                    settled = False
                    break
            if settled:
                combined_tau = float(l)
                break
        append_to_csv({"from_cpu": from_cpu, "to_cpu": to_cpu, "metric": "combined_inf_norm",
                       "u_steady": steady_norm, "tau_seconds": combined_tau}, summary_csv, summary_fields)
    print(f"Wrote settling-time summary to {summary_csv}")


def run() -> None:
    """
    Runs the 5G CPU-limit settling-time experiment: restarts the DU monitor at a fine sampling
    interval, measures the transient response of physical-layer metrics to CPU-limit changes,
    and computes settling times.

    :return: None
    """
    emulation = "csle-level17-090"
    du_name = constants.FIVE_G.DU_NAMES[0]
    ul_port, dl_port = 5201, 6201
    offered_load_mbps = 8
    memory_limit_docker = "20g"
    scenarios: List[Tuple[float, float]] = [(1.0, 3.0), (3.0, 1.0)]
    num_trials = 5
    sample_interval_seconds = 1
    warmup_seconds = 15
    pre_window_seconds = 10
    settle_window_seconds = 120
    delta = 0.02
    steady_state_tail_secs = 30
    output_csv = "/home/kim/5g_settling_time_timeseries.csv"
    summary_csv = "/home/kim/5g_settling_time_summary.csv"
    metrics: List[Tuple[str, Callable[[Any], float]]] = [
        ("carried_load_ul_mbps", lambda m: m.ul_fec_tput_mbps),
        ("carried_load_dl_mbps", lambda m: m.dl_fec_tput_mbps),
        ("phy_ul_latency_us", lambda m: m.ul_avg_latency_us),
        ("phy_dl_latency_us", lambda m: m.dl_avg_latency_us),
    ]
    fieldnames = ["from_cpu", "to_cpu", "trial", constants.FIVE_G.DU, "l_seconds", "ts"] + [c for c, _ in metrics]

    logger = logging.getLogger("settling_time")
    logging.basicConfig(level=logging.INFO)

    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=emulation)
    if len(executions) == 0:
        raise ValueError(f"There is no execution of an emulation with name: {emulation}")
    execution = executions[0]

    du_container = next((c for c in execution.emulation_env_config.containers_config.containers
                         if du_name in c.get_full_name()), None)
    if du_container is None:
        raise ValueError(f"Could not find the DU container {du_name} in the emulation config")
    du_ip = du_container.docker_gw_bridge_ip

    orig_interval = execution.emulation_env_config.kafka_config.time_step_len_seconds
    print(f"Original DU monitor interval: {orig_interval}s; switching to {sample_interval_seconds}s")
    try:
        set_du_monitor_interval(execution, du_ip, sample_interval_seconds, logger)
        time.sleep(5)
        collect_timeseries(execution=execution, du_name=du_name, output_csv=output_csv, fieldnames=fieldnames,
                           metrics=metrics, scenarios=scenarios, num_trials=num_trials,
                           memory_limit_docker=memory_limit_docker, offered_load_mbps=offered_load_mbps,
                           ul_port=ul_port, dl_port=dl_port, warmup_seconds=warmup_seconds,
                           pre_window_seconds=pre_window_seconds, settle_window_seconds=settle_window_seconds,
                           sample_interval_seconds=sample_interval_seconds)
    finally:
        print(f"Restoring DU monitor interval to {orig_interval}s")
        set_du_monitor_interval(execution, du_ip, orig_interval, logger)

    compute_summary(output_csv=output_csv, summary_csv=summary_csv, metrics=metrics, scenarios=scenarios,
                    delta=delta, steady_state_tail_secs=steady_state_tail_secs)
    print("\n--- Settling-time experiment complete. ---")


if __name__ == '__main__':
    run()
