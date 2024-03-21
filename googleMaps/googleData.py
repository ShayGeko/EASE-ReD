import requests
import json
import csv
import os
from dotenv import load_dotenv


def search_restaurants(query, apiKey, location):
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


location = "Kelowna, BC, Canada"

with open(f"{location}.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Cuisine Type", "Name", "Address", "Website"])

    with open("cuisine.csv", "r") as cuisine_file:
        reader = csv.reader(cuisine_file)
        load_dotenv()
        apiKey = os.getenv("GOOGLE_API_KEY")

        for row in reader:
            cuisine = row[0]  # Get the cuisine from the first column
            # API rq
            data = search_restaurants(cuisine, apiKey, location)

            for place in data.get("places", []):
                name = place["displayName"]["text"]
                address = place["formattedAddress"]
                website = place.get("websiteUri", "")

                writer.writerow([cuisine, name, address, website])
