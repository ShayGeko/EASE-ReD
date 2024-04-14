import pandas as pd
import sys
import os

# **** Should be in the same directory as the uncleaned data ****


def reformat(input):
    """
    Reformat the input CSV file by performing various data cleaning operations.

    Parameters:
    input (str): The path to the input CSV file.

    Returns:
    None
    """
    data = pd.read_csv(input)
    # get the base filename without extension
    base_filename = os.path.splitext(os.path.basename(input))[0]

    # removing any whitespace from the data
    data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # remove rows where the first column contains a :
    data = data[~data.iloc[:, 0].str.contains(":")]

    # replace 'n.e.c.' with 'n.o.c.' in the first column
    data.iloc[:, 0] = data.iloc[:, 0].str.replace("n.e.c.", "n.o.c.")

    # skip the first two columns
    for column in data.columns[2:]:
        # keep the first two columns and the current column
        new_data = data[[data.columns[0], column]]

        # remove the last 10 characters from the column name
        new_column_name = column[:-10]

        # rename the column
        new_data.columns = ["origin", new_column_name]

        # remove any " in the second column
        new_data[new_column_name] = new_data[new_column_name].str.replace('"', "")

        # append the new column name to the base filename
        new_filename = f"cleanedcounties/{new_column_name}.csv"

        new_data.to_csv(new_filename, index=False)


if __name__ == "__main__":
    filename = sys.argv[1]
    reformat(filename)
