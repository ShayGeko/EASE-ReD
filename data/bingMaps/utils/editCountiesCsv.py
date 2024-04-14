import pandas as pd


def edit_counties_csv():
    """
    This function reads a CSV file containing counties and states data,
    merges two columns together with a space in between, and writes the
    merged data to a new CSV file.

    Parameters:
    None

    Returns:
    None
    """
    # Load the data
    df = pd.read_csv(
        "counties_states.csv",
        header=None,
    )

    # Merge two columns together with a space in between
    newDf = df[df.columns[0]].astype(str) + " " + df[df.columns[1]].astype(str)

    # Write it back to a new file
    newDf.to_csv(
        "edited_counties.csv",
        header=False,
        index=False,
    )
