"""
This module contains the function create_graph which creates a card with a graph and a date-time header.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html

def create_graph():
    return (dbc.Card([
                    dbc.CardHeader([
                        html.H5("Today", id="date-time")
                    ], style={"height": "40px"}),
                    dbc.CardBody([
                        dcc.Graph(id="graph", style={"height": "40vh"})
                    ])
                ]))
