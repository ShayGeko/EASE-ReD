import csv
import os
import requests
import sys

from dotenv import load_dotenv

totalRest = 1000


def search_yelp(api_key, term, location, offset=0):
    """
    Search Yelp API for businesses based on the given parameters.

    Parameters:
    - api_key (str): Yelp API key for authentication.
    - term (str): Search term for the type of business.
    - location (str): Location to search for businesses.
    - offset (int): Offset for pagination of results.

    Returns:
    - data (dict): JSON response containing the search results.
    """
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
    """
    Write the list of businesses to a CSV file.

    Parameters:
    - businesses (list): List of businesses to write to the CSV file.
    - filename (str): Name of the CSV file to write to.
    """
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
    """
    Main function to execute the program.
    """
    load_dotenv()
    api_key = os.getenv("YELP_API_KEY")

    term = "restaurant"
    location = sys.argv[1] if len(sys.argv) > 1 else "victoria"

    totalBus = []

    for i in range(0, totalRest, 50):
        data = search_yelp(api_key, term, location, offset=i)
        if "businesses" in data:
            totalBus.extend(data["businesses"])

    if not os.path.exists("csv"):
        os.makedirs("csv")
    write_to_csv(totalBus, os.path.join("csv", f"{location}.csv"))


if __name__ == "__main__":
    main()
