import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()
# Your Bing Maps API key
api_key = os.getenv("BING_MAPS_API_KEY")

# The type of cuisine you're interested in
cuisine = "Restaurant"

# The location you're searching in
location = "New York"

# Construct the URL for the HTTP request
url = f"https://atlas.microsoft.com/search/poi/json?subscription-key={api_key}&api-version=1.0&query={cuisine}+in+{location}&limit=100"

# Make the HTTP request
response = requests.get(url)

# Parse the response
data = response.json()

# Prepare data for CSV
csv_data = []
for item in data["results"]:
    categories = item["poi"]["categories"]
    if "restaurant" in categories:
        categories.remove("restaurant")
        print(categories)
    if categories:  # Check if categories is not empty
        csv_data.append([categories])
# Write data to CSV file
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Categories"])
    writer.writerows(csv_data)
