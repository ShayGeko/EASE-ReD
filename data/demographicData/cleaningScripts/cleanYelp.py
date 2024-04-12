import pandas as pd
import csv


def clean():
    # reading in the city names
    with open("city.csv", "r") as file:
        reader = csv.reader(file)

        next(reader)
        for city in reader:
            city_filename = city[0]
            data = pd.read_csv(city_filename)

            columns_to_drop = ["Alias"]
            data.drop(columns=columns_to_drop, inplace=True)

            data.columns = ["name", "cuisine"]
            # Swap 'name' and 'cuisine' columns
            data = data[["cuisine", "name"]]
            data.to_csv(f"{city_filename}", index=False)


if __name__ == "__main__":
    clean()
