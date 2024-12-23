"""
This module contains the layout of the application.
"""
from dash import dcc, html
import dash_bootstrap_components as dbc
from app.components.cards import create_header_prague
from app.components.cards import create_header_london
from app.components.cards import create_current_weather
from app.components.cards import create_middle_section
from app.components.graph_component import create_graph
from app.components.map_component import create_map


def create_layout():
    return dbc.Container([
        dcc.Store(id='store-initial-call', data=True),
        # Header
        dbc.Row([
            dbc.Col(html.H2("Forecast", className="text-light",
                            style={"textAlign": "left", "height": "30px", "margin": "0px", "padding-top": "10px"}),
                    width=6),
            dbc.Col(dbc.Input(id="search-bar", type="text", placeholder="Input a city",
                              style={"textAlign": "left", "height": "50px"}), width=2, className="mt-2"),
            dbc.Col(create_header_prague(), width=2, className="mt-2"),
            dbc.Col(create_header_london(), width=2, className="mt-2"),
        ], justify="start", className="mt-2",
            style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
        # Update Interval
        dcc.Interval(
            id="update-interval",
            interval=10 * 60 * 1000,  # 10 minutes
            n_intervals=0,  # Starts immediately
        ),
        dbc.Row([
            # Map
            dbc.Col(create_map(), width=6),
            # Current weather
            dbc.Col(create_current_weather(), width=6)
        ], justify="start", className="mt-2",
            style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
        # Middle section
        dbc.Row(create_middle_section(), justify="start", className="mt-2",
            style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
        # Graph
        dbc.Row([
            dbc.Col(create_graph(), width=12)
        ], justify="start", className="mt-2",
            style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
        # Bottom section
        #dbc.Row(create_bottom_section(), className="mt-4")
    ], fluid=True)
