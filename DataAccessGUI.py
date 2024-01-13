from dash import Dash, html, Input, Output
from flask import request

class DataAccessGUI:
    def __init__(self, api, enable_gui=False):
        self.api = api
        self.enable_gui = enable_gui
        
    def __enter__(self):
        if self.enable_gui == True:
            self.app = Dash(server=self.api.server, routes_pathname_prefix="/dash/")
            self.app.run_server(debug=False)
            self.api.server.testing = True
            self.setup_layout()
        return self
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        return False
        
    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1('Dash App in a Class'),
            html.Button('Click Me', id='my-button'),
            html.Div(id='output-container')
        ])

        @self.app.callback(
            Output('output-container', 'children'),
            Input('my-button', 'n_clicks')
        )
        def update_output(n_clicks):
            if n_clicks is None:
                return 'Button not clicked yet'
            else:
                return f'Button clicked {n_clicks} times'