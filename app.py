import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import ClientsideFunction, Input, Output, State
import plotly.express as px

import urllib.request, json

path_datasets = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'


city_info_bin = pd.read_csv('data_bool_geo_final.csv')
preferences_list = list(city_info_bin.drop(columns=["City", "Country", "Lat", "Long"]).columns)
filters = [dict(label=parameter, value=parameter) for parameter in preferences_list]



# datasets needed for plots
data = pd.read_csv('age_group.csv')
index_df = pd.read_csv('Index.csv')
com = pd.read_csv('col.csv')

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
        html.P('Applied filters:', id='preferencesText'),
        dcc.Dropdown(
            placeholder='Select Filters',
            id='filters_drop',
            options=filters,
            clearable=False,
            className='dropdownMenu',
            multi=True
        )
    ],
        id='dropdown_menu_applied_filters'
    ),
],
    id="filters_container",
    style={"display": "block"},
    className="stack-top col-3"
)

initial_popup_layout = html.Div([
    html.H1("Where to live!", className="title"),
    html.H3("In this dashboard you can indicate your preferences and navigate the map to find the perfect city \
    for you to live."),
    html.H3("Instructions:"),
    html.P("First, select your preferences using the filters on the top left corner."),
    html.P("Then navigate through the map and click on the locations to see more details."),
    html.H3("Click anywhere to start!"),

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
        style={"display": "flex", "align": "right", "bottom": "10%"}
    ),
],
    id="initial_popup"
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
    style={"display": "block"},
    id="info_bar"
)

selected_location_layout = html.Div([
    html.Div([
        html.H3("Insert selected location", id="title_selected_location"),
        html.Span('X', id="x_close_selection")
    ]),

    dcc.Graph(id='funnel-graph'),
    dcc.Graph(id='radar'),
    #dcc.Graph(id='bubble')
],
    id="selected_location",
    style={"display": "none"}
)

hovered_location_layout = html.Div([
    html.H4("Insert selected location"),
],
    id="hovered_location",
    style={"display": "none"},
)

print(dcc.__version__)  # 0.6.0 or above is required

app = dash.Dash(__name__, external_stylesheets='')

suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    initial_popup_layout,
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
        id="map_container",
        style={'display': 'flex'}
    ),
    filters_layout,
    info_bar_layout,
    selected_location_layout,
    hovered_location_layout,
],
    id='page-content',
    style={'position': 'relative'},
)

#################
#   Figures     #
#################
selections = set()

@app.callback(Output('initial_popup', 'style'),
              Input('initial_popup', 'n_clicks'))
def close_initial_popup(n_clicks):
    show_flex = {'display': 'flex'}
    show_block = {'display': 'block'}
    hide = {'display': 'none'}
    if n_clicks is not None:
        return hide
    else:
        return show_block


@app.callback(Output('dropdown_menu_applied_filters', 'style'),
              Output('select_filters_arrow', 'title'),
              Input('select_filters_arrow', 'n_clicks'),
              State('select_filters_arrow', 'title'))
def toggle_applied_filters(n_clicks, state):
    style = {'display': 'none'}
    if n_clicks is not None:
        if state == 'is_open':
            style = {'display': 'none'}
            state = 'is_closed'
        else:
            style = {'display': 'block'}
            state = 'is_open'

    return style, state


selected_location = ""
x_close_selection_clicks = -1


@app.callback(Output('selected_location', "style"),
              Output('title_selected_location', "children"),
              Output('funnel-graph', "figure"),
              Output('radar', "figure"),
              [Input('map', 'clickData')],
              Input('x_close_selection', 'n_clicks'))
