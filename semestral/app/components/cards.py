"""
This module contains functions that create cards for the dashboard.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

def create_header_prague():
    return (dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.P("Prague:", style={"fontSize": "17px", "fontWeight": "bold", "width": "65px"}),
                        width=5),
                dbc.Col(html.Img(src="", id="prague_icon",
                                 style={"width": "25px", "height": "25px", "align": "middle"}), width=1),
                dbc.Col(html.P("Loading...", id="prague_temperature",
                               style={"fontSize": "18px", "fontWeight": "bold", "align": "middle"}), width=5)
            ]),
        ])
    ], style={"textAlign": "middle", "height": "50px"}),
    )


def create_header_london():
    return (dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.P("London:", style={"fontSize": "17px", "fontWeight": "bold", "width": "65px"}),
                    width=5),
                dbc.Col(html.Img(src="", id="london_icon",
                                 style={"width": "25px", "height": "25px", "align": "middle"}), width=1),
                dbc.Col(html.P("Loading...", id="london_temperature",
                               style={"fontSize": "18px", "fontWeight": "bold", "align": "middle"}),
                        width=5)
            ]),
        ])
    ], style={"textAlign": "left", "height": "50px"}))


def create_current_weather():
    return (dbc.Card([
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
                        html.P(children="", id="conditions",
                               style={"height": "5px", "text-weight": "bolder"}),
                        html.P(children="", id="current_feels_like",
                               style={"font-size": "15px", "text-weight": "lighter"}),
                    ]), ),
            ]),
            # html.Hr(),
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

            ], className="g-1"),
        ]),
    ], style={"height": "50vh"}))


def create_middle_section():
    return (dbc.CardGroup([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    # 1st day
                    dbc.Col([
                        dbc.Button([
                            dbc.Row([html.P(children="", id='date1')]),
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
                        ], style={"cursor": "pointer", "background-color": "transparent",
                                  "border-color": "transparent"}, id="button-day1", n_clicks=0),
                    ]),
                    # 2nd day
                    dbc.Col([
                        dbc.Button([
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
                        ], style={"cursor": "pointer", "background-color": "transparent",
                                  "border-color": "transparent"}, id="button-day2", n_clicks=0),
                    ]),
                    # 3rd day
                    dbc.Col([
                        dbc.Button([
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
                        ], style={"cursor": "pointer", "background-color": "transparent",
                                  "border-color": "transparent"}, id="button-day3", n_clicks=0),
                    ]),
                    # 4th day
                    dbc.Col([
                        dbc.Button([
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
                        ], style={"cursor": "pointer", "background-color": "transparent",
                                  "border-color": "transparent"}, id="button-day4", n_clicks=0),
                    ]),
                    # 5th day
                    dbc.Col([
                        dbc.Button([
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
                        ], style={"cursor": "pointer", "background-color": "transparent",
                                  "border-color": "transparent"}, id="button-day5", n_clicks=0),
                    ]),
                    # 6th day
                    dbc.Col([
                        dbc.Button([
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
                        ], style={"cursor": "pointer", "background-color": "transparent",
                                  "border-color": "transparent"}, id="button-day6", n_clicks=0),
                    ]),
                    # 7th day
                    dbc.Col([
                        dbc.Button([
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
                        ], style={"cursor": "pointer", "background-color": "transparent",
                                  "border-color": "transparent"}, id="button-day7", n_clicks=0),
                    ]),
                ]),
            ]),

        ])
    ]))
