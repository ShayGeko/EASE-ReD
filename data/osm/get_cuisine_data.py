import os
import sys

import pandas as pd


def main(input):
    cities = pd.read_csv(input)
    
    promises = []
    for city, state in cities.values:
        promises.append(get_city_restaurants_with_cuisine(city, state))
    
    for promise in promises:
        response = promise.result()
        print(response)
    

if __name__ == "__main__":
    input = sys.argv[1]
    main(input)