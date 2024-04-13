import pandas as pd
import numpy as np
import sys
import ast


# converting string vector to list of numbers


import numpy as np


def sum_string_vector(string_vector1, string_vector2):
    # Convert string vectors to numpy arrays
    list_vector1 = np.fromstring(string_vector1[0:-1], sep=",")
    list_vector2 = np.fromstring(string_vector2[0:-1], sep=",")

    # Sum all the corresponding values in the arrays
    sum_vector = np.add(list_vector1, list_vector2)

    # Calculate average
    avg_vector = sum_vector / 2

    return ",".join(map(str, avg_vector.tolist()))


def merge_category_name(df1, df2, ouputFileName):
    """
    for every val in the string vector sum those together then YEAH
    """
    # take the two df's
    df1["sum"] = df1.iloc[:, 1:]
    df1 = df1.drop(columns=["embedding"], axis=1)

    df2["sum"] = df2.iloc[:, 1:]
    df2 = df2.drop(columns=["embedding"], axis=1)

    merged_df = pd.merge(df1, df2, on="county")

    # Apply the function to each row
    merged_df["avg"] = merged_df.apply(
        lambda row: sum_string_vector(row["sum_x"], row["sum_y"]), axis=1
    )
    merged_df.drop(columns=["sum_x", "sum_y"], inplace=True)
    merged_df.rename(columns={"avg": "embedding"}, inplace=True)
    merged_df.to_csv(f"{ouputFileName}.csv", index=False)


if __name__ == "__main__":
    df1 = pd.read_csv(sys.argv[1])
    df2 = pd.read_csv(sys.argv[2])
    output = sys.argv[3]
    merge_category_name(df1, df2, output)