def update_selected_location(clickData, n_clicks):
    global selected_location
    global x_close_selection_clicks
    location = ""
    if clickData is not None:
        location = clickData['points'][0]['text']
        if location != selected_location:
            selected_location = location
            style = {'display': 'block'}
        else:
            selected_location = ""
            location = ""
            style = {'display': 'none'}
    else:
        selected_location = ""
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
def update_radar(Country):
    # creating a subset dataframe

    # select from:
    # Quality of Life Index, Purchasing Power Index, Safety Index, Health Care Index,
    # Cost of Living Index, Property Price to Income Ratio,	Traffic Commute Time Index
    # Pollution Index, Climate Index
    selected = index_df[
        ['Country', 'Safety Index', 'Health Care Index', 'Cost of Living Index', 'Climate Index', 'Pollution Index']]

    Row_list = []

    # get list of values for each country selected
    # Iterate over each row
    for index, row in selected.iterrows():
        # Create list for the current
        r = [row['Safety Index'], row['Health Care Index'], row['Cost of Living Index'], row['Climate Index'],
             row['Pollution Index']]

        # append the list to the final list
        Row_list.append(r)

    # list of attributes to be compared
    categories = ['Safety Index', 'Health Care Index', 'Cost of Living Index', 'Climate Index', 'Pollution Index']
    categories = [*categories, categories[0]]

    country_1 = Row_list[0]
    country_2 = Row_list[1]
    country_3 = Row_list[2]
    country_1 = [*country_1, country_1[0]]
    country_2 = [*country_2, country_2[0]]
    country_3 = [*country_3, country_3[0]]

    return go.Figure(
        data=[
            go.Scatterpolar(r=country_1, theta=categories, fill='toself', name='Country 1'),
            # go.Scatterpolar(r=country_2, theta=categories, fill='toself', name='Country 2'),
            # go.Scatterpolar(r=country_3, theta=categories, fill='toself', name='Country 3')
        ],
        layout=go.Layout(
            title=go.layout.Title(text='Country'),
            polar={'radialaxis': {'visible': True}},
            showlegend=True,
            #margin=go.layout.Margin(
            #    l=0,  # left margin
            #    r=0,  # right margin
            #    b=0,  # bottom margin
            #    t=0  # top margin
            #),
            width=350,
            height=300,
        )
    )


def bubble_happiness(Country):
    return px.scatter(com, x="Logged GDP per capita", y="Healthy life expectancy",
                      size="population", color="Ladder score",
                      hover_name='Country name', log_x=True, size_max=60)


hovered_location = ""


@app.callback(Output('hovered_location', "style"),
              Output('hovered_location', "children"),
              [Input('map', 'hoverData')])
def update_hovered_location(hoverData):
    global hovered_location
    location = ""
    if hoverData is not None:
        location = hoverData['points'][0]['text']
        if location != hovered_location:
            hovered_location = location
            style = {'display': 'block'}
        else:
            hovered_location = ""
            location = ""
            style = {'display': 'none'}
    else:
        hovered_location = ""
        location = ""
        style = {'display': 'none'}

    location_info = html.Div([
        html.H3(location),
        html.Canvas(width=300, height=300)
    ])

    return style, location_info


@app.callback(Output('page-content', 'style'),
              Input('width', 'n_clicks'),
              Input('height', 'n_clicks'))
def set_page_size(width, height):
    return {'width': width, 'height': height}


@app.callback(Output('map', 'figure'),
              [Input('filters_drop', 'value')],
              Input('width', 'n_clicks'),
              Input('height', 'n_clicks'))
def update_map(filter_list, width, height):
    fig = go.Figure()

    if filter_list is not None and len(filter_list) != 0:

        filters = []
        for f in filter_list:
            filters.append(city_info_bin[f])
        highlighted = city_info_bin.loc[np.all(filters, 0), ['City', 'Country', 'Lat', 'Long']]
        not_highlighted = city_info_bin.loc[~np.all(filters, 0), ['City', 'Country', 'Lat', 'Long']]

        # Highlighted
        fig.add_trace(
            go.Scattermapbox(
                lat=highlighted.Lat,
                lon=highlighted.Long,
                text=highlighted.City,
                name="Compatible location",
                mode="markers",
                marker=go.scattermapbox.Marker(
                    size=15,
                    opacity=0.9,
                    color='#F3D576',
                ),
                hovertemplate="<extra></extra>",
            )
        )
    else:
        not_highlighted = city_info_bin

    # Not highlighted
    fig.add_trace(
        go.Scattermapbox(
            lat=not_highlighted.Lat,
            lon=not_highlighted.Long,
            text=not_highlighted.City,
            name="Incompatible location",
            mode="markers",
            marker=go.scattermapbox.Marker(
                size=10,
                opacity=0.9,
                color='#333333',
            ),
            hovertemplate="<extra></extra>",
        )
    )

    mapbox_token = "pk.eyJ1IjoiZmFya2l0ZXMiLCJhIjoiY2ttaHYwZnQzMGI0cDJvazVubzEzc2lncyJ9.fczsOA4Hfgdf8_bAAZkdYQ"
    all_plots_layout = dict(
        mapbox=dict(style="mapbox://styles/farkites/ckn0lwfm319ae17o5jmk3ckvu",
                    accesstoken=mapbox_token,
                    ),
        legend=dict(
                    bgcolor="rgba(51,51,51,0.6)",
                    yanchor="top",
                    y=0.35,
                    xanchor="left",
                    x=0,
                    font=dict(
                                family="Open Sans",
                                size=15,
                                color="white",
                            ),
                    ),
        autosize=False,
        width=width,
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo_bgcolor='rgba(0,0,0,0)',

    )
    fig.layout = all_plots_layout

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
    Output('hovered_location', 'title'),
    [Input('map', 'hoverData')],
)

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
