#!/bin/bash

# Path to the text file containing city names
FILE_PATH="cities.txt"

declare -a bg_pids

# Function to kill all background jobs
cleanup() {
    echo "Terminating background jobs..."
    for pid in "${bg_pids[@]}"; do
        kill "$pid" 2>/dev/null
    done
}

# Trap INT and TERM signals to call the cleanup function
trap cleanup INT TERM


echo "Fetching data for all cities"
# Loop through each line in the file
while IFS= read -r city
do
  # Call your Python script with the city name as an argument
  python3 osm-get-city-restaurants.py "$city" cuisine &
  bg_pids+=($!) # Store the PID of the background job

done < "$FILE_PATH"

# Wait for all background jobs to finish
wait

echo "Done"

cleanup
