import pandas as pd

if __name__ == "__main__":
    f2 = "/home/kim/five_g_merged_dataset_simultaneous.csv"

    # Read the CSV
    df1 = pd.read_csv(f2)

    # Define the columns you want to change
    columns_to_update = [
        "DU1_signal_strength",
        "DU2_signal_strength",
        "DU3_signal_strength",
        "DU4_signal_strength",
        "CU1_signal_strength",
        "CU2_signal_strength"
    ]

    # Assign the value 10 to all rows in these columns simultaneously
    df1[columns_to_update] = 10

    # Verify the changes (printing the first few rows instead of raw arrays is cleaner)
    print("Update complete. Verification of first 5 rows:")
    print(df1[columns_to_update].head())

    # Save the modified data back to a file
    # (Change the filename below if you want to overwrite the original)
    print(df1["DU1_signal_strength"].values)
    print(df1["DU2_signal_strength"].values)
    print(df1["DU3_signal_strength"].values)
    print(df1["DU4_signal_strength"].values)
    print(df1["CU1_signal_strength"].values)


    output_path = "/home/kim/five_g_merged_dataset_simultaneous_updated.csv"
    df1.to_csv(output_path, index=False)
    print(f"Saved updated file to: {output_path}")