import csv
import os
import re
import pandas as pd


def process_csv(input_file, output_file):
    """
    Process the CSV file by cleaning and removing unwanted rows.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.

    Returns:
        None
    """
    lines_to_remove = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        16,
        17,
        26,
        31,
        41,
        42,
        49,
        65,
        84,
        90,
        111,
        136,
        137,
        165,
        177,
        201,
        204,
        205,
        234,
        249,
        268,
        270,
        273,
    ]
    # Load the entire data
    df = pd.read_csv(input_file, encoding="ISO-8859-1", error_bad_lines=False)

    # Find the index of the row that contains "Total - Ethnic origin [5]"
    start_index = df[df.iloc[:, 0] == "Total - Ethnic origin [5]"].index[0]

    # Slice the DataFrame from the start_index row onwards
    df = df.loc[start_index:]

    # Keep only the first two columns
    df = df.iloc[:, :2]
    print(df.head())
    df.columns = ["origin", "population"]
    df["origin"] = df["origin"].str.replace(r'"\s*\d+\s*"', "")
    df["origin"] = df["origin"].str.replace("n.i.e", "n.o.s")
    df["origin"] = df["origin"].str.strip().str.replace('" ', '"')
    df.to_csv(output_file, index=False)


def process_csv_with_replacement(input_file, output_file, replace_column):
    """
    Process the CSV file with replacement of values in the first column.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
        replace_column (str): Path to the CSV file containing replacement values.

    Returns:
        None
    """
    process_csv(input_file, output_file)
    replace_data = pd.read_csv(replace_column, header=None)[0].tolist()
    df = pd.read_csv(output_file)
    df.iloc[: len(replace_data), 0] = replace_data
    df.to_csv(output_file, index=False)
    aggregate_data(
        output_file
    )  # Call the aggregate_data function after cleaning and replacing column names


# def process_csv_with_replacement(input_file, output_file, replace_column):
#     """
#     Process the CSV file with replacement of values in the first column.

#     Args:
#         input_file (str): Path to the input CSV file.
#         output_file (str): Path to the output CSV file.
#         replace_column (str): Path to the CSV file containing replacement values.

#     Returns:
#         None
#     """
#     process_csv(input_file, output_file)
#     replace_data = read_first_column(replace_column)
#     with open(output_file, "r") as f:
#         reader = csv.reader(f)
#         rows = list(reader)
#     with open(output_file, "w", newline="") as f:
#         writer = csv.writer(f)
#         for i, row in enumerate(rows):
#             if i < len(replace_data):
#                 row[0] = replace_data[i]
#             writer.writerow(row)
#     aggregate_data(
#         output_file
#     )  # Call the aggregate_data function after cleaning and replacing column names


def aggregate_data(output_file):
    """
    Aggregate the data by origin name and their sum.

    Args:
        output_file (str): Path to the output CSV file.

    Returns:
        None
    """
    df = pd.read_csv(output_file)
    df = df.groupby("origin").sum().reset_index()
    df.to_csv(output_file, index=False)


# def process_csv(input_file, output_file):
#     """
#     Process the CSV file by cleaning and removing unwanted rows.

#     Args:
#         input_file (str): Path to the input CSV file.
#         output_file (str): Path to the output CSV file.

#     Returns:
#         None
#     """
#     lines_to_remove = [
#         2,
#         6,
#         16,
#         17,
#         26,
#         31,
#         41,
#         42,
#         49,
#         65,
#         84,
#         90,
#         111,
#         136,
#         137,
#         165,
#         177,
#         201,
#         204,
#         205,
#         234,
#         249,
#         268,
#         270,
#         273,
#     ]

#     with open(input_file, "r", encoding="ISO-8859-1") as csv_file:
#         reader = csv.reader(csv_file)
#         with open(output_file, "w", newline="") as outfile:
#             writer = csv.writer(outfile)
#             writer.writerow(["origin", "population"])
#             header_skipped = False
#             for row in reader:
#                 if not header_skipped and row[0] == "Total - Ethnic origin [5]":
#                     header_skipped = True
#                     continue
#                 if header_skipped:
#                     cleaned_row = []
#                     for item in row:
#                         cleaned_item = re.sub(r'"\s*\d+\s*"', "", item)
#                         cleaned_item = cleaned_item.replace("n.i.e", "n.o.s")
#                         cleaned_item = cleaned_item.strip().replace('" ', '"')
#                         cleaned_row.append(
#                             cleaned_item.strip()
#                             if item.startswith('"')
#                             else cleaned_item
#                         )
#                     writer.writerow(cleaned_row[:-2])
#     with open(output_file, "r") as f:
#         lines = f.readlines()
#     with open(output_file, "w") as f:
#         for i, line in enumerate(lines, 1):
#             if i not in lines_to_remove:
#                 f.write(line)


def read_first_column(file_name):
    """
    Read the first column of a CSV file.

    Args:
        file_name (str): Path to the CSV file.

    Returns:
        list: The values in the first column.
    """
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        first_column = [row[0] for row in reader if row]
    return first_column


# def process_csv_with_replacement(input_file, output_file, replace_column):
#     """
#     Process the CSV file with replacement of values in the first column.

#     Args:
#         input_file (str): Path to the input CSV file.
#         output_file (str): Path to the output CSV file.
#         replace_column (str): Path to the CSV file containing replacement values.

#     Returns:
#         None
#     """
#     process_csv(input_file, output_file)

#     replace_data = read_first_column(replace_column)

#     with open(output_file, "r") as f:
#         reader = csv.reader(f)
#         rows = list(reader)
#     with open(output_file, "w", newline="") as f:
#         writer = csv.writer(f)
#         for i, row in enumerate(rows):
#             if i < len(replace_data):
#                 row[0] = replace_data[i]
#             writer.writerow(row)


def clean_census_for_cities(city_list_file, replace_column):
    """
    Clean the census data for multiple cities.

    Args:
        city_list_file (str): Path to the CSV file containing the list of cities.
        replace_column (str): Path to the CSV file containing replacement values.

    Returns:
        None
    """
    with open(city_list_file, "r") as cities_file:
        cities_reader = csv.reader(cities_file)
        for city_row in cities_reader:
            city_name = city_row[0]
            input_file = f"{city_name}.csv"
            output_file = os.path.join("cleanedcensus", f"{city_name}.csv")

            process_csv_with_replacement(input_file, output_file, replace_column)
            print(f"Cleaning for {city_name} completed.")


def main():
    """
    Main function to clean census data for cities.
    """
    city_list_file = "totalcities.csv"
    replace_column = "replace.csv"
    clean_census_for_cities(city_list_file, replace_column)


if __name__ == "__main__":
    main()
