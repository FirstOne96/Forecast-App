"""
This module contains the callbacks for updating the weather data in the app.
"""
from dash import Output, Input, callback, State
from utils.data_processing import get_current_weather_data
from utils.geolocation import geolocator
from geopy.geocoders import Nominatim

# callback for updating weather data for Prague and London
@callback([Output("prague_temperature", "children"),
           Output("prague_icon", "src"),
           Output("london_temperature", "children"),
           Output("london_icon", "src")
           ],
          Input("update-interval", "n_intervals"),
          prevent_initial_call=False
          )
def update_prague_london_weather(n_intervals):
    # Coordinates for Prague and London
    prague_coords = (50.0755, 14.4378)
    london_coords = (51.5074, -0.1278)

    # Get current weather data for both locations
    prague_data = get_current_weather_data(*prague_coords)
    london_data = get_current_weather_data(*london_coords)

    # Validate API responses
    if prague_data is None :
        prague_temp = "N/A"
        prague_icon = ""
    else:
        prague_temp = f'{prague_data["temp"][0]}°C'
        prague_icon_value = prague_data['icon'].iloc[0] if not prague_data['icon'].empty else "man"
        prague_icon = f"./assets/icons/1st Set - Color/{prague_icon_value}.png"

    if london_data is None:
        london_temp = "N/A"
        london_icon = ""
    else:
        london_temp = f'{london_data["temp"][0]}°C'
        london_icon_value = london_data['icon'].iloc[0] if not london_data['icon'].empty else "man"
        london_icon = f'./assets/icons/1st Set - Color/{london_icon_value}.png'

    return prague_temp, prague_icon, london_temp, london_icon



@callback(
    [Output("current_temperature", "children"),
     Output("current_feels_like", "children"),
     Output("conditions", "children"),
     Output("forecast-icon", "src"),
     Output("location", "children"),

     Output("current_humidity", "children"),
     Output("current_windspeed", "children"),
     Output("current_cloudiness", "children"),
     Output("description", "children"),
     Output('store-initial-call', 'data')
     ],
    [Input("map", "clickData"),
     ],
    [State('store-initial-call', 'data')],
    prevent_initial_call=False
)
def update_weather(clickData, initial_call):
    if initial_call:
        lat, lon = 50.0755, 14.4378
    elif clickData is None:
        return (
            "Current weather data not available",
            "",
            "",
            f"./assets/icons/man.png",
            "Unknown Location",
            "",
            "",
            "",
            "No description available",
            False
        )
    else:
        lat, lon = clickData['latlng'].values()
    # Get current weather
    weather_data = get_current_weather_data(lat, lon)
    if weather_data is None or weather_data.empty:
        return (
            "Current weather data not available",
            "",
            "",
            f"./assets/icons/man.png",
            "Unknown Location",
            "",
            "",
            "",
            "No description available",
            False
        )

    current_location = geolocator(lat, lon)

    icon_value = weather_data['icon'].iloc[0] if not weather_data['icon'].empty else "man"
    icon_url = f'./assets/icons/1st Set - Color/{icon_value}.png'
    current_temperature = f'{weather_data["temp"].iloc[0]}°C' if not weather_data["temp"].empty else "N/A"
    current_feels_like = f'Feels like: {weather_data["feelslike"].iloc[0]}°C' if not weather_data[
        "feelslike"].empty else "N/A"
    current_conditions = f'{weather_data["conditions"].iloc[0]}' if not weather_data["conditions"].empty else "N/A"
    current_humidity = f'{weather_data["humidity"].iloc[0]}%' if not weather_data["humidity"].empty else "N/A"
    current_windspeed = f'{weather_data["windspeed"].iloc[0]} km/h' if not weather_data["windspeed"].empty else "N/A"
    current_cloudiness = f'{weather_data["cloudcover"].iloc[0]}%' if not weather_data["cloudcover"].empty else "N/A"
    description = weather_data["description"].iloc[0] if not weather_data["description"].empty else "N/A"

    return (current_temperature, current_feels_like, current_conditions, icon_url, current_location,
            current_humidity, current_windspeed, current_cloudiness, description, False)


# callback for updating the weather data for the city in the search bar
@callback(
    [Output("current_temperature", "children", allow_duplicate=True),
     Output("current_feels_like", "children", allow_duplicate=True),
     Output("conditions", "children", allow_duplicate=True),
     Output("forecast-icon", "src", allow_duplicate=True),
     Output("location", "children", allow_duplicate=True),
     Output("current_humidity", "children", allow_duplicate=True),
     Output("current_windspeed", "children", allow_duplicate=True),
     Output("current_cloudiness", "children", allow_duplicate=True),
     Output("description", "children", allow_duplicate=True)],
    [Input("search-bar", "n_submit")],  # This will trigger only when Enter is pressed
    [State("search-bar", "value")],
    prevent_initial_call=True  # Prevents callback from running on initial load
)
def update_weather_from_search(n_submit, value):
    if not value:
        return "Please enter a city name", "", "", "", "", "", "", "", ""

    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(value)

    if location is None:
        return "City not found", "", "", f"assets/icons/man.png", "", "", "", "", ""

    lat, lon = location.latitude, location.longitude

    # Use the existing get_current_weather_data function to fetch weather information
    weather_data = get_current_weather_data(lat, lon)

    if weather_data is None or weather_data.empty:
        return (
            "Current weather data not available",
            "",
            "",
            f"./assets/icons/man.png",
            f"{value}",
            "",
            "",
            "",
            "No description available"
        )

    current_location = value
    icon_value = weather_data['icon'].iloc[0] if not weather_data['icon'].empty else "man"
    icon_url = f'./assets/icons/1st Set - Color/{icon_value}.png'
    current_temperature = f'{weather_data["temp"].iloc[0]}°C' if not weather_data["temp"].empty else "N/A"
    current_feels_like = f'Feels like: {weather_data["feelslike"].iloc[0]}°C' if not weather_data["feelslike"].empty else "N/A"
    current_conditions = f'{weather_data["conditions"].iloc[0]}' if not weather_data["conditions"].empty else "N/A"
    current_humidity = f'{weather_data["humidity"].iloc[0]}%' if not weather_data["humidity"].empty else "N/A"
    current_windspeed = f'{weather_data["windspeed"].iloc[0]} km/h' if not weather_data["windspeed"].empty else "N/A"
    current_cloudiness = f'{weather_data["cloudcover"].iloc[0]}%' if not weather_data["cloudcover"].empty else "N/A"
    description = weather_data["description"].iloc[0] if not weather_data["description"].empty else "N/A"

    return (current_temperature, current_feels_like, current_conditions, icon_url, current_location,
            current_humidity, current_windspeed, current_cloudiness, description)
