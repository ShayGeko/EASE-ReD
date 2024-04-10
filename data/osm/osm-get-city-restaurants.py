import gzip
import json
import requests
import sys
import xml.etree.ElementTree as ET

from urllib.parse import urlencode

def get_city_restaurants_with_cuisine(city:str="Vancouver", state = ""):
    # The API URL
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:xml][timeout:90];
    area[name="{city}"];
    (
      node(area)["amenity"="restaurant"]["cuisine"];
      node(area)["amenity"="cafe"]["cuisine"];
    );
    out;
    """ if state == "" else\
        f"""
        [out:xml][timeout:90];
        // Define the state area
        area["admin_level"="4"]["name"="{state}"]->.stateArea;
        // Define the city area within the state
        area(area.stateArea)["name"="{city}"]->.cityArea;
        (
        // Search for nodes that are restaurants within the city area
        node(area.cityArea)["amenity"="restaurant"];
        // Search for nodes that are cafes within the city area
        node(area.cityArea)["amenity"="cafe"];
        );
        // Output the result
        out meta;
    """
    encoded_query = urlencode({"data": query})
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    print(f"sending the query for {city} {state}")
    response = requests.post(url, data=encoded_query, headers=headers)
    print(f"got response for {city}")
    return response

def get_all_city_restaurants(city:str="Vancouver"):
    # The API URL
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:xml][timeout:90];
    area[name="{city}"];
    (
      node(area)["amenity"="restaurant"];
      node(area)["amenity"="cafe"];
    );
    out;
    """
    encoded_query = urlencode({"data": query})
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    print(f"sending the query for {city}")
    response = requests.post(url, data=encoded_query, headers=headers)
    print(f"got response for {city}")
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

def main(city:str="Vancouver", type = 'cuisine', state=""):
    city_words = city.split(" ")
    # capitalize first letter
    city = " ".join([word.capitalize() for word in city_words])
    if type == 'cuisine':
        response = get_city_restaurants_with_cuisine(city, state)
    elif type == 'all':
        response = get_all_city_restaurants(city, state)
    else:
        print("Unrecognized type. Aborting...")
        return
    
    if response.status_code == 200:
        data = xml2dict(response.content)
        n_restaurants = len(data["nodes"])

        print(f"Found {n_restaurants} restaurants in {city}")

        filename = f"./data/osm-{city.lower()}-{state.lower()}-restaurant-{type}.json.gz"
        with gzip.open(filename, 'wt', encoding='UTF-8') as gzfile:
            json.dump(data, gzfile, indent=2)

        print(f"Data has been written to {filename}")
    else: 
        print(f"Failed to fetch data. Status code: {response.status_code}, error: {response.text}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        state = sys.argv[2] if len(sys.argv) > 2 else ''
        type = sys.argv[3] if len(sys.argv) > 3 else 'cuisine'
        main(city, type, state)
    else:
        main()  
