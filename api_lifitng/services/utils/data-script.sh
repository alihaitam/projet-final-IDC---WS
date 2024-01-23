#!/bin/bash

# Check if a city name argument is provided
if [ -z "$1" ]; then
    echo "No city name provided."
    exit 1
fi

# Use the first argument as the city name
city_name="$1"

# OpenWeatherMap API call to get lat and lon
response=$(curl -s "http://api.openweathermap.org/geo/1.0/direct?q=${city_name}&appid=d898a496f42850738d98ee8f6c3bf71a")

# Extract latitude and longitude using grep and awk
lat=$(echo $response | grep -o '"lat":[^,]*' | awk -F ':' '{print $2}')
lon=$(echo $response | grep -o '"lon":[^,]*' | awk -F ':' '{print $2}')

# Check if lat and lon are available
if [ -z "$lat" ] || [ -z "$lon" ]; then
    echo "Could not find the location for the specified city."
    exit 1
fi

# Define an array of categorySet values
categorySets=(7315146 7342 9937002 9377 7314003 7318 9376 7315 7374 7317)

# URL-encoded query: construct where {?s ?p ?o}
CONSTRUCT="construct%20WHERE%20%7B%20%3Fs%20%3Fp%20%3Fo%20%7D%20"

# Create a 'data' directory in the current directory (if it doesn't already exist)
mkdir -p ../api_lifitng/data

# Initialize a variable to hold the concatenated data
concatenated_data=""

# Loop over each categorySet and fetch data
for categorySet in "${categorySets[@]}"
do
    data=$(curl --header "Accept: text/turtle" "http://localhost/service/tomtom/findPlace?categorySet=${categorySet}&lat=${lat}&lon=${lon}&query=${CONSTRUCT}")
    
    # Append data, skipping the first three lines for all but the first file
    if [ -z "$concatenated_data" ]; then
        concatenated_data="$data"
    else
        concatenated_data+=$'\n'$(echo "$data" | tail -n +4)
    fi
done

# Write the concatenated data to city_venues.ttl
echo "$concatenated_data" > "../api_lifitng/data/city_venues.ttl"

echo "All data concatenated into ../api_lifitng/data/city_venues.ttl"
