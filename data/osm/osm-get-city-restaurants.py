import gzip
import json
import requests
import sys
import xml.etree.ElementTree as ET
import pandas as pd

from urllib.parse import urlencode

def get_city_restaurants_with_cuisine(county:str="Vancouver", state = ""):
    # The API URL
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:xml][timeout:180];
    area["name"="{county} County"]->.county; // County name is not unique!
    (
    node(area.county)["amenity"="restaurant"];
    node(area.county)["amenity"="cafe"];
    );
    // Output the result
    out meta;
    """
    encoded_query = urlencode({"data": query})
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    print(f"Sending the query for {county} County")
    response = requests.post(url, data=encoded_query, headers=headers)
    print(f"Got response for {county} County")
    return response

def xml2dict(xml: str):
    root = ET.fromstring(xml)
    data = {"nodes": []}
    for node in root.findall('.//node'):
        node_data = {
            "id": node.attrib.get("id"),
            "lat": node.attrib.get("lat"),
            "lon": node.attrib.get("lon"),
            "tags": {}
        }
        for tag in node.findall('./tag'):
            node_data["tags"][tag.attrib.get("k")] = tag.attrib.get("v")
        data["nodes"].append(node_data)

    return data


def get_county_restaurants(county:str="New York", type = 'cuisine'):
    county_wds = county.split(" ")
    # capitalize first letter
    county = " ".join([word.capitalize() for word in county_wds])
    if type == 'cuisine':
        response = get_city_restaurants_with_cuisine(county)
    else:
        print("Unrecognized type. Aborting...")
        return
    
    if response.status_code == 200:
        print("Data fetched successfully. Parsing xml...")
        data = xml2dict(response.content)
        n_restaurants = len(data["nodes"])

        print(f"Found {n_restaurants} restaurants in {county} County")

        filename = f"./data/osm-{county.lower()}-restaurant-{type}.json.gz"
        with gzip.open(filename, 'wt', encoding='UTF-8') as gzfile:
            json.dump(data, gzfile, indent=2)

        print(f"Data has been written to {filename}")
    else: 
        print(f"Failed to fetch data. Status code: {response.status_code}, error: {response.text}")

def main(counties_file = "./counties.csv"):
    counties = pd.read_csv(counties_file)

    for county in counties['county']:
        get_county_restaurants(county)
    


if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        state = sys.argv[2] if len(sys.argv) > 2 else ''
        type = sys.argv[3] if len(sys.argv) > 3 else 'cuisine'
        main(city, type, state)
    else:
        main()  
