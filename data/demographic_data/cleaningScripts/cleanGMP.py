import pandas as pd
import csv


def clean():
    """
    Cleans the demographic data for different cities.

    This function reads in a list of city names from a CSV file, and for each city,
    it reads the corresponding data file, drops unnecessary columns, renames the columns,
    and saves the cleaned data back to the original file.

    Args:
        None

    Returns:
        None
    """
    # reading in the city names
    with open("city.csv", "r") as file:
        reader = csv.reader(file)

        next(reader)
        for city in reader:
            city_filename = city[0]
            data = pd.read_csv(city_filename)

            columns_to_drop = ["Address", "Website"]
            data.drop(columns=columns_to_drop, inplace=True)

            data.columns = ["cuisine", "name"]
            data.to_csv(f"{city_filename}", index=False)


if __name__ == "__main__":
    clean()
