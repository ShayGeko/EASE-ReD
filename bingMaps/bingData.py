import requests
import csv
import os
from dotenv import load_dotenv
from itertools import islice

load_dotenv()
# Your Bing Maps API key
api_key = os.getenv("BING_API_KEY")

# The type of cuisine you're interested in
cuisine = "Restaurants"

# Read locations from counties_states.csv
with open("edited_counties.csv", "r") as f:
    reader = csv.reader(f)
    locations = list(islice(reader, 2262, None))  # Skip to line 449

# For each location
for location in locations:
    # Convert list to string
    location = " ".join(location)
    print(location)

    # Construct the URL for the HTTP request
    url = f"https://atlas.microsoft.com/search/poi/json?subscription-key={api_key}&api-version=1.0&query={cuisine}+in+{location}&limit=100"

    # Make the HTTP request
    response = requests.get(url)

    # Parse the response
    data = response.json()

    # Prepare data for CSV
    csv_data = []
    for item in data.get("results", []):
        categories = item["poi"]["categories"]
        if "restaurant" in categories:
            categories.remove("restaurant")
        if categories:  # Check if categories is not empty
            csv_data.append([categories])
    # Write data to CSV file
    with open(f"counties/{location}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Categories"])
        writer.writerows(csv_data)
