import json
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # file_path = "/home/kim/merged_five_g_statistics.json"
    file_path = "/home/kim/five_g_downlink_statistics.json"
    # file_path = "/home/kim/five_g_uplink_statistics.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        merged_statistics = json.load(f)

    SPECIFIC_CPU_LIMIT = 2.5
    SPECIFIC_SIGNAL_STRENGTH = 10
    SPECIFIC_MEMORY_LIMIT = 20.0
    TARGET_DU = "csle_cloud_ran_du_1_1-level17-15"
    # TARGET_DU = "csle_cloud_ran_cu_1_1-level17-15"
    # TARGET_METRIC = "e2e_uplink_lost_percent"
    # TARGET_METRIC = "e2e_downlink_lost_percent"
    # TARGET_METRIC = "e2e_uplink_jitter_ms"
    # TARGET_METRIC = "e2e_downlink_jitter_ms"
    # TARGET_METRIC = "du_mac_layer_processing_latency_us"
    # TARGET_METRIC = "du_physical_layer_downlink_processing_latency_us"
    # TARGET_METRIC = "du_physical_layer_uplink_processing_latency_us"
    # TARGET_METRIC = "du_cpu_usage_percent"
    # TARGET_METRIC = "e2e_uplink_throughput_bps"
    # TARGET_METRIC = "du_physical_layer_snr_uplink_db"
    # TARGET_METRIC = "du_physical_layer_channel_estimation_latency_us"
    # TARGET_METRIC = "du_physical_layer_uplink_throughput_mbps"
    # TARGET_METRIC = "du_physical_layer_downlink_throughput_mbps"
    TARGET_METRIC = "du_rlc_creating_pdu_latency_ns"
    # TARGET_METRIC = "du_cell_scheduling_processing_latency_ms"
    # TARGET_METRIC = "du_cell_downlink_bitrate_bps"
    # TARGET_METRIC = "du_cell_uplink_bitrate_bps"
    # TARGET_METRIC = "du_cell_modulation_and_coding_scheme_downlink"
    # TARGET_METRIC = "du_cell_modulation_and_coding_scheme_uplink"
    # TARGET_METRIC = "du_cell_block_error_rate_percent_downlink"
    # TARGET_METRIC = "du_cell_block_error_rate_percent_uplink"
    # TARGET_METRIC = "du_memory_usage_mb"
    # TARGET_METRIC = "du_power_consumption_watts"
    # TARGET_METRIC = "cu_power_consumption_watts"
    # TARGET_METRIC = "cu_cpu_usage_percent"
    # TARGET_METRIC = "cu_memory_usage_mb"
    # TARGET_METRIC = "du_mac_layer_cpu_usage_percent"
    # TARGET_METRIC = "du_physical_layer_uplink_cpu_usage_percent"
    # TARGET_METRIC = "du_physical_layer_downlink_cpu_usage_percent"

    rows = []
    num_samples = len(merged_statistics["load"])

    # Get the list of metric values for the target DU
    du_metrics = merged_statistics.get(TARGET_DU, {})
    metric_values = du_metrics.get(TARGET_METRIC, [])

    for i in range(num_samples):
        # We only care about rows where the target metric actually has a value
        # This skips the 'Uplink' half of the file when plotting 'Downlink' metrics
        if i < len(metric_values) and metric_values[i] is not None:
            row = {
                "load": merged_statistics["load"][i],
                "cpu_limit": merged_statistics["cpu_limit"][i],
                "signal_strength": merged_statistics["signal_strength"][i],
                "memory_limit": merged_statistics["memory_limit"][i],
                TARGET_METRIC: metric_values[i]/1000
            }
            rows.append(row)

    df = pd.DataFrame(rows)

    if df.empty:
        print("Error: No rows created. Check if TARGET_METRIC exists in the JSON.")
        exit()

    filtered_df = df[
        (df["cpu_limit"] == SPECIFIC_CPU_LIMIT) &
        (df["signal_strength"] == SPECIFIC_SIGNAL_STRENGTH) &
        (df["memory_limit"] == SPECIFIC_MEMORY_LIMIT)
        ].dropna(subset=[TARGET_METRIC])  # Ensure we drop any remaining NaNs

    if filtered_df.empty:
        print(f"Error: No data found for CPU={SPECIFIC_CPU_LIMIT} and metric={TARGET_METRIC}")
    else:
        summary = filtered_df.groupby("load")[TARGET_METRIC].agg(["mean", "std"]).reset_index()
        summary = summary.sort_values("load")

        plt.figure(figsize=(10, 6))
        plt.plot(summary["load"], summary["mean"], marker='o', color='teal', label=f"Mean")
        plt.fill_between(summary["load"], summary["mean"] - summary["std"],
                         summary["mean"] + summary["std"], color='teal', alpha=0.2)

        plt.title(f"{TARGET_METRIC.replace('_', ' ').title()} vs. Load")
        plt.xlabel("Offered Load (Mbit/s)")
        plt.ylabel(TARGET_METRIC.replace("_", " "))
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.show()

        print(f"Plot complete. Data points used: {len(filtered_df)}")

        for i in range(len(summary["load"].values)):
            val = summary['mean'].values[i]
            # if summary['load'].values[i] >= 6:
            #     val=val*1.15
            print(f"{summary['load'].values[i]} {val} "
                  f"{val - summary['std'].values[i]} "
                  f"{val + summary['std'].values[i]}")
            # print(f"{summary['load'].values[i]} {summary['load'].values[i]*((1-summary['mean'].values[i]/100))} "
            #       f"{summary['load'].values[i]*((1-(summary['mean'].values[i]/100-summary['std'].values[i]/100)))} "
            #       f"{summary['load'].values[i]*((1-(summary['mean'].values[i]/100+summary['std'].values[i]/100)))} ")