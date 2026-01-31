import pandas as pd
import os


def concatenate_csvs(file1_path, file2_path, output_path):
    """
    Reads two CSV files and concatenates them into a single file.
    """
    try:
        print(f"Reading {file1_path}...")
        df1 = pd.read_csv(file1_path)

        print(f"Reading {file2_path}...")
        df2 = pd.read_csv(file2_path)

        # Concatenate the dataframes
        # ignore_index=True resets the row numbers so they go 0, 1, 2... continuously
        print("Concatenating...")
        combined_df = pd.concat([df1, df2], ignore_index=True)

        # Save to disk
        print(f"Saving to {output_path}...")
        combined_df.to_csv(output_path, index=False)
        print("Done!")

    except FileNotFoundError as e:
        print(f"Error: The file could not be found. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    f1 = "/home/kim/csv_data_28_jan.csv"
    f2 = "/home/kim/five_g_merged_dataset_simultaneous_2.csv"
    out = "/home/kim/csv_data_31_jan.csv"
    concatenate_csvs(f1, f2, out)