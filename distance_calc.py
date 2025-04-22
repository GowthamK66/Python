from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Initialize the geocoder
geolocator = Nominatim(user_agent="distance_calculator")

# Define the locations as place names or addresses
location1 = "chennai central"
location2 = "avadi"

# Get the latitude and longitude coordinates for the locations
location1_coords = geolocator.geocode(location1)
location2_coords = geolocator.geocode(location2)

if location1_coords and location2_coords:
    # Extract the latitude and longitude
    coords1 = (location1_coords.latitude, location1_coords.longitude)
    coords2 = (location2_coords.latitude, location2_coords.longitude)

    # Calculate the distance using the Haversine formula
    distanceK = geodesic(coords1, coords2).kilometers
    distanceM = geodesic(coords1, coords2).miles

    print(f"The distance between {location1} and {location2} is {distanceK} kilometers.")
    print(f"The distance between {location1} and {location2} is {distanceM} miles.")
else:
    print("One or both of the locations could not be geocoded.")
