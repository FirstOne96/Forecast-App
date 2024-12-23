"""
Main file for running the app
"""
from app import app
from app.layout import create_layout

app.layout = create_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
