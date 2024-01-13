from dash import Dash, html, Input, Output

class DataAccessGUI:
    def __init__(self, api, enable_gui=False):
        self.api = api
        self.enable_gui = enable_gui
        
    def __enter__(self):
        if self.enable_gui == True:
            self.app = Dash(server=self.api.server, routes_pathname_prefix="/dash/")
            self.setup_layout()
            self.app.run(port=8050)
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
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