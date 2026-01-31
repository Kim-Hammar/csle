import pandas as pd
import os


def transform_csv(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    print(f"Reading: {input_path}")
    df = pd.read_csv(input_path)

    # 1. Rename static top-level columns
    df.rename(columns={"routing_config": "R"}, inplace=True)

    # Define Node Ranges
    du_nodes = ["DU1", "DU2", "DU3", "DU4"]
    cu_nodes = ["CU1", "CU2"]

    # --- COMPUTATIONS ---
    print("Performing computations...")

    for du in du_nodes:
        # DUi-CL = DUi-L * (1 - loss/100)
        loss_uplink = df.get(f"{du}_e2e_uplink_lost_percent", 0)
        df[f"{du}-CL"] = df[f"{du}_load_uplink"] * (1 - (loss_uplink / 100.0))

        # DUi-CLD = DUi-LD * (1 - loss/100)
        loss_downlink = df.get(f"{du}_e2e_downlink_lost_percent", 0)
        df[f"{du}-CLD"] = df[f"{du}_load_downlink"] * (1 - (loss_downlink / 100.0))

        # DUi-D = MAC + PHY_UL + Cell_Sched (ms->us)
        # Note: 'du_' prefix was stripped in previous steps, so we look for 'mac_layer...'
        mac_lat = df.get(f"{du}_mac_layer_processing_latency_us", 0)
        phy_ul_lat = df.get(f"{du}_physical_layer_uplink_processing_latency_us", 0)
        sched_lat_ms = df.get(f"{du}_cell_scheduling_processing_latency_ms", 0)

        df[f"{du}-D"] = mac_lat + phy_ul_lat + (sched_lat_ms * 1000.0)

        # DUi-DD = MAC + PHY_DL + Cell_Sched (ms->us)
        phy_dl_lat = df.get(f"{du}_physical_layer_downlink_processing_latency_us", 0)
        df[f"{du}-DD"] = mac_lat + phy_dl_lat + (sched_lat_ms * 1000.0)

        # DUi-MCS = Avg(MCS_DL, MCS_UL)
        mcs_dl = df.get(f"{du}_cell_modulation_and_coding_scheme_downlink", 0)
        mcs_ul = df.get(f"{du}_cell_modulation_and_coding_scheme_uplink", 0)
        df[f"{du}-MCS"] = (mcs_dl + mcs_ul) / 2.0

        # DUi-BER = Avg(BER_DL, BER_UL)
        ber_dl = df.get(f"{du}_cell_block_error_rate_percent_downlink", 0)
        ber_ul = df.get(f"{du}_cell_block_error_rate_percent_uplink", 0)
        df[f"{du}-BER"] = (ber_dl + ber_ul) / 2.0

        # --- UPDATE 1: CONVERT CELL BITRATE BPS TO MBPS ---
        df[f"{du}-TD"] = df.get(f"{du}_cell_downlink_bitrate_bps", 0) / 1_000_000.0
        df[f"{du}-T"] = df.get(f"{du}_cell_uplink_bitrate_bps", 0) / 1_000_000.0

        # --- UPDATE 2: CONVERT E2E THROUGHPUT BPS TO MBPS ---
        df[f"{du}-ETD"] = (df.get(f"{du}_e2e_downlink_throughput_bps", 0) / 1_000_000.0)* (1 - (loss_downlink / 100.0))
        df[f"{du}-ET"] = (df.get(f"{du}_e2e_uplink_throughput_bps", 0) / 1_000_000.0)* (1 - (loss_uplink / 100.0))

    # CUj-D = DUi_mac_layer_processing_latency_us / 5
    if f"DU1_mac_layer_processing_latency_us" in df.columns:
        df["CU1-D"] = df["DU1_mac_layer_processing_latency_us"] / 5.0

    if f"DU3_mac_layer_processing_latency_us" in df.columns:
        df["CU2-D"] = df["DU3_mac_layer_processing_latency_us"] / 5.0

    # --- RENAMING ---
    print("Renaming columns...")

    final_rename_map = {}

    # DUs
    for du in du_nodes:
        # Jitter remains in ms (no division)
        final_rename_map[f"{du}_e2e_downlink_jitter_ms"] = f"{du}-JD"
        final_rename_map[f"{du}_e2e_uplink_jitter_ms"] = f"{du}-J"

        # Throughputs (ET, ETD, T, TD) are computed manually above, so we exclude them from rename map

        # Physical Layer SNR
        final_rename_map[f"{du}_physical_layer_snr_uplink_db"] = f"{du}-SNR"

        # Configs
        final_rename_map[f"{du}_cpu_limit"] = f"{du}-C"
        final_rename_map[f"{du}_memory_limit"] = f"{du}-M"
        final_rename_map[f"{du}_load_downlink"] = f"{du}-LD"
        final_rename_map[f"{du}_load_uplink"] = f"{du}-L"

        # Usage
        final_rename_map[f"{du}_cpu_usage_percent"] = f"{du}-CU"
        final_rename_map[f"{du}_memory_usage_mb"] = f"{du}-MU"
        final_rename_map[f"{du}_power_consumption_watts"] = f"{du}-P"

        # Static/Config
        final_rename_map[f"{du}_bandwidth"] = f"{du}-B"
        final_rename_map[f"{du}_signal_strength"] = f"{du}-G"

    # CUs
    for cu in cu_nodes:
        final_rename_map[f"{cu}_power_consumption_watts"] = f"{cu}-P"
        final_rename_map[f"{cu}_cpu_usage_percent"] = f"{cu}-CU"
        final_rename_map[f"{cu}_memory_usage_mb"] = f"{cu}-MU"
        final_rename_map[f"{cu}_cpu_limit"] = f"{cu}-C"
        final_rename_map[f"{cu}_memory_limit"] = f"{cu}-M"

    df.rename(columns=final_rename_map, inplace=True)

    # --- FILTERING ---
    keep_cols = ["R"]

    # Add DU columns (22 per DU)
    for du in du_nodes:
        keep_cols.extend([
            f"{du}-JD", f"{du}-ETD", f"{du}-J", f"{du}-ET", f"{du}-SNR",
            f"{du}-C", f"{du}-M", f"{du}-LD", f"{du}-L", f"{du}-CU", f"{du}-MU", f"{du}-P",
            f"{du}-TD", f"{du}-T", f"{du}-B", f"{du}-G",
            f"{du}-CL", f"{du}-CLD", f"{du}-D", f"{du}-DD", f"{du}-MCS", f"{du}-BER"
        ])

    # Add CU columns (6 per CU)
    for cu in cu_nodes:
        keep_cols.extend([
            f"{cu}-P", f"{cu}-CU", f"{cu}-MU", f"{cu}-C", f"{cu}-M", f"{cu}-D"
        ])

    # Filter columns
    existing_cols = [c for c in keep_cols if c in df.columns]

    missing = set(keep_cols) - set(existing_cols)
    if missing:
        print(f"Warning: The following columns are still missing: {missing}")
    else:
        print(f"Success: All {len(keep_cols)} expected columns are present.")

    df_final = df[existing_cols]

    print(f"Writing transformed data to: {output_path}")
    print(f"Final shape: {df_final.shape}")
    df_final.to_csv(output_path, index=False)


if __name__ == "__main__":
    input_csv = "/home/kim/five_g_merged_dataset_new_2.csv"
    output_csv = "/home/kim/five_g_final_transformed_2.csv"

    transform_csv(input_csv, output_csv)