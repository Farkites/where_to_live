import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1(children='Where to live!',
                    style={'textAlign': 'center'}
                    ),
            html.H2('In this dashboard you can indicate your preferences and \
                     navigate the map to find the perfect city for you to live')
        ],
            className='header',
            style={'padding-top': '1%'}
        )],
        className='row'
    ),
    # Body
    html.Div([
        # Navigation Bar
        html.Div([
            html.A('Home', href='/main', className='navButton'),
            html.A('Map', href='/map_page', className='navButton'),
            html.A('Compare your profile', href='/profile', className='navButton'),
            html.A('Preferences', href='/preferences', className='navButton'),
            html.A('Countries Stats', href='/countries', className='navButton')
        ],
            className='mainNav'
        ),
        # Map Section
        html.Div([
            html.Div([
                html.A('Start!', href='/map_page')
            ],
                className='startButton'
            )
        ],
            style={"display": "flex",
                   "align-content": "flex",
                    "position": "relative"},
        )
    ],
        className='body',
    )
])
