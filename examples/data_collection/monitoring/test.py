import json
import os


def print_unique_combinations(filepath):
    """
    Parses a CSLE statistics JSON file and prints unique combinations
    of Signal Strength, CPU Limit, and Memory Limit.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if required keys exist
        required_keys = ["signal_strength", "cpu_limit", "memory_limit"]
        for key in required_keys:
            if key not in data:
                print(f"Error: Key '{key}' not found in JSON.")
                return

        # Zip the lists together to create rows (tuples), then use set() to find uniques
        # We zip: (signal[0], cpu[0], mem[0]), (signal[1], cpu[1], mem[1]), etc.
        combinations = set(zip(
            data["signal_strength"],
            data["cpu_limit"],
            data["memory_limit"]
        ))

        # Sort for cleaner output
        sorted_combinations = sorted(list(combinations))

        print(f"\nScanning: {filepath}")
        print(f"Total experiments recorded: {len(data['signal_strength'])}")
        print(f"Unique Configurations Found: {len(sorted_combinations)}\n")

        # Table Header
        header = f"{'Signal (dB)':<15} | {'CPU Limit':<15} | {'Memory Limit':<15}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        # Print Rows
        for signal, cpu, memory in sorted_combinations:
            print(f"{signal:<15} | {cpu:<15} | {memory:<15}")
        print("-" * len(header))

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. The file format might be invalid.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # You can change the path here if needed
    file_path = "/home/kim/five_g_uplink_statistics_old.json"
    print_unique_combinations(file_path)