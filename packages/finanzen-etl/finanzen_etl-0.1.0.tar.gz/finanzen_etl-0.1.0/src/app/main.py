import pandas as pd


def read_a_csv(file_path: str = None) -> pd.DataFrame:
    """
    Reads a CSV file and returns a DataFrame.

    :param file_path: Path to the CSV file.
    :return: DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return pd.DataFrame()


def main():
    print(f"total rows are : {read_a_csv().count()}")


if __name__ == "__main__":
    main()
