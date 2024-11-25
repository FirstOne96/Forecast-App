# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objects as go
import dash_leaflet as dl
from geopy.geocoders import Nominatim
from datetime import datetime

def layout():
    app.layout = dbc.Container([
        # Header
        dbc.Row([
            dbc.Col(html.H2("Forecast", className="text-light", style={"textAlign": "left", "height": "30px", "margin": "0px", "padding-top": "10px"}),
                    width=6, ),
            dbc.Col(dbc.Input(id="search-bar", type="text", placeholder="Input a city",
                              style={"textAlign": "left", "height": "50px"}), width=2, className="mt-2",),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.P("Prague:", style={"fontSize": "17px", "fontWeight" : "bold", "width": "65px"}), width=5),
                            dbc.Col(html.Img(src="", id="prague_icon",
                                    style={"width": "25px", "height": "25px", "align" : "middle"}), width=1),
                            dbc.Col(html.P("Loading...", id="prague_temperature",
                                    style={"fontSize": "18px", "fontWeight": "bold", "align" : "middle"}), width=5)
                            ]),
                        ])
                ], style={"textAlign": "middle", "height": "50px"}),
                width=2, className="mt-2"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.P("London:", style={"fontSize": "17px", "fontWeight": "bold", "width": "65px"}), width=5),
                            dbc.Col(html.Img(src="", id="london_icon",
                                             style={"width": "25px", "height": "25px", "align" : "middle"}), width=1),
                            dbc.Col(html.P("Loading...", id="london_temperature",
                                           style={"fontSize": "18px", "fontWeight": "bold", "align" : "middle"}), width=5)
                        ]),
                    ])
                ], style={"textAlign": "left", "height": "50px"}),
                width=2, className="mt-2",
            ),
        ], justify="start", className="mt-2", style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
        # Update Interval
        dcc.Interval(
            id="update-interval",
            interval=10 * 60 * 1000,  # 10 minutes
            n_intervals=0,  # Starts immediately
        ),
        # Map
        dbc.Row([
            dbc.Col(dl.Map(id='map',
                           children=[
                               dl.TileLayer()
                           ], center=[50.0755, 14.4378], zoom=10, style={'height': '50vh'}),
                    width=6),
            # Card with current weather
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col(html.H5(children="Current Weather", className="card-title",
                                            style={"font-size": "20px"}), width=6),
                            dbc.Col(html.H5(children="...", id="location", className="card-title",
                                            style={"font-size": "20px", "text-align": "right"}), width=6),
                        ], style={"height": "22px"}),
                        html.H5(children=f"{datetime.now():%H:%M}", className="card-text", style={"font-size": "14px"}),
                    ]),
                    dbc.CardBody([

                        dbc.Row([
                            dbc.Col(html.Img(src="", id="forecast-icon", style={"width": "70px", "height": "70px"}),
                                    style={"max-width": "72px"}),
                            dbc.Col(
                                html.P(children="", id="current_temperature",
                                           className="card-text", style={"font-size": "60px"}),
                                width=4),
                            dbc.Col(
                                dbc.Row([
                                html.P(children="", id="conditions",style={"height": "5px", "text-weight" : "bolder"} ),
                                html.P(children="", id="current_feels_like",
                                       style={"font-size": "15px", "text-weight" : "lighter"}),
                        ]),),
                        ]),
                        #html.Hr(),
                        dbc.Row([
                           html.P(children="", id="description", style={"font-size": "15px"}),
                        ]),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col([
                                html.P("Humidity: ", style={"font-size": "15px"}),
                                html.P(children="", id="current_humidity", style={"font-size": "15px"}),
                            ]),
                            dbc.Col([
                                html.P("Wind speed: ", style={"font-size": "15px"}),
                                html.P(children="", id="current_windspeed", style={"font-size": "15px"}),
                            ], ),
                            dbc.Col([
                                html.P("Cloudiness: ", style={"font-size": "15px"}),
                                html.P(children="", id="current_cloudiness", style={"font-size": "15px"}),
                            ]),

                        ], className="g-1" ),
                    ]),
                ],  style={"height": "50vh"}),
            ], width=6)
        ], className="mt-2", style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
        # Middle section
        dbc.Row([
            dbc.Col(html.Div(id='forecast-title', className="text-info mt-2", children="7-days forecast"), width=12),
            dbc.Col(dcc.Graph(id='forecast-graph'), width=12),
        ], className="mt-2"),
        dbc.Row([
            dbc.Col([
                html.H5("Podrobnosti o počasí", className="text-warning"),
                dbc.Card([
                    dbc.CardBody([
                        html.P("Pocitová teplota: ...", id="feels-like"),
                        html.P("Vlhkost: ...", id="humidity"),
                        html.P("Oblačnost: ...", id="cloudiness"),
                    ])
                ])
            ], width=6),
            dbc.Col([
                html.H5("Chat GPT (Telling what to wear)", className="text-warning"),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Textarea(id="wear-suggestion", style={"width": "100%", "height": "200px"}),
                    ])
                ])
            ], width=6)
        ], className="mt-4")
    ], fluid=True)

