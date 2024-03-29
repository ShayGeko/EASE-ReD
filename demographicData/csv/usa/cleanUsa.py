import pandas as pd
import os
import csv

# reading in the city names
with open("cities.csv", "r") as file:
    reader = csv.reader(file)

    next(reader)
    for city in reader:
        city_filename = city[0]
        city_data = pd.read_csv(city_filename)

        columns_to_drop = [
            "ID Year",
            "ID Birthplace",
            "Year",
            "ID Nativity",
            "Nativity",
            "Country Code",
            "ID Geography",
            "Geography",
        ]
        city_data = city_data.drop(columns=columns_to_drop)

        # replace with "n.o.s" to match canada data
        city_data["Birthplace"] = city_data["Birthplace"].replace(
            {
                r"(.*), not specified$": r"\1, n.o.s",
                "Other U.S. Island Areas, Oceania, Not Specified, or at Sea": "Other U.S. Island Areas, Oceania, n.o.s",
                "Not Specified": "n.o.s",
            },
            regex=True,
        )

        # save to new file
        cleaned_filename = f"{os.path.splitext(city_filename)[0]}_cleaned.csv"
        city_data.to_csv(cleaned_filename, index=False)
