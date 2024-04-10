import csv
import os
import requests
import sys

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


def main():
    load_dotenv()
    api_key = os.getenv('YELP_API_KEY')

    # set location to whatever
    term = "restaurant"
    location = sys.argv[1]  if len(sys.argv)>1 else "victoria"

    # list for csv
    totalBus = []

    for i in range(0, totalRest, 50):
        data = search_yelp(api_key, term, location, offset=i)
        if "businesses" in data:
            totalBus.extend(data["businesses"])

    # write to csv
    if not os.path.exists("csv"):
        os.makedirs("csv")
    write_to_csv(totalBus, os.path.join("csv", f"{location}.csv"))

if __name__ == "__main__":
    main()
