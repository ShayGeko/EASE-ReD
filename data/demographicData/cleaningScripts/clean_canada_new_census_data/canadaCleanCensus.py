import csv
import os
import pandas as pd

# **** Should be in the same directory as the uncleaned data ****


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
        0,
        1,
        2,
        3,
        4,
        5,
        6,
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
    df = pd.read_csv(
        input_file, encoding="ISO-8859-1", skiprows=list(range(0, 6)), nrows=284
    )

    # drop the columns after the second column
    df.drop(df.iloc[:, 2:], inplace=True, axis=1)

    # assign new columns names
    df.columns = ["origin", "population"]

    # replacing n.o.s and whitesoace chatacters
    df["origin"] = df["origin"].str.replace(r'"\s*\d+\s*"', "")
    df["origin"] = df["origin"].str.replace("n.i.e", "n.o.s")
    df["origin"] = df["origin"].str.strip().str.replace('" ', '"')

    # remove the lines from lines_to_remove
    df = df.drop(lines_to_remove, errors="ignore")

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

    # read the replacement data from the replace_column csv file
    replace_data = pd.read_csv(replace_column, header=None)[0].tolist()

    df = pd.read_csv(output_file)

    # replace the first column of the cleaned csv file with the replacement data
    df.iloc[: len(replace_data), 0] = replace_data

    df.to_csv(output_file, index=False)

    aggregate_data(output_file)
    process_csv(input_file, output_file)

    # replace the first column of the cleaned csv file with the replacement data
    replace_data = pd.read_csv(replace_column, header=None)[0].tolist()

    df = pd.read_csv(output_file)

    # replace the first column of the cleaned csv file with the replacement data
    df.iloc[: len(replace_data), 0] = replace_data

    # write the replaced data back to the csv file
    df.to_csv(output_file, index=False)

    # aggregate the data in the csv file
    aggregate_data(output_file)


def aggregate_data(output_file):
    """
    Aggregate the data by origin name and their sum.

    Args:
        output_file (str): Path to the output CSV file.

    Returns:
        None
    """
    df = pd.read_csv(output_file)

    # group by the sum of the population by origin
    df = df.groupby("origin").sum().reset_index()
    df.to_csv(output_file, index=False)


def clean_census_for_cities(city_list_file, replace_column):
    """
    Clean the census data for multiple cities.

    Args:
        city_list_file (str): Path to the CSV file containing the list of cities.
        replace_column (str): Path to the CSV file containing replacement values.

    Returns:
        None
    """
    # open the city list file
    with open(city_list_file, "r") as cities_file:
        cities_reader = csv.reader(cities_file)

        for city_row in cities_reader:
            city_name = city_row[0]

            # construct the input file path using the city name
            input_file = f"{city_name}.csv"

            # construct the output file path using the city name
            output_file = os.path.join("cleanedcensus", f"{city_name}.csv")

            # call the function to process the csv file with replacement
            process_csv_with_replacement(input_file, output_file, replace_column)

            # print a message indicating the completion of cleaning for the current city
            print(f"cleaning for {city_name} completed.")


def main():
    """
    Main function to clean census data for cities.
    """
    city_list_file = "totalcities.csv"
    replace_column = "replace.csv"
    clean_census_for_cities(city_list_file, replace_column)


if __name__ == "__main__":
    main()
