import requests
import json
import csv
import os
from dotenv import load_dotenv

# **** Should be in the same directory as the utils folder ****


def search_restaurants(cuisine, apiKey, location):
    """
    Search for restaurants based on cuisine and location using the Google Places API.

    Args:
        cuisine (str): The type of cuisine to search for.
        apiKey (str): The API key for accessing the Google Places API.
        location (str): The location to search for restaurants in.

    Returns:
        dict: The JSON response containing the search results.
    """
    query = f"{cuisine} Restaurants in {location}"
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": apiKey,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types,places.websiteUri",
    }
    data = {"textQuery": query}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def main():
    """
    Main function to execute the program.

    This function loads environment variables, reads county data from a CSV file,
    and performs restaurant searches for each county and cuisine type.
    The search results are then written to separate CSV files for each county.
    """
    print("Loading environment variables...")
    load_dotenv()
    apiKey = os.getenv("GOOGLE_API_KEY")
    print("Environment variables loaded.")

    with open("us_counties.csv", "r") as counties_file:
        counties_reader = csv.reader(counties_file)

        for county_row in counties_reader:
            # current location
            location = county_row[0]
            print(f"Creating new file for location: {location}")
            with open(f"usrestaurants/{location}.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Cuisine Type", "Name"])
                with open("cuisine.csv", "r") as cuisine_file:
                    reader = csv.reader(cuisine_file)
                    for row in reader:
                        # get the cuisine
                        cuisine = row[0]
                        print(
                            f"Making request for cuisine: {cuisine} in location: {location}"
                        )

                        # api request
                        data = search_restaurants(cuisine, apiKey, location)
                        for place in data.get("places", []):
                            name = place["displayName"]["text"]
                            address = place["formattedAddress"]
                            website = place.get("websiteUri", "")

                            # write it to the csv
                            writer.writerow([cuisine, name, address, website])


if __name__ == "__main__":
    main()
