import json
import os
import csv
import sys


def process_csle_file(filepath):
    """
    Parses a CSLE JSON file and aggregates samples by configuration.
    Returns a list of config objects containing lists of values.
    """
    if not os.path.exists(filepath):
        print(f"Warning: File not found at {filepath}")
        return []

    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if "load" not in data:
        print("Error: 'load' key missing.")
        return []

    # --- MAPPING ---
    name_mapping = {
        "csle_cloud_ran_du_1_1-level17-15": "DU1",
        "csle_cloud_ran_du_1_2-level17-15": "DU2",
        "csle_cloud_ran_du_1_3-level17-15": "DU3",
        "csle_cloud_ran_du_1_4-level17-15": "DU4",
        "csle_cloud_ran_cu_1_1-level17-15": "CU1",
        "csle_cloud_ran_cu_1_2-level17-15": "CU2"
    }

    # 1. Identify Nodes
    original_node_keys = [k for k, v in data.items() if isinstance(v, dict)]
    num_samples = len(data["load"])

    # 2. Detect Direction
    is_uplink = False
    is_downlink = False
    for node in original_node_keys:
        keys = data[node].keys()
        if any("e2e_uplink" in k for k in keys):
            is_uplink = True
            break
        elif any("e2e_downlink" in k for k in keys):
            is_downlink = True
            break

    # Missing metrics to zero-fill
    missing_metrics_map = {}
    if is_uplink:
        missing_metrics_map = {
            "e2e_downlink_jitter_ms": 0.0,
            "e2e_downlink_throughput_bps": 0.0,
            "e2e_downlink_lost_percent": 0.0
        }
    elif is_downlink:
        missing_metrics_map = {
            "e2e_uplink_jitter_ms": 0.0,
            "e2e_uplink_throughput_bps": 0.0,
            "e2e_uplink_lost_percent": 0.0
        }

    # 3. Grouping Dictionary
    grouped_rows = {}

    for i in range(num_samples):
        # Extract Config Signature
        load_val = data["load"][i]
        signal_val = data["signal_strength"][i]
        cpu_val = data["cpu_limit"][i]
        mem_val = data["memory_limit"][i]

        config_key = (load_val, signal_val, cpu_val, mem_val)

        if config_key not in grouped_rows:
            grouped_rows[config_key] = {
                "routing_config": 1,
                "measurements": {}
            }

        current_meas = grouped_rows[config_key]["measurements"]

        # --- PROCESS EACH NODE ---
        for original_key in original_node_keys:
            target_name = name_mapping.get(original_key, original_key)

            def append_metric(metric_name, value):
                flat_key = f"{target_name}_{metric_name}"
                if flat_key not in current_meas:
                    current_meas[flat_key] = []
                current_meas[flat_key].append(value)

            # A. Inject Configs
            for cfg_key, cfg_val in [
                ("signal_strength", signal_val),
                ("cpu_limit", cpu_val),
                ("memory_limit", mem_val)
            ]:
                append_metric(cfg_key, cfg_val)

            # B. Inject Bandwidth/Antennas (DU Only)
            if "DU" in target_name:
                append_metric("bandwidth", 5)
                append_metric("number_of_antennas", 1)

            # C. Inject Load Direction
            val_up = load_val if is_uplink else 0.0
            val_down = 0.0 if is_uplink else load_val

            append_metric("load_uplink", val_up)
            append_metric("load_downlink", val_down)

            # D. Inject File Metrics (Strip Prefixes)
            for metric, values in data[original_key].items():
                if i >= len(values): continue
                val = values[i]

                clean_metric = metric
                if metric.startswith("du_"):
                    clean_metric = metric[3:]
                elif metric.startswith("cu_"):
                    clean_metric = metric[3:]

                append_metric(clean_metric, val)

            # E. Inject Missing E2E (DU Only)
            if "DU" in target_name:
                for missing_key, zero_val in missing_metrics_map.items():
                    append_metric(missing_key, zero_val)

    return list(grouped_rows.values())


def convert_to_flat_rows(grouped_data):
    """
    Expands the grouped lists into individual rows for CSV.
    """
    csv_rows = []

    for group in grouped_data:
        # Base columns
        routing_config = group["routing_config"]
        measurements = group["measurements"]

        # Determine number of samples in this group
        # (Grab length of first list found in measurements)
        if not measurements:
            continue

        first_key = next(iter(measurements))
        num_samples_in_group = len(measurements[first_key])

        # Iterate through samples 0..N
        for i in range(num_samples_in_group):
            row = {
                "routing_config": routing_config
            }

            # Flatten measurements for index i
            for metric_key, values_list in measurements.items():
                if i < len(values_list):
                    row[metric_key] = values_list[i]
                else:
                    row[metric_key] = None  # Should not happen if data is consistent

            csv_rows.append(row)

    return csv_rows


def merge_and_save_csv(uplink_path, downlink_path, output_path):
    # 1. Process files
    grouped_data = []
    grouped_data.extend(process_csle_file(uplink_path))
    grouped_data.extend(process_csle_file(downlink_path))

    # 2. Expand into flat rows
    print("Flattening data structure...")
    flat_rows = convert_to_flat_rows(grouped_data)

    if not flat_rows:
        print("No data found to write.")
        return

    # 3. Write CSV
    print(f"Writing {len(flat_rows)} rows to CSV: {output_path}")

    # Collect all headers from all rows (in case keys differ slightly)
    # We sort them to keep similar keys together
    headers = set()
    for row in flat_rows:
        headers.update(row.keys())

    # Sort headers: routing_config first, then alphabetical
    sorted_headers = sorted(list(headers))
    if "routing_config" in sorted_headers:
        sorted_headers.remove("routing_config")
        sorted_headers.insert(0, "routing_config")

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted_headers)
        writer.writeheader()
        writer.writerows(flat_rows)

    print("Success.")


if __name__ == "__main__":
    # --- UPDATE PATHS HERE ---
    uplink_file = "/home/kim/five_g_uplink_statistics_old_2.json"
    downlink_file = "/home/kim/five_g_downlink_statistics_old_2.json"
    output_file = "/home/kim/five_g_merged_dataset_new_2.csv"

    merge_and_save_csv(uplink_file, downlink_file, output_file)

    # --- VERIFICATION ---
    try:
        import pandas as pd

        if os.path.exists(output_file):
            print("\n--- Pandas DataFrame Preview ---")
            df = pd.read_csv(output_file)
            print(f"Total Rows: {len(df)}")
            print(f"Total Columns: {len(df.columns)}")

            print("\nSample columns:")
            cols = ["routing_config", "DU1_signal_strength", "DU1_load_uplink", "DU1_cpu_usage_percent"]
            present_cols = [c for c in cols if c in df.columns]
            print(df[present_cols].head())
    except ImportError:
        pass