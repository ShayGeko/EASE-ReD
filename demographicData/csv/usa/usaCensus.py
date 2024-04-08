import pandas as pd
import sys


def reformat(input):
    data = pd.read_csv(input)
    base_filename = input[:-10]  # remove the last 10 characters from the filename

    for column in data.columns[2:]:  # skip the first two columns
        # keep the first two columns and the current column
        new_data = data[[data.columns[0], column]]

        # remove the last 10 characters from the column name
        new_column_name = column[:-10]

        # rename the column
        new_data = new_data.rename(columns={column: new_column_name})

        # Remove any leading or trailing whitespace (including tabs) from the data
        new_data = new_data.map(lambda x: x.strip() if isinstance(x, str) else x)

        # remove anything with a :
        new_data = new_data.loc[
            ~(new_data[new_data.columns[0]].str.contains(":") & (new_data.index > 1))
        ]

        # Rename the header columns to origin, population
        new_data.columns = ["origin", "population"]

        # remove any " in the second column
        new_data[new_data.columns[1]] = (
            new_data[new_data.columns[1]].astype(str).str.replace('"', "")
        )
        # replace 'n.e.c.' with 'n.o.c.' in the first column
        new_data[new_data.columns[0]] = new_data[new_data.columns[0]].str.replace(
            "n.e.c.", "n.o.c."
        )

        new_filename = f"counties/{new_column_name}.csv"  # append the new column name to the base filename

        new_data.to_csv(new_filename, index=False)


if __name__ == "__main__":
    filename = sys.argv[1]
    reformat(filename)
