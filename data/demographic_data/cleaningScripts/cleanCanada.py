import pandas as pd
import numpy as np
import sys


def clean(file):
    """
    Cleans the given CSV file containing demographic data for the Old Stats Canada dataset.

    Parameters:
    file (str): The path to the CSV file to be cleaned.

    Returns:
    None
    """
    data = pd.read_csv(file)
    filename = file.split("/")[-1].replace(".csv", "")

    # drop columns: Total - Gender_Symb	Men+ (2),	Men+_Symb,	Women+ (3),	Women+_Symb
    data = data.drop(data.columns[[2] + list(range(4, data.shape[1]))], axis=1)

    # remove columns that aren't the ethnic and total data
    topic = data.columns[0]
    total = data.columns[2]
    nationality = data.columns[1]
    data = data[data[topic] != "Visible minority"]
    data = data[~data[topic].str.startswith("Total")]

    # Strip spaces after opening quotation mark in the nationality column
    data[nationality] = data[nationality].str.lstrip()

    # calculating the percentage for each group
    data["percentage"] = data[total][1:] / data[total][1:].sum() * 100

    data = data.drop(columns=topic)

    # rename the column names
    data.columns = ["nationality", "total_population", "percentage"]

    # count up total classes
    totalClasses = data[data.columns[0]].nunique()

    # create a new df with total classes
    total_classes_df = pd.DataFrame(
        [["Total Classes in CSV", totalClasses, np.nan]], columns=data.columns
    )

    # xoncat new df with the data
    data = pd.concat([total_classes_df, data]).reset_index(drop=True)
    print(data)
    data.to_csv(f"{filename}_cleaned.csv", index=False)


if __name__ == "__main__":
    clean(sys.argv[1])
