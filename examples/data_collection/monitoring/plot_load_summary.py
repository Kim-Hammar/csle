import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # Load the merged data
    # Ensure the path matches your environment
    file_path = "/home/kim/five_g_statistics_merged.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        merged_statistics = json.load(f)

    # --- 1. CONFIGURATION ---
    # Change these variables to plot different DUs or Metrics
    TARGET_DU = "csle_cloud_ran_du_1_1-level17-15"
    # TARGET_METRIC = "e2e_lost_percent"
    # TARGET_METRIC = "e2e_jitter_ms"
    # TARGET_METRIC = "du_mac_layer_processing_latency_us"
    # TARGET_METRIC = "du_physical_layer_downlink_processing_latency_us"
    # TARGET_METRIC = "du_physical_layer_uplink_processing_latency_us"
    # TARGET_METRIC = "du_cpu_usage_percent"
    # TARGET_METRIC = "e2e_throughput_bps"
    TARGET_METRIC = "du_physical_layer_snr_uplink_db"
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
    # Examples: "e2e_throughput_bps", "du_cpu_usage_percent", "e2e_power_consumption_watts"

    # --- 2. DATA CONVERSION ---
    # Flatten the merged_statistics into a DataFrame
    rows = []
    num_samples = len(merged_statistics["load"])

    for i in range(num_samples):
        row = {
            "load": merged_statistics["load"][i],
            "cpu_limit": merged_statistics["cpu_limit"][i]
        }
        # Add metrics for the target DU
        if TARGET_DU in merged_statistics:
            for metric_name, values in merged_statistics[TARGET_DU].items():
                # Safety check for list length
                if i < len(values):
                    row[metric_name] = values[i]
        rows.append(row)

    df = pd.DataFrame(rows)

    # --- 3. AGGREGATION ---
    # Here we group by 'load' instead of 'cpu_limit'
    # This averages results across all CPU limits for each load level
    summary = df.groupby("load")[TARGET_METRIC].agg(["mean", "std"]).reset_index()
    summary = summary.sort_values("load")

    # --- 4. PLOTTING ---
    plt.figure(figsize=(10, 6))

    # Plot the main trend line
    plt.plot(summary["load"], summary["mean"], marker='s', color='red', linestyle='-', linewidth=2, label="Mean")

    # Shaded area for variance
    plt.fill_between(
        summary["load"],
        summary["mean"] - summary["std"],
        summary["mean"] + summary["std"],
        color='red',
        alpha=0.15,
        label="Std Dev"
    )

    # Formatting
    plt.title(f"Impact of Load on {TARGET_METRIC.replace('_', ' ').title()}\n(DU: {TARGET_DU})", fontsize=14)
    plt.xlabel("Offered Load (Mbit/s)", fontsize=12)
    plt.ylabel(TARGET_METRIC.replace("_", " ").title(), fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()

    # Save and show
    plt.tight_layout()
    plt.savefig(f"{TARGET_METRIC}_vs_load.png")
    plt.show()

    print(f"Plot generated for {TARGET_METRIC} vs Load.")
    print(summary.round(3))