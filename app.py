import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import ClientsideFunction, Input, Output, State
import plotly.express as px

import urllib.request, json

with urllib.request.urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as url:
    data_geo = json.loads(url.read().decode())

for feature in data_geo['features']:
    feature['id'] = feature['properties']['name']
path_datasets = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'
df_emissions = pd.read_csv(path_datasets + 'emissions.csv')
df_emission_0 = df_emissions.loc[df_emissions['year'] == 2000][['country_name', 'CO2_emissions']]

nationality_options = ["Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Antiguans", "Argentinean",
                       "Tunisian", "Turkish", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbekistani",
                       "Venezuelan", "Vietnamese", "Welsh", "Yemenite", "Zambian", "Zimbabwean"]

nationality_options = [dict(label=nationality, value=nationality) for nationality in nationality_options]

# datasets needed for plots
data = pd.read_csv('data/age_group.csv')
index_df = pd.read_csv('data/Index.csv')
com = pd.read_csv('data/com.csv')

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
    html.Div([
        html.H3('Select your filters', style={'display': 'inline'}),
        html.Span([
            html.Span(className="Select-arrow", title="is_open")
        ],
            className='Select-arrow-zone',
            id='select_filters_arrow'
        ),
    ],

    ),
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
        id='dropdown_menu_applied_filters'
    ),
],
    id="filters_container",
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
    html.Div([
        html.H3("Insert selected country", id="title_selected_country"),
        html.Span('X', id="x_close_selection")
    ]),

    dcc.Graph(id='funnel-graph'),
    dcc.Graph(id='radar'),
    #dcc.Graph(id='bubble')
],
    id="selected_country",
    style={"display": "none"}
)

hovered_country_layout = html.Div([
    html.H4("Insert selected country"),
],
    id="hovered_country",
    style={"display": "none"},
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
            dcc.Graph(id='map', clear_on_unhover=True, config={'doubleClick': 'reset'})
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
    hovered_country_layout,
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


@app.callback(Output('dropdown_menu_applied_filters', 'style'),
              Output('select_filters_arrow', 'title'),
              Input('select_filters_arrow', 'n_clicks'),
              State('select_filters_arrow', 'title'))
def toggle_applied_filters(n_clicks, data):
    style = {'display': 'none'}
    if n_clicks is not None:
        if data == 'is_open':
            style = {'display': 'none'}
            data = 'is_closed'
        else:
            style = {'display': 'block'}
            data = 'is_open'

    return style, data


selected_country = ""
x_close_selection_clicks = -1


@app.callback(Output('selected_country', "style"),
              Output('title_selected_country', "children"),
              Output('funnel-graph', "figure"),
              Output('radar', "figure"),
              #Output('bubble', "figure"),
              [Input('map', 'clickData')],
              Input('x_close_selection', 'n_clicks'))
def update_selected_country(clickData, n_clicks):
    global selected_country
    global x_close_selection_clicks
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

    if n_clicks != x_close_selection_clicks:
        style = {'display': 'none'}
        x_close_selection_clicks = n_clicks

    return style, location, update_demo(location), update_radar(location)#, bubble_happiness(location)


def update_demo(Country):
    if Country == "All Countries":
        df_plot = data.copy()
    else:
        df_plot = data[data['Country'] == Country]

    trace1 = go.Bar(x=df_plot.Country, y=df_plot['Under 5'], name='Under 5')
    trace2 = go.Bar(x=df_plot.Country, y=df_plot['Aged 5-14'], name='Aged 5-14')
    trace3 = go.Bar(x=df_plot.Country, y=df_plot['Aged 15-24'], name='Aged 15-24')
    trace4 = go.Bar(x=df_plot.Country, y=df_plot['Aged 25-64'], name='Aged 25-64')
    trace5 = go.Bar(x=df_plot.Country, y=df_plot['Over 65'], name='Over 65')

    return {
        'data': [trace1, trace2, trace3, trace4, trace5],
        'layout':
            go.Layout(
                title='Age demographics for {}'.format(Country),
                orientation=180,
                barmode='stack',
                #margin=go.layout.Margin(
                #    l=0,  # left margin
                #    r=0,  # right margin
                #    b=0,  # bottom margin
                #    t=0  # top margin
                #),
                width=350,
                height=300,
            ),

    }


# radar plot to compare index values
def update_radar(City):
    # creating a subset dataframe

    # select from:
    # Quality of Life Index, Purchasing Power Index, Safety Index, Health Care Index,
    # Cost of Living Index, Property Price to Income Ratio,	Traffic Commute Time Index
    # Pollution Index, Climate Index
    selected = index_df[
        ['Country', 'Safety Index', 'Health Care Index', 'Cost of Living Index', 'Climate Index', 'Pollution Index']]

    select_df = selected[selected['City'] == City]

    Row_list = []
    r=[]
    # get list of values for each country selected
    # Iterate over each row
    for index, rows in select_df.iterrows():
        for i in range(len(cat)):
            # Create list for the current 
            r.append(rows[cat[i]])

            # append the list to the final list
        Row_list.append(r)
        Row_list=list(np.concatenate(Row_list).flat)

    # list of attributes to be compared
    categories = ['Safety Index', 'Health Care Index', 'Cost of Living Index', 'Climate Index', 'Pollution Index']
    categories = [*categories, categories[0]]

    return go.Figure(
        data=[
            go.Barpolar(
                        r=Row_list,
                        theta=categories,
                        name=City,
                        marker_color=["#E4FF87",'#e1bbfa','#fabbf3', '#709BFF', '#b6faf8', '#e1e6e2', '#FFAA70', '#FFDF70', '#B6FFB4',],
                        marker_line_color='white',
                        hoverinfo=['theta']*9,
                        opacity=0.7,
                        base=0)
            
        ],
        layout=[go.Layout(
                    title=go.layout.Title(text=City),
                    polar_angularaxis_rotation=90,
                    polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    angularaxis=dict(linewidth=3, showline=False,showticklabels=True),
                    radialaxis=dict(showline=False,
                    showticklabels=False,
                    linewidth=2,
                    gridcolor='white',
                    gridwidth=2)),
                    showlegend=True,
            
            )])


def bubble_happiness(Country):
    return px.scatter(com, x="Logged GDP per capita", y="Healthy life expectancy",
                      size="population", color="Ladder score",
                      hover_name='Country name', log_x=True, size_max=60)


hovered_country = ""


@app.callback(Output('hovered_country', "style"),
              Output('hovered_country', "children"),
              [Input('map', 'hoverData')])
def update_hovered_country(hoverData):
    global hovered_country
    location = ""
    if hoverData is not None:
        location = hoverData['points'][0]['location']
        if location != hovered_country:
            hovered_country = location
            style = {'display': 'block'}
        else:
            hovered_country = ""
            location = ""
            style = {'display': 'none'}
    else:
        hovered_country = ""
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
def update_map(filter_list, width, height):  # clickData
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
                            colorscale=[[0, "rgb(255,255,255)"], [1, "rgb(145, 100, 162)"]],
                            hovertemplate="<extra></extra>"
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

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='move_hover'
    ),
    Output('hovered_country', 'title'),
    [Input('map', 'hoverData')],
)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
