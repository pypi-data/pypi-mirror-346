import pandas as pd
from src.app.utils import validation_utils
import sys
sys.path.append('/src/app')


def main():
    # Example usage of the validation_utils module
    data = {
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c'],
        'column3': [True, False, None]
    }
    df = pd.DataFrame(data)
    # Validate the data
    is_valid = validation_utils.check_not_null(df, 'column2')
    if is_valid:
        print("Data is valid.")
    else:
        print("Data is invalid. ")


if __name__ == "__main__":
    main()
