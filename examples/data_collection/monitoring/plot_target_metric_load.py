import json
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Load the merged data
    # file_path = "/home/kim/five_g_uplink_statistics.json"
    file_path = "/home/kim/merged_five_g_statistics.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        merged_statistics = json.load(f)

    # --- 1. FILTER CONFIGURATION ---
    # Set your specific experimental constraints here
    SPECIFIC_CPU_LIMIT = 2.5
    SPECIFIC_SIGNAL_STRENGTH = 10
    SPECIFIC_MEMORY_LIMIT = 20.0

    TARGET_DU = "csle_cloud_ran_du_1_1-level17-15"
    # TARGET_DU = "csle_cloud_ran_cu_1_1-level17-15"
    TARGET_METRIC = "e2e_uplink_lost_percent"
    # TARGET_METRIC = "e2e_uplink_jitter_ms"
    # TARGET_METRIC = "du_mac_layer_processing_latency_us"
    # TARGET_METRIC = "du_physical_layer_downlink_processing_latency_us"
    # TARGET_METRIC = "du_physical_layer_uplink_processing_latency_us"
    # TARGET_METRIC = "du_cpu_usage_percent"
    # TARGET_METRIC = "e2e_uplink_throughput_bps"
    # TARGET_METRIC = "du_physical_layer_snr_uplink_db"
    # TARGET_METRIC = "du_physical_layer_channel_estimation_latency_us"
    # TARGET_METRIC = "du_physical_layer_uplink_throughput_mbps"
    # TARGET_METRIC = "du_physical_layer_downlink_throughput_mbps"
    # TARGET_METRIC = "du_rlc_creating_pdu_latency_ns"
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

    # --- 2. DATA CONVERSION ---
    rows = []
    num_samples = len(merged_statistics["load"])

    for i in range(num_samples):
        row = {
            "load": merged_statistics["load"][i],
            "cpu_limit": merged_statistics["cpu_limit"][i],
            "signal_strength": merged_statistics["signal_strength"][i],
            "memory_limit": merged_statistics["memory_limit"][i]
        }
        # Add metrics for the target DU
        if TARGET_DU in merged_statistics:
            values = merged_statistics[TARGET_DU].get(TARGET_METRIC, [])
            # test = merged_statistics[TARGET_DU].get("du_physical_layer_downlink_cpu_usage_percent", [])
            if i < len(values):
                row[TARGET_METRIC] = values[i]
                #/(1000000)
        rows.append(row)

    df = pd.DataFrame(rows)

    # --- 3. FILTERING ---
    # Slicing the dataframe to match your specific parameters
    filtered_df = df[
        (df["cpu_limit"] == SPECIFIC_CPU_LIMIT) &
        (df["signal_strength"] == SPECIFIC_SIGNAL_STRENGTH) &
        (df["memory_limit"] == SPECIFIC_MEMORY_LIMIT)
        ]

    if filtered_df.empty:
        print(f"Error: No data found for CPU={SPECIFIC_CPU_LIMIT}, "
              f"Signal={SPECIFIC_SIGNAL_STRENGTH}, Memory={SPECIFIC_MEMORY_LIMIT}")
    else:
        # --- 4. AGGREGATION ---
        # Group by load to average the 5 samples per load level
        summary = filtered_df.groupby("load")[TARGET_METRIC].agg(["mean", "std"]).reset_index()
        summary = summary.sort_values("load")

        # --- 5. PLOTTING ---
        plt.figure(figsize=(10, 6))

        # Main Trend
        plt.plot(summary["load"], summary["mean"], marker='o', color='teal',
                 linestyle='-', linewidth=2, label=f"Mean (CPU: {SPECIFIC_CPU_LIMIT})")

        # Variance Shading
        plt.fill_between(
            summary["load"],
            summary["mean"] - summary["std"],
            summary["mean"] + summary["std"],
            color='teal', alpha=0.2, label="Std Dev (Across Samples)"
        )

        # Formatting
        plt.title(f"{TARGET_METRIC.replace('_', ' ').title()} vs. Load\n"
                  f"(CPU: {SPECIFIC_CPU_LIMIT}, Signal: {SPECIFIC_SIGNAL_STRENGTH}dB, DU: {TARGET_DU})",
                  fontsize=12)
        plt.xlabel("Offered Load (Mbit/s)", fontsize=11)
        plt.ylabel(TARGET_METRIC.replace("_", " ").title(), fontsize=11)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.legend()

        plt.tight_layout()
        plt.show()

        print(f"Plot complete for CPU {SPECIFIC_CPU_LIMIT}. "
              f"Total data points used: {len(filtered_df)}")

        # print(summary["load"].values)
        for i in range(len(summary["load"].values)):
            print(f"{summary['load'].values[i]} {summary['mean'].values[i]} "
                  f"{summary['mean'].values[i] - summary['std'].values[i]} "
                  f"{summary['mean'].values[i] + summary['std'].values[i]}")
            # print(f"{summary['load'].values[i]} {summary['load'].values[i]*((1-summary['mean'].values[i]/100))} "
            #       f"{summary['load'].values[i]*((1-(summary['mean'].values[i]/100-summary['std'].values[i]/100)))} "
            #       f"{summary['load'].values[i]*((1-(summary['mean'].values[i]/100+summary['std'].values[i]/100)))} ")