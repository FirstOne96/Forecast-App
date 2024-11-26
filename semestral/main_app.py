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
            dbc.CardGroup([
                dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                            # 1st day
                                    dbc.Col([
                                        dbc.Row([html.P(children="Today", id='date1')]),
                                        dbc.Row([
                                            dbc.Col([html.Img(src="", id="icon1")]),
                                            dbc.Col([dbc.Row([
                                                html.P(children="", id="temp1max")
                                            ]),
                                                dbc.Row([
                                                    html.P(children="", id="temp1min")
                                                ])
                                            ])
                                        ])
                                ], style={"cursor": "pointer"}, id="button-day1"),

                                # 2nd day
                                dbc.Col([
                                    dbc.Row([html.P(children="", id='date2')]),
                                    dbc.Row([
                                        dbc.Col([html.Img(src="", id="icon2")]),
                                        dbc.Col([dbc.Row([
                                            html.P(children="", id="temp2max")
                                        ]),
                                            dbc.Row([
                                                html.P(children="", id="temp2min")
                                            ])
                                        ])
                                    ])
                                ], style={"cursor": "pointer"}, id="button-day2"),
                                # 3rd day
                                dbc.Col([
                                    dbc.Row([html.P(children="", id='date3')]),
                                    dbc.Row([
                                        dbc.Col([html.Img(src="", id="icon3")]),
                                        dbc.Col([dbc.Row([
                                            html.P(children="", id="temp3max")
                                        ]),
                                            dbc.Row([
                                                html.P(children="", id="temp3min")
                                            ])
                                        ])
                                    ])
                                ], style={"cursor": "pointer"}, id="button-day3"),
                                # 4th day
                                dbc.Col([
                                    dbc.Row([html.P(children="", id='date4')]),
                                    dbc.Row([
                                        dbc.Col([html.Img(src="", id="icon4")]),
                                        dbc.Col([dbc.Row([
                                            html.P(children="", id="temp4max")
                                        ]),
                                            dbc.Row([
                                                html.P(children="", id="temp4min")
                                            ])
                                        ])
                                    ])
                                ], style={"cursor": "pointer"}, id="button-day4"),
                                # 5th day
                                dbc.Col([
                                    dbc.Row([html.P(children="", id='date5')]),
                                    dbc.Row([
                                        dbc.Col([html.Img(src="", id="icon5")]),
                                        dbc.Col([dbc.Row([
                                            html.P(children="", id="temp5max")
                                        ]),
                                            dbc.Row([
                                                html.P(children="", id="temp5min")
                                            ])
                                        ])
                                    ])
                                ], style={"cursor": "pointer"}, id="button-day5"),
                                # 6th day
                                dbc.Col([
                                    dbc.Row([html.P(children="", id='date6')]),
                                    dbc.Row([
                                        dbc.Col([html.Img(src="", id="icon6")]),
                                        dbc.Col([dbc.Row([
                                            html.P(children="", id="temp6max")
                                        ]),
                                            dbc.Row([
                                                html.P(children="", id="temp6min")
                                            ])
                                        ])
                                    ])
                                ], style={"cursor": "pointer"}, id="button-day6"),
                                # 7th day
                                dbc.Col([
                                    dbc.Row([html.P(children="", id='date7')]),
                                    dbc.Row([
                                        dbc.Col([html.Img(src="", id="icon7")]),
                                        dbc.Col([dbc.Row([
                                            html.P(children="", id="temp7max")
                                        ]),
                                            dbc.Row([
                                                html.P(children="", id="temp7min")
                                            ])
                                        ])
                                    ])
                                ], style={"cursor": "pointer"}, id="button-day7")
                            ]),
                        ]),

                ])
            ]),
        ], className="mt-2", style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
        # Bottom section
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
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}?key=SLU3NEK44RZHES6CQK7U7H7QS&unitGroup=metric"
    response = requests.get(weather_url)
    if response.status_code != 200:
        return None
    data = response.json()
    def parse_data():
        # Parse data
        nonlocal data
        description = data["description"]
        df = pd.DataFrame(data["currentConditions"])
        df.insert(0, "description", description)
        df.drop(columns=["dew", "datetimeEpoch", "snow", "snowdepth", "winddir", "pressure", "visibility", "solarradiation", "solarenergy", "uvindex", "stations", "sunriseEpoch", "sunsetEpoch"], inplace=True)
        return df

    res = parse_data()
    return res

def get_7day_forecast(lat, lon):
    # 7-day forecast
    forecast_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/next7days?unitGroup=metric&key=SLU3NEK44RZHES6CQK7U7H7QS&unitGroup=metric"
    response = requests.get(forecast_url)
    data = response.json()

    def parse_forecast_data():
        # Parse forecast data
        nonlocal data
        forecast = data["days"]
        df = pd.DataFrame(forecast)
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.drop(columns=["datetimeEpoch", "feelslikemax", "feelslike", "feelslikemin", "dew", "precip",
                              "precipcover", "snow", "snowdepth", "windgust", "winddir", "pressure",
                              "cloudcover", "visibility", "solarradiation", "solarenergy", "uvindex", "severerisk",
                              "sunriseEpoch", "sunsetEpoch", "stations", "source", "hours"])
        return df
    res = parse_forecast_data()
    return res

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
    if prague_data is None :
        prague_temp = "N/A"
        prague_icon = ""
    else:
        prague_temp = f'{prague_data["temp"][0]}°C'
        prague_icon = f'assets/icons/1st Set - Color/{prague_data["icon"][0]}.png'

    if london_data is None:
        london_temp = "N/A"
        london_icon = ""
    else:
        london_temp = f'{london_data["temp"][0]}°C'
        london_icon = f'assets/icons/1st Set - Color/{london_data["icon"][0]}.png'

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
    icon_url = f"assets/icons/1st Set - Color/{weather_data['icon'][0]}.png"
    current_temperature = f'{weather_data["temp"][0]}°C'
    current_feels_like = f'Feels like: {weather_data["feelslike"][0]}°C'
    current_conditions = f'{weather_data["conditions"][0]}'
    current_humidity = f'{weather_data["humidity"][0]}%'
    current_windspeed = f'{weather_data["windspeed"][0]} km/h'
    current_cloudiness = f'{weather_data["cloudcover"][0]}%'
    description = weather_data["description"][0]
    try:
        sunrise = f'{weather_data["sunrise"][0]}'
        sunset = f'{weather_data["sunset"][0]}'
    except KeyError:
        sunrise = "N/A"
        sunset = "N/A"

    return (current_temperature, current_feels_like, current_conditions, icon_url, current_location,
            current_humidity, current_windspeed, current_cloudiness, description)

@app.callback(
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
    forecast_data = get_7day_forecast(lat, lon)
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



if __name__ == '__main__':
    app.run(debug=True)
