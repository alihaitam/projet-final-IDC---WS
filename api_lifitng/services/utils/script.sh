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

# URL-encoded query: construct where {?s ?p ?o}
CONSTRUCT="construct%20WHERE%20%7B%20%3Fs%20%3Fp%20%3Fo%20%7D%20"

# Second API call with lat and lon
curl --header "Accept: text/turtle" "http://localhost/service/tomtom/findPlace?categorySet=9377&lat=${lat}&lon=${lon}&query=${CONSTRUCT}" > ../api_lifting/venues.ttl

echo "Results saved to venues.ttl"
