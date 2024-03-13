import csv
import requests
import os

from dotenv import load_dotenv

# can only make max 50 requests, up 1000 restaurants at a time
"""
Kelowna - 559 
Richmond - 4900 
Van - 5400 
Surrey - 1800 
Burnaby - 6600 
Victoria - 778 
"""
totalRest = 1000


def search_yelp(api_key, term, location, offset=0):
    url = "https://api.yelp.com/v3/businesses/search"

    headers = {"Authorization": f"Bearer {api_key}"}

    params = {
        "term": term,
        "location": location,
        "limit": 50,  # max num of results per request
        "offset": offset,
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    return data

load_dotenv()
api_key = os.getenv('YELP_API_KEY')

# set location to whatever
term = "restaurant"
location = "victoria"


def write_to_csv(businesses, filename):
    fieldnames = ["Name", "Alias", "Title"]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for business in businesses:
            row = {"Name": business["name"], "Alias": business["alias"]}
            if "categories" in business and len(business["categories"]) > 0:
                row["Title"] = business["categories"][0]["title"]
            writer.writerow(row)


# list for csv
totalBus = []

for i in range(0, totalRest, 50):
    data = search_yelp(api_key, term, location, offset=i)
    if "businesses" in data:
        totalBus.extend(data["businesses"])


# write to csv
write_to_csv(totalBus, f"{location}.csv")
