import requests
import json
import csv
import os
from dotenv import load_dotenv
import aiohttp
import asyncio

# def search_restaurants(query, apiKey, location):
#     query = f"{cuisine} Restaurants in {location}"
#     url = "https://places.googleapis.com/v1/places:searchText"
#     headers = {
#         "Content-Type": "application/json",
#         "X-Goog-Api-Key": apiKey,
#         "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types,places.websiteUri",
#     }
#     data = {"textQuery": query}
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     return response.json()


# location = "Kelowna, BC, Canada"

# with open(f"{location}.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Cuisine Type", "Name", "Address", "Website"])

#     load_dotenv()
#     apiKey = os.getenv("GOOGLE_API_KEY")

#     for cuisine, query in cuisine_types.items():
#         # API rq
#         data = search_restaurants(query, apiKey, location)

#         for place in data.get("places", []):
#             name = place["displayName"]["text"]
#             address = place["formattedAddress"]
#             website = place.get("websiteUri", "")

#             writer.writerow([cuisine, name, address, website])


# the 'proper' divide by two lol
def get_query(cuisine):
    query = cuisine + " Food"
    return query


# make the call async so we dont block while waiting for response
async def search_restaurants_async(query, apiKey, location):
    query = f"{query} Restaurants in {location}"
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": apiKey,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types,places.websiteUri",
    }
    data = {"textQuery": query}
    print(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, headers=headers, data=json.dumps(data)
        ) as response:
            print("balls")
            print(response.status)
            return await response.json()


async def process_queries(apiKey, filename, location="Vernon, BC"):
    tasks = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            cuisine = row[0]
            query = get_query(cuisine)
            task = search_restaurants_async(query, apiKey, location)
            tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results


async def main():
    load_dotenv()
    apiKey = os.getenv("GOOGLE_API_KEY")

    filename = "cuisine.csv"
    # apiKey = ""
    results = await process_queries(apiKey, filename)
    # # store results etc
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
    # main()
