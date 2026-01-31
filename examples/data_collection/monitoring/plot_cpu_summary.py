import json
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    with open("/home/kim/five_g_statistics_merged.json", 'r', encoding='utf-8') as f:
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
    TARGET_METRIC = "du_power_consumption_watts"

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
                row[metric_name] = values[i]
        rows.append(row)

    df = pd.DataFrame(rows)

    # --- 3. AGGREGATION ---
    # We group by cpu_limit to get the mean and standard deviation across all samples/loads
    # This gives a clearer trend line
    summary = df.groupby("cpu_limit")[TARGET_METRIC].agg(["mean", "std"]).reset_index()
    summary = summary.sort_values("cpu_limit")  # Ensure the X-axis is ordered

    # --- 4. PLOTTING ---
    plt.figure(figsize=(10, 6))

    # Plot the main trend line
    plt.plot(summary["cpu_limit"], summary["mean"], marker='o', linestyle='-', linewidth=2, label="Mean")

    # Add a shaded area for standard deviation (shows variance/instability)
    plt.fill_between(
        summary["cpu_limit"],
        summary["mean"] - summary["std"],
        summary["mean"] + summary["std"],
        alpha=0.2,
        label="Std Dev"
    )

    # Formatting
    plt.title(f"Impact of CPU Limit on {TARGET_METRIC}\n(DU: {TARGET_DU})", fontsize=14)
    plt.xlabel("CPU Limit (Cores)", fontsize=12)
    plt.ylabel(TARGET_METRIC.replace("_", " ").title(), fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Save and show
    plt.tight_layout()
    # plt.savefig(f"{TARGET_METRIC}_vs_cpu.png")
    plt.show()

    print(f"Plot generated for {TARGET_METRIC}. Summary data:")
    print(summary)