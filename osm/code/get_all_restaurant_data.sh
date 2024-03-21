#!/bin/bash

# Path to the text file containing city names
FILE_PATH="cities.txt"

echo "Fetching data for all cities"
# Loop through each line in the file
while IFS= read -r city
do
  # Call your Python script with the city name as an argument
  python3 osm-get-city-restaurants.py "$city" all &
done < "$FILE_PATH"

# Wait for all background jobs to finish
wait

echo "All cities have been processed."
