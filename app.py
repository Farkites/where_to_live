import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import ClientsideFunction, Input, Output

import urllib.request, json

with urllib.request.urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as url:
    data_geo = json.loads(url.read().decode())

for feature in data_geo['features']:
    feature['id'] = feature['properties']['name']
path_datasets = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'
df_emissions = pd.read_csv(path_datasets + 'emissions.csv')
df_emission_0 = df_emissions.loc[df_emissions['year'] == 2000][['country_name', 'CO2_emissions']]

case_df = pd.read_csv(('../../Project1/data/Case.csv'))

nationality_options = ["Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Antiguans", "Argentinean",
                       "Tunisian", "Turkish", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbekistani",
                       "Venezuelan", "Vietnamese", "Welsh", "Yemenite", "Zambian", "Zimbabwean"]

nationality_options = [dict(label=nationality, value=nationality) for nationality in nationality_options]
hover_layout = html.Div([
    html.H4('Details of a location'),
    html.Div([
        html.A("This is the info on hover. TODO: substitute with fig")
    ],
        className="hover-details"
    )
],
    className="hover-details-container stack-top"
)

filters_layout = html.Div([
    html.H2('Select your filters'),
    html.Div([
        html.A('Applied filters:', className='preferencesText'),
        dcc.Dropdown(
            placeholder='Select Filters',
            id='filters_drop',
            options=nationality_options,
            clearable=False,
            className='dropdownMenu',
            multi=True
        )
    ],
        # className='stack-top'
    ),
],
    id="filters-container",
    className="stack-top col-2"
)

info_bar_layout = html.Div([
    html.H1("Where to live!", className="title"),
    html.H3("In this dashboard you can indicate your preferences and navigate the map to find the perfect city \
    for you to live", className="subtitle"),
    html.Div([
        html.Div([
            html.H6("Authors:"),
            html.P("Mario Rodríguez Ibáñez", className="author_name"),
            html.P("Diogo Acabado", className="author_name"),
            html.P("Doris Macean", className="author_name"),
            html.P("Daniel Philippi", className="author_name"),
        ]),
        html.Div([
            html.H6("Sources:"),
            html.P("asdfasdfajsdhlkansdfmcaksdfasdfasdf", className="source"),
            html.P("asdfasdvfasdfasxfqwrfasdfasdfvasd", className="source"),
            html.P("asdfasdvfasdfasdfasdfvgasdfa", className="source"),
            html.P("Dasdfasdfasdfasdfsvasdfvasdfasdfva", className="source"),
        ])
    ],
        style={"display": "flex", "align": "right"}
    ),
],
    className="stack-top info_bar row",
    id="info_bar"
)

selected_country_layout = html.Div([
    html.H4("Insert selected country"),
],
    id="selected_country",
    style={"display": "none"}
)
print(dcc.__version__)  # 0.6.0 or above is required

app = dash.Dash(__name__, external_stylesheets='')

suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div(id="width", style={'display': 'none'}),  # Just to retrieve the width of the window
        html.Div(id="height", style={'display': 'none'}),  # Just to retrieve the height of the window
        html.Div([
            dcc.Graph(id='map')
        ],
            style={'width': '100%', 'height': '100%'},
            className='background-map-container'
        )
    ],
        style={'display': 'flex'}
    ),
    filters_layout,
    info_bar_layout,
    selected_country_layout,
],
    id='page-content',
    style={'position': 'relative'},
)

#################
#   Figures     #
#################
selections = set()
country_names = {feature['properties']['name']: feature for feature in data_geo['features']}


def get_highlights(selections, geojson=data_geo, country_names=country_names):
    geojson_highlights = dict()
    for k in geojson.keys():
        if k != 'features':
            geojson_highlights[k] = geojson[k]
        else:
            geojson_highlights[k] = [country_names[selection] for selection in selections]
    return geojson_highlights


selected_country = ""


@app.callback(Output('selected_country', "style"),
              Output('selected_country', "children"),
              [Input('map', 'clickData')])
def update_selected_country(clickData):
    global selected_country
    location = ""
    if clickData is not None:
        location = clickData['points'][0]['location']
        if location != selected_country:
            selected_country = location
            style = {'display': 'block'}
        else:
            selected_country = ""
            location = ""
            style = {'display': 'none'}
    else:
        selected_country = ""
        location = ""
        style = {'display': 'none'}

    country_info = html.Div([
        html.H3(location),
        html.Canvas(width=300, height=300)
    ])
    return style, country_info


@app.callback(Output('map', 'figure'),
              [Input('filters_drop', 'value')],
              #              [Input('map', 'clickData')],
              Input('width', 'n_clicks'),
              Input('height', 'n_clicks'))
def update_map(filter_list, width, height):#clickData
    """if clickData is not None:
        location = clickData['points'][0]['location']

        if location not in selections:
            selections.add(location)
        else:
            selections.remove(location)

        print(selections)
    """
    fig = go.Figure()
    fig.add_trace(
        go.Choroplethmapbox(geojson=data_geo,
                            locations=df_emission_0['country_name'],
                            z=df_emission_0['CO2_emissions'],
                            zmin=0,
                            colorscale=[[0, "rgb(255,255,255)"], [1, "rgb(145, 100, 162)"]]
                            )
    )
    """
    if len(selections) > 0:
        highlights = get_highlights(selections, data_geo)
        fig.add_trace(
            go.Choroplethmapbox(geojson=highlights,
                                colorscale=[[0, "rgba(0,0,0,255)"], [1, "rgba(0, 0, 0, 255)"]],
                                locations=df_emission_0['country_name'])
        )
        print(highlights)
    """
    mapbox_token = "pk.eyJ1IjoiZmFya2l0ZXMiLCJhIjoiY2ttaHYwZnQzMGI0cDJvazVubzEzc2lncyJ9.fczsOA4Hfgdf8_bAAZkdYQ"
    all_plots_layout = dict(
        mapbox=dict(style="light",
                    layers=[dict(source=feature,
                                 below='traces',
                                 type='fill',
                                 fill=dict(outlinecolor='gray')
                                 ) for feature in data_geo['features']],
                    accesstoken=mapbox_token,
                    ),
        autosize=False,
        width=width,
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo_bgcolor='rgba(0,0,0,0)',

    )
    fig.layout = all_plots_layout
    """
    if len(selections) > 0:
        highlights = get_highlights(selections, data_geo)
        fig.update_mapboxes(dict(
                                layers=[dict(source=highlight,
                                              below='traces',
                                              type='fill',
                                              fill=dict(outlinecolor='red')
                               ) for highlight in highlights]))
    """
    return fig


# Get window size function
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='get_window_width'
    ),

    Output('width', 'n_clicks'),
    [Input('url', 'href')],

)

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='get_window_height'
    ),
    Output('height', 'n_clicks'),
    [Input('url', 'href')],
)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
