#!/bin/bash

# Path to the text file containing city names
FILE_PATH="../demographicData/csv/cities.csv"

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

{
  read -r # ignore first line
  i=0
  while IFS=', ' read -r city state; do
    # Call your Python script with the city name as an argument
    python3 osm-get-city-restaurants.py "$city" "$state" cuisine &
    # echo $city $state
    bg_pids+=($!) # Store the PID of the background job
    ((i++))
    if (( i % 10 == 0 )); then
      echo "Sleeping for a while..."
      sleep 10 # Sleep for 5 seconds every 15 iterations
    fi

done 
}< "$FILE_PATH"

# Wait for all background jobs to finish
wait

echo "Done"

cleanup
