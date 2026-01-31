import json


def merge_json_data(target_data, source_data, start_load=6.0):
    """
    Appends data from source_data to target_data for all samples
     where the 'load' is >= start_load.
    """
    # 1. Find indices in the source data that match our criteria
    source_loads = source_data.get("load", [])
    indices_to_copy = [i for i, load in enumerate(source_loads) if load >= start_load]

    if not indices_to_copy:
        print(f"No data found in source with load >= {start_load}")
        return target_data

    # 2. Define a recursive function to append list data
    def append_recursive(target, source, indices):
        for key, value in source.items():
            if isinstance(value, dict):
                # If target doesn't have this nested dict, skip or initialize it
                if key in target:
                    append_recursive(target[key], source[key], indices)
            elif isinstance(value, list):
                # Ensure the target has this list
                if key not in target:
                    target[key] = []
                # Append only the elements at the specified indices
                for idx in indices:
                    if idx < len(value):
                        target[key].append(value[idx])

    append_recursive(target_data, source_data, indices_to_copy)
    return target_data


if __name__ == '__main__':
    file_path_1 = "/home/kim/five_g_statistics_downlink_cpu_0_3_gain_10_memory_20.json"
    file_path_2 = "/home/kim/five_g_statistics_downlink_cpu_0_4_gain_10_memory_20.json"
    output_path = "/home/kim/five_g_statistics_downlink_cpu_0_3_gain_10_memory_20_updated.json"

    # Load data
    try:
        with open(file_path_1, 'r', encoding='utf-8') as f:
            data_1 = json.load(f)
        with open(file_path_2, 'r', encoding='utf-8') as f:
            data_2 = json.load(f)

        # Merge data from 6.0 upwards
        updated_data = merge_json_data(data_1, data_2, start_load=6.0)

        # Save the updated file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=4, sort_keys=True)

        print(f"Successfully updated file. Saved to: {output_path}")

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")