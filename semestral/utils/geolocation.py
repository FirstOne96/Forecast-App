"""
This module contains a function for reverse geocoding.
"""
from geopy.geocoders import Nominatim

def geolocator(lat, lon):
    geolocation = Nominatim(user_agent="weather_app")
    location = geolocation.reverse(f"{lat}, {lon}", language="en")
    if location is None:
        return f"{lat}, {lon}"
    address = location.raw.get("address", {})

    # Check for town, village, state or country (in order of priority)
    city = address.get("city")
    town = address.get("town")
    village = address.get("village")
    state = address.get("state")
    country = address.get("country")
    if city:
        return f"{city}, {country}"
    elif town:
        return f"{town}, {country}"
    elif village:
        return f"{village}, {country}"
    elif state and country:
        return f"{state}, {country}"
    elif country:
        return f"{country}"
    return f"{lat}, {lon}"
