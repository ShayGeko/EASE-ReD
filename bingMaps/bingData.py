import requests
import csv
import os
from dotenv import load_dotenv
from itertools import islice

load_dotenv()  # load environment variables from .env file
api_key = os.getenv(
    "BING_API_KEY"
)  # get the Bing Maps API key from environment variables

cuisine = "Restaurants"  # define the type of cuisine you're interested in

# read locations from counties_states.csv
with open("edited_counties.csv", "r") as f:
    reader = csv.reader(f)
    locations = list(islice(reader, 1893, None))  # skip to line 449

# for each location
for location in locations:
    location = " ".join(location)  # convert list to string

    # construct the URL for the HTTP request
    url = f"https://atlas.microsoft.com/search/poi/json?subscription-key={api_key}&api-version=1.0&query={cuisine}+in+{location}&limit=100"

    response = requests.get(url)  # make the HTTP request

    data = response.json()  # parse the response

    # prepare data for CSV
    csv_data = []
    for item in data.get("results", []):
        # categories = item["poi"]["categories"]
        name = item["poi"]["name"]
        # print(name)
        # if "restaurant" in categories:  # if "restaurant" is in categories, remove it
        #     categories.remove("restaurant")
        if name:  # if not empty
            csv_data.append([name])

    # write data to CSV file
    with open(f"nameCategory/{location}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        print("Currently creating: ", location)
        writer.writerow(["Name"])  # write the header
        writer.writerows(csv_data)  # write the rows
