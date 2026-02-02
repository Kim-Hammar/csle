import pandas as pd


def concatenate_csvs(file1_path: str, file2_path: str, output_path: str) -> None:
    """
    Reads two CSV files and concatenates them into a single file.

    :param file1_path: the path to the first CSV file
    :param file2_path: the path to the second CSV file
    :param output_path: the path to save the concatenated CSV file
    :return: None
    """
    try:
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        combined_df = pd.concat([df1, df2], ignore_index=True)
        combined_df.to_csv(output_path, index=False)
    except FileNotFoundError as e:
        print(f"Error: The file could not be found. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    f1 = "/home/kim/csv_data_31_jan.csv"
    f2 = "/home/kim/five_g_merged_dataset_simultaneous_3.csv"
    out = "/home/kim/csv_data_2_feb.csv"
    concatenate_csvs(f1, f2, out)
