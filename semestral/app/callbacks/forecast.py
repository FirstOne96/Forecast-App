"""
This file contains the callbacks for updating the 7-day forecast based on the location clicked on the map or the city
"""
from dash import Output, Input, callback, State
from utils.data_processing import get_forecast_data
from geopy.geocoders import Nominatim


@callback(
    [
        Output('date1', 'children'), Output('icon1', 'src'), Output('temp1max', 'children'), Output('temp1min', 'children'),
        Output('date2', 'children'), Output('icon2', 'src'), Output('temp2max', 'children'), Output('temp2min', 'children'),
        Output('date3', 'children'), Output('icon3', 'src'), Output('temp3max', 'children'), Output('temp3min', 'children'),
        Output('date4', 'children'), Output('icon4', 'src'), Output('temp4max', 'children'), Output('temp4min', 'children'),
        Output('date5', 'children'), Output('icon5', 'src'), Output('temp5max', 'children'), Output('temp5min', 'children'),
        Output('date6', 'children'), Output('icon6', 'src'), Output('temp6max', 'children'), Output('temp6min', 'children'),
        Output('date7', 'children'), Output('icon7', 'src'), Output('temp7max', 'children'), Output('temp7min', 'children')
    ],
        [Input('map', 'clickData')
    ],
)
def update_forecast(clickData):
    # Get 7-day forecast
    if clickData is None:
        lat, lon = 50.0755, 14.4378
    else:
        lat, lon = clickData['latlng'].values()
    forecast_data = get_forecast_data(lat, lon)
    if forecast_data is None:
        return "Failed to get forecast data",

    outputs = []
    for day in range(7):
        if day == 0:
            date = "Today"
        else:
            date = forecast_data["datetime"][day].strftime("%d.%m")
        icon = f'assets/icons/1st Set - Color/{forecast_data["icon"][day]}.png'
        temp_max = f'{forecast_data["tempmax"][day]}°C'
        temp_min = f'{forecast_data["tempmin"][day]}°C'

        outputs.extend([date, icon, temp_max, temp_min])

    return outputs


# callback for updating the 7-day forecast for the city in the search bar
@callback(
[
        Output('date1', 'children', allow_duplicate=True), Output('icon1', 'src', allow_duplicate=True), Output('temp1max', 'children', allow_duplicate=True), Output('temp1min', 'children', allow_duplicate=True),
        Output('date2', 'children', allow_duplicate=True), Output('icon2', 'src', allow_duplicate=True), Output('temp2max', 'children', allow_duplicate=True), Output('temp2min', 'children', allow_duplicate=True),
        Output('date3', 'children', allow_duplicate=True), Output('icon3', 'src', allow_duplicate=True), Output('temp3max', 'children', allow_duplicate=True), Output('temp3min', 'children', allow_duplicate=True),
        Output('date4', 'children', allow_duplicate=True), Output('icon4', 'src', allow_duplicate=True), Output('temp4max', 'children', allow_duplicate=True), Output('temp4min', 'children', allow_duplicate=True),
        Output('date5', 'children', allow_duplicate=True), Output('icon5', 'src', allow_duplicate=True), Output('temp5max', 'children', allow_duplicate=True), Output('temp5min', 'children', allow_duplicate=True),
        Output('date6', 'children', allow_duplicate=True), Output('icon6', 'src', allow_duplicate=True), Output('temp6max', 'children', allow_duplicate=True), Output('temp6min', 'children', allow_duplicate=True),
        Output('date7', 'children', allow_duplicate=True), Output('icon7', 'src', allow_duplicate=True), Output('temp7max', 'children', allow_duplicate=True), Output('temp7min', 'children', allow_duplicate=True)
    ],
    [Input("search-bar", "n_submit")],  # This will trigger only when Enter is pressed
    [State("search-bar", "value")],
    prevent_initial_call=True  # Prevents callback from running on initial load
)
def update_forecast_from_search(n_submit, value):
    if not value:
        return "Please enter a city name", "", "", "", "", "", "", "", ""

    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(value)

    if location is None:
        return "City not found", "", "", "", "", "", "", "", ""

    lat, lon = location.latitude, location.longitude

    # Use the existing get_data function to fetch weather information
    forecast_data = get_forecast_data(lat, lon)

    outputs = []
    for day in range(7):
        if day == 0:
            date = "Today"
        else:
            date = forecast_data["datetime"][day].strftime("%d.%m")
        icon = f'assets/icons/1st Set - Color/{forecast_data["icon"][day]}.png'
        temp_max = f'{forecast_data["tempmax"][day]}°C'
        temp_min = f'{forecast_data["tempmin"][day]}°C'

        outputs.extend([date, icon, temp_max, temp_min])

    return outputs
