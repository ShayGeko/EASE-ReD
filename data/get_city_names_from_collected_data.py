import sys
import os

def find_all_cities_in_current_folder(folder, unique_cities = set()):
    files = os.listdir(folder)
    print(files)
    for file in files:
        if os.path.isdir(os.path.join(folder,file)):
            find_all_cities_in_current_folder(os.path.join(folder,file), unique_cities)
        else:
            city = file.split("_")[0]
            if city not in unique_cities:
                unique_cities.add(city)
    return unique_cities

def main(input_folder,output_file):
    # scan through all folders in input and parse file names
    # file format {city}_cleaned.csv

    unique_cities = find_all_cities_in_current_folder(input_folder)
    with open(output_file, "w") as f:
        for city in unique_cities:
            f.write(city + "\n")


if __name__ == "__main__":
    input_folder = "./demographicData/csv/data_world/us_county_demographics_grouped_norm.csv"
    output_file = "./demographicData/csv/data_world/counties.csv"
    main(input_folder, output_file)