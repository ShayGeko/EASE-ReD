import gzip
import json
import requests
import sys
import xml.etree.ElementTree as ET

from urllib.parse import urlencode

def get_city_restaurants_with_cuisine(city:str="Vancouver"):
    # The API URL
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:xml][timeout:90];
    area[name="{city}"][admin_level=8]->.searchArea;
    (
      node(area.searchArea)["amenity"="restaurant"]["cuisine"];
      node(area.searchArea)["amenity"="cafe"]["cuisine"];
    );
    out meta;
    """
    encoded_query = urlencode({"data": query})
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=encoded_query, headers=headers)
    return response

def get_all_city_restaurants(city:str="Vancouver"):
    # The API URL
    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:xml][timeout:90];
    area[name="{city}"][admin_level=8]->.searchArea;
    (
      node(area.searchArea)["amenity"="restaurant"];
      node(area.searchArea)["amenity"="cafe"];
    );
    out meta;
    """
    encoded_query = urlencode({"data": query})
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=encoded_query, headers=headers)
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
        data.append(node_data)

    return data

def main(city:str="Vancouver", type = 'cuisine'):
    if type == 'cuisine':
        response = get_city_restaurants_with_cuisine(city)
    elif type == 'all':
        response = get_all_city_restaurants(city)
    else:
        print("Unrecognized type. Aborting...")
        return
    
    if response.status_code == 200:
        data = xml2dict(response.content)
        n_restaurants = len(data["nodes"])

        print(f"Found {n_restaurants} restaurants in {city}")

        filename = f"../osm-{city.lower()}-restaurant-{type}.json.gz"
        with gzip.open(filename, 'wt', encoding='UTF-8') as gzfile:
            json.dump(data, gzfile, indent=2)

        print(f"Data has been written to {filename}")
    else: 
        print(f"Failed to fetch data. Status code: {response.status_code}, error: {response.text}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        type = sys.argv[2] if len(sys.argv) > 2 else 'cuisine'
        main(city, type)
    else:
        main()  
