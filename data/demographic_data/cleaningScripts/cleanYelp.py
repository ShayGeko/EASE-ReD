import pandas as pd
import csv


import csv
import pandas as pd

def clean():
    """
    Cleans the Yelp data by dropping unnecessary columns, renaming columns, and swapping column positions.

    This function reads in a list of city names from a CSV file called 'city.csv'. For each city, it reads in a
    corresponding CSV file containing Yelp data. It drops the 'Alias' column, renames the remaining columns to
    'name' and 'cuisine', and swaps the positions of the 'name' and 'cuisine' columns. Finally, it saves the cleaned
    data back to the same CSV file.

    Note: This function assumes that the CSV files for each city are named after the city itself.

    Returns:
        None
    """
    with open("city.csv", "r") as file:
        reader = csv.reader(file)

        next(reader)
        for city in reader:
            city_filename = city[0]
            data = pd.read_csv(city_filename)

            columns_to_drop = ["Alias"]
            data.drop(columns=columns_to_drop, inplace=True)

            data.columns = ["name", "cuisine"]
            data = data[["cuisine", "name"]]

            data.to_csv(f"{city_filename}", index=False)


if __name__ == "__main__":
    clean()
