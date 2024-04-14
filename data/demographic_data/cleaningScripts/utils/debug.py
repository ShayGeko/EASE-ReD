import sys
import pandas as pd
import numpy as np


def main(input):
    """
    This function reads a CSV file and prints the first few rows of the DataFrame.

    Parameters:
    input (str): The path to the CSV file.

    Returns:
    None
    """
    df = pd.read_csv(input, sep=",")

    print(df.head())


if __name__ == "__main__":
    input = sys.argv[1]

    main(input)
