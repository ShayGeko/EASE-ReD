import requests
import json
import csv


def search_restaurants(query, apiKey, location):
    query = f"{cuisine} Restaurants in {location}"
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": apiKey,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.types,places.websiteUri",
    }
    data = {"textQuery": query}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


# 102 total
cuisine_types = {
    "Mexican": "Mexican Food",
    "Swedish": "Swedish Food",
    "Latvian": "Latvian Food",
    "Italian": "Italian Food",
    "Spanish": "Spanish Food",
    "American": "American Food",
    "Scottish": "Scottish Food",
    "British": "British Food",
    "Thai": "Thai Food",
    "Japanese": "Japanese Food",
    "Chinese": "Chinese Food",
    "Indian": "Indian Food",
    "Canadian": "Canadian Food",
    "Russian": "Russian Food",
    "Jewish": "Jewish Food",
    "Polish": "Polish Food",
    "German": "German Food",
    "French": "French Food",
    "Hawaiian": "Hawaiian Food",
    "Brazilian": "Brazilian Food",
    "Peruvian": "Peruvian Food",
    "Salvadorian": "Salvadorian Food",
    "Cuban": "Cuban Food",
    "Tibetan": "Tibetan Food",
    "Egyptian": "Egyptian Food",
    "Greek": "Greek Food",
    "Belgian": "Belgian Foods",
    "Irish": "Irish Food",
    "Welsh": "Welsh Food",
    "Cajun": "Cajun Food",
    "Portuguese": "Portuguese Food",
    "Turkish": "Turkish Food",
    "Haitian": "Haitian Food",
    "Tahitian": "Tahitian Food",
    "Kenyan": "Kenyan Food",
    "Korean": "Korean Food",
    "Algerian": "Algerian Food",
    "Nigerian": "Nigerian Food",
    "Libyan": "Libyan Food",
    "Moroccan": "Moroccan Food",
    "Lebanese": "Lebanese Food",
    "Vietnamese": "Vietnamese Food",
    "Hungarian": "Hungarian Food",
    "Mediterranean": "Mediterranean Food",
    "Mormon": "Mormon Food",
    "Ethiopian": "Ethiopian Food",
    "Caribbean": "Caribbean Food",
    "Soul": "Soul Food",
    "Argentinian": "Argentinian Food",
    "Chilean": "Chilean Food",
    "Colombian": "Colombian Food",
    "Costa Rican": "Costa Rican Food",
    "Czech": "Czech Food",
    "Danish": "Danish Food",
    "Dutch": "Dutch Food",
    "Ecuadorian": "Ecuadorian Food",
    "Finnish": "Finnish Food",
    "Ghanaian": "Ghanaian Food",
    "Guatemalan": "Guatemalan Food",
    "Honduran": "Honduran Food",
    "Icelandic": "Icelandic Food",
    "Indonesian": "Indonesian Food",
    "Iranian": "Iranian Food",
    "Iraqi": "Iraqi Food",
    "Israeli": "Israeli Food",
    "Jamaican": "Jamaican Food",
    "Jordanian": "Jordanian Food",
    "Kuwaiti": "Kuwaiti Food",
    "Laotian": "Laotian Food",
    "Lithuanian": "Lithuanian Food",
    "Malaysian": "Malaysian Food",
    "Mongolian": "Mongolian Food",
    "Nepalese": "Nepalese Food",
    "Nicaraguan": "Nicaraguan Food",
    "Norwegian": "Norwegian Food",
    "Pakistani": "Pakistani Food",
    "Panamanian": "Panamanian Food",
    "Paraguayan": "Paraguayan Food",
    "Peruvian": "Peruvian Food",
    "Philippine": "Philippine Food",
    "Polish": "Polish Food",
    "Puerto Rican": "Puerto Rican Food",
    "Romanian": "Romanian Food",
    "Saudi Arabian": "Saudi Arabian Food",
    "Singaporean": "Singaporean Food",
    "Slovak": "Slovak Food",
    "Slovenian": "Slovenian Food",
    "Somali": "Somali Food",
    "South African": "South African Food",
    "Sri Lankan": "Sri Lankan Food",
    "Swiss": "Swiss Food",
    "Syrian": "Syrian Food",
    "Taiwanese": "Taiwanese Food",
    "Tanzanian": "Tanzanian Food",
    "Thai": "Thai Food",
    "Tunisian": "Tunisian Food",
    "Ukrainian": "Ukrainian Food",
    "Uruguayan": "Uruguayan Food",
    "Venezuelan": "Venezuelan Food",
    "Vietnamese": "Vietnamese Food",
    "Yemeni": "Yemeni Food",
    "Zambian": "Zambian Food",
    "Zimbabwean": "Zimbabwean Food",
}

# idk where to find the .env file
apiKey = ""

location = "Kelowna, BC, Canada"

with open(f"{location}.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Cuisine Type", "Name", "Address", "Website"])

    for cuisine, query in cuisine_types.items():
        # API rq
        data = search_restaurants(query, apiKey, location)

        for place in data.get("places", []):
            name = place["displayName"]["text"]
            address = place["formattedAddress"]
            website = place.get("websiteUri", "")

            writer.writerow([cuisine, name, address, website])
