def check_not_null(df, column):
    """check if a column in a DataFrame is not null
    Args:
        df (DataFrame): The DataFrame to check.
        column (str): The name of the column to check.
    Returns:
        bool: True if the column is not null, False otherwise.
    """
    return df[column].isnull().sum() == 0


def check_not_empty(df, column):
    """check if a column in a DataFrame is not empty
    Args:
        df (DataFrame): The DataFrame to check.
        column (str): The name of the column to check.
    Returns:
        bool: True if the column is not empty, False otherwise.
    """
    return df[column].eq("").sum() == 0


def check_not_duplicate(df, column):
    """check if a column in a DataFrame is not duplicate
    Args:
        df (DataFrame): The DataFrame to check.
        column (str): The name of the column to check.
    Returns:
        bool: True if the column is not duplicate, False otherwise.
    """
    return df[column].duplicated().sum() == 0
