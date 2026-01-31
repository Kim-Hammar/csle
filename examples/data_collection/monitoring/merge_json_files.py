import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    files = [
        "/home/kim/five_g_uplink_statistics_old.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_1_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_2_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_3_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_4_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_5_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_6_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_7_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_8_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_9_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_0_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_1_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_2_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_3_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_4_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_5_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_6_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_7_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_8_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_9_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_3_0_gain_20_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_5_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_6_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_7_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_8_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_1_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_1_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_2_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_3_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_4_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_5_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_6_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_7_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_8_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_9_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_0_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_1_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_2_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_3_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_4_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_5_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_6_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_7_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_8_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_9_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_3_0_gain_30_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_5_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_6_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_7_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_8_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_9_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_0_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_1_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_2_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_3_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_4_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_5_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_6_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_7_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_8_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_9_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_0_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_1_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_2_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_3_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_4_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_5_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_6_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_7_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_8_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_9_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_3_0_gain_40_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_5_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_6_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_7_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_8_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_0_9_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_2_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_3_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_4_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_5_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_6_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_7_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_8_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_1_9_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_0_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_1_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_2_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_3_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_4_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_5_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_6_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_7_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_8_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_2_9_gain_50_memory_20.json",
        "/home/kim/five_g_statistics_uplink_cpu_3_0_gain_50_memory_20.json"
    ]
    # This will hold the combined data
    merged_statistics = {}

    for file_path in files:
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found. Skipping.")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Initialize the merged_statistics structure based on the first file's keys
        if not merged_statistics:
            merged_statistics = data
            continue

        # For subsequent files, append the lists to the existing keys
        # 1. Merge top-level lists (load, signal_strength, etc.)
        for key in ["load", "signal_strength", "cpu_limit", "memory_limit"]:
            if key in data:
                merged_statistics[key].extend(data[key])

        # 2. Merge DU and CU specific metrics
        # We look for keys that were initialized in the first file (e.g., DU/CU names)
        for entity_name, metrics in data.items():
            if isinstance(metrics, dict) and entity_name in merged_statistics:
                for metric_name, values in metrics.items():
                    if metric_name in merged_statistics[entity_name]:
                        merged_statistics[entity_name][metric_name].extend(values)

    # Save the consolidated data
    output_file = "/home/kim/five_g_uplink_statistics_old_2.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_statistics, f, indent=4, sort_keys=True)

    print(f"Successfully merged {len(files)} files into {output_file}")