def get_data(lat, lon):
    # Actual weather
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}?key=SEUTDBMZLD5MPNAAU6PJJQA2E&unitGroup=metric"
    response = requests.get(weather_url)
    data = response.json()
    return data


def world_map():
    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        showland=True,
        landcolor="rgb(212, 212, 212)",
        showocean=True, oceancolor="LightBlue",
        showcountries=True,
        showcoastlines=True,
        coastlinecolor="Gray",
    )
    fig.update_layout(
        height=300,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        autosize=True
    )
    return fig


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


def forecast_graph():
    pass



app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Weather App"
layout()

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
    prague_data = get_data(*prague_coords)
    london_data = get_data(*london_coords)

    # Validate API responses
    if not prague_data or "currentConditions" not in prague_data:
        prague_temp = "N/A"
        prague_icon = ""
    else:
        prague_temp = f'{prague_data["currentConditions"]["temp"]}°C'
        prague_icon = f'assets/icons/1st Set - Color/{prague_data["currentConditions"]["icon"]}.png'

    if not london_data or "currentConditions" not in london_data:
        london_temp = "N/A"
        london_icon = ""
    else:
        london_temp = f'{london_data["currentConditions"]["temp"]}°C'
        london_icon = f'assets/icons/1st Set - Color/{london_data["currentConditions"]["icon"]}.png'

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
     #Output("sunrise", "children"),
     #Output("sunset", "children")
     ],
    [Input("map", "clickData")],
    prevent_initial_call=False
)
def update_weather(clickData):
    if clickData is None:
        lat, lon = 50.0755, 14.4378
    else:
        lat, lon = clickData['latlng'].values()

    # Get current weather
    weather_data = get_data(lat, lon)
    if weather_data is None:
        return "Failed to get weather data", ""

    current_location = geolocator(lat, lon)
    icon_url = f"assets/icons/1st Set - Color/{weather_data['currentConditions']['icon']}.png"
    current_temperature = f'{weather_data["currentConditions"]["temp"]}°C'
    current_feels_like = f'Feels like: {weather_data["currentConditions"]["feelslike"]}°C'
    current_conditions = f'{weather_data["currentConditions"]["conditions"]}'
    current_humidity = f'{weather_data["currentConditions"]["humidity"]}%'
    current_windspeed = f'{weather_data["currentConditions"]["windspeed"]} km/h'
    current_cloudiness = f'{weather_data["currentConditions"]["cloudcover"]}%'
    description = weather_data["description"]
    try:
        sunrise = f'{weather_data["currentConditions"]["sunrise"]}'
        sunset = f'{weather_data["currentConditions"]["sunset"]}'
    except KeyError:
        sunrise = "N/A"
        sunset = "N/A"

    return (current_temperature, current_feels_like, current_conditions, icon_url, current_location,
            current_humidity, current_windspeed, current_cloudiness, description)


if __name__ == '__main__':
    app.run(debug=True)
