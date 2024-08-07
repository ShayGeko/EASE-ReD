import pandas as pd


def get_unique_ethnicities():
    """
    Reads a CSV file containing Canada Census data and extracts the unique origins/ethnic groups.
    Saves the unique values to a new CSV file.

    Returns:
    None
    """
    # identifying all of the origins/ethnic groups in the Canada Census data
    df = pd.read_csv("ethnicities_in_canadaCensus.csv")
    unique = df.iloc[:, 0].unique()
    df_unique = pd.DataFrame(unique, columns=[df.columns[0]])
    df_unique.to_csv("ethnicities_in_canadaCensus.csv", index=False)


if __name__ == "__main__":
    get_unique_ethnicities()
