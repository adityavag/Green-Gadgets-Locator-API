import csv
import folium
import requests
import json
from math import radians, cos, sin, asin, sqrt
import geocoder

# Fetch current latitude and longitude
g = geocoder.ip('me')
current_lat, current_lon = g.latlng
# current_lat = float(sys.argv[1])
# current_lon = float(sys.argv[2])
print(current_lat, current_lon)
def distance(lat1, lat2, lon1, lon2):
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))
	r = 6371
	return(c * r)



with open('coordinates.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  
    
   
    coordinates_with_distance = []

    for column in csvreader:
        place=column[0]
        lat = float(column[1])
        lon = float(column[2])
        dist = distance(current_lat, lat, current_lon, lon)
        coordinates_with_distance.append((place,lat, lon, dist))

sorted_coordinates = sorted(coordinates_with_distance, key=lambda x: x[3])

for place,lat, lon, dist in sorted_coordinates:
    m = folium.Map(location=[lat,lon],zoom_start=12)
    break


# Set up your MapQuest API Key
api_key =   "4qEncwfFYnev0jvk5vSsHlEB91J3uDrI"

# Define the coordinates


# Generate the route using MapQuest API
route_url = f"http://www.mapquestapi.com/directions/v2/route?key={api_key}&from={lat},{lon}&to={current_lat},{current_lon}&unit=m"
response = requests.get(route_url)

# Check if the route was successfully generated
if response.status_code == 200:
    route_data = response.json()
    
    # Extract route coordinates
    route_coords = []
    for leg in route_data["route"]["legs"]:
        for maneuver in leg["maneuvers"]:
            route_coords.append((maneuver["startPoint"]["lat"], maneuver["startPoint"]["lng"]))
    
    # Create a map
    m = folium.Map(location=[lat, lon], zoom_start=12)


        # Add markers
        # Red marker
    folium.Marker(
        [lat, lon],
        popup="<i>E-Waste Facility</i>",
        tooltip="Click me",
        icon=folium.Icon(color='red')
    ).add_to(m)

    # Blue circle marker
    folium.CircleMarker(
        [current_lat, current_lon],
        radius=10,
        popup="<b>Your Location</b>",
        tooltip="Click me",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

    # Add the PolyLine using the route coordinates
    folium.PolyLine(route_coords, color='blue').add_to(m)

       
   
   
    # Save the map
    m.save('index.html')
    

else:
    print("Error generating route:", response.status_code)

output_list = []

i = 0
for place, lat, lon, dist in sorted_coordinates:
    i = i + 1

    output_list.append({"Address": place, "Distance": dist})

    if i == 4:
        break

# Write each address to a new line in the JSON file
with open('output.json', 'w') as json_file:
    json.dump(output_list, json_file)
    # json_file.write(',')



