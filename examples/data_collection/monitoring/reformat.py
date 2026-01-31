import json

if __name__ == '__main__':
    # 1. Load the data
    file_path = "/home/kim/five_g_statistics_merged.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Define the DU names (from your original script)
    du_names = [
        "csle_cloud_ran_du_1_1-level17-15",
        "csle_cloud_ran_du_1_2-level17-15",
        "csle_cloud_ran_du_1_3-level17-15",
        "csle_cloud_ran_du_1_4-level17-15"
    ]

    # 3. Iterate through each DU and rename the specific keys
    for du in du_names:
        if du in data:
            # We create a list of keys to modify to avoid "dictionary size changed during iteration" errors
            keys_to_rename = [k for k in data[du].keys() if k.startswith("e2e_")]

            for old_key in keys_to_rename:
                # Construct the new key name
                new_key = old_key.replace("e2e_", "e2e_uplink_")

                # Move the data to the new key and delete the old one
                data[du][new_key] = data[du].pop(old_key)

    # 4. Save the modified JSON back to a file
    output_path = "/home/kim/five_g_statistics_renamed.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True)

    print(f"Renaming complete. File saved to: {output_path}")