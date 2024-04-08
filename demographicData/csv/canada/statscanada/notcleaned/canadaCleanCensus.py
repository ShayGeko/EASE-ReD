import csv
import os
import re


def process_csv(input_file, output_file):
    # Your existing CSV processing code
    lines_to_remove = [
        2,
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

    with open(input_file, "r", encoding="ISO-8859-1") as csv_file:
        reader = csv.reader(csv_file)
        with open(output_file, "w", newline="") as outfile:
            writer = csv.writer(outfile)

            header_skipped = False
            for row in reader:
                if not header_skipped and row[0] == "Total - Ethnic origin [5]":
                    header_skipped = True
                    writer.writerow(row)
                    continue
                if header_skipped:
                    cleaned_row = []
                    for item in row:
                        cleaned_item = re.sub(r'"\s*\d+\s*"', "", item)
                        cleaned_item = cleaned_item.replace("n.i.e", "n.o.s")
                        cleaned_item = cleaned_item.strip().replace('" ', '"')
                        cleaned_row.append(
                            cleaned_item.strip()
                            if item.startswith('"')
                            else cleaned_item
                        )
                    writer.writerow(cleaned_row[:-2])

    with open(output_file, "r") as f:
        lines = f.readlines()
    with open(output_file, "w") as f:
        for i, line in enumerate(lines, 1):
            if i not in lines_to_remove:
                f.write(line)


def read_first_column(file_name):
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        first_column = [row[0] for row in reader if row]
    return first_column


def process_csv_with_replacement(input_file, output_file, replace_column):
    process_csv(input_file, output_file)

    replace_data = read_first_column(replace_column)

    with open(output_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        for i, row in enumerate(rows):
            if i < len(replace_data):
                row[0] = replace_data[i]
            writer.writerow(row)


def clean_census_for_cities(city_list_file, replace_column):
    with open(city_list_file, "r") as cities_file:
        cities_reader = csv.reader(cities_file)
        for city_row in cities_reader:
            city_name = city_row[0]
            input_file = f"{city_name}.csv"
            output_file = os.path.join("cleanedcensus", f"{city_name}.csv")

            process_csv_with_replacement(input_file, output_file, replace_column)
            print(f"Cleaning for {city_name} completed.")


def main():
    city_list_file = "totalcities.csv"  # Adjust this with your file name
    replace_column = "replace.csv"  # Adjust this with your file name
    clean_census_for_cities(city_list_file, replace_column)


if __name__ == "__main__":
    main()
