import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import ClientsideFunction, Input, Output, State
import plotly.express as px
from ipywidgets import widgets
from helper.plots import custom_dims_plot

import urllib.request, json

# name mapper
with open('mapping_dict_final_binary.json', 'r') as f:
    dimension_mapper_binary = json.load(f)

with open('mapping_dict_final.json', 'r') as f:
    dimension_mapper = json.load(f)

city_info_bin = pd.read_csv('data_bool_geo_final.csv')

filters = []
for k,v in dimension_mapper_binary.items():
    filters.append(dict(label=v, value=k))

temperature_df = pd.read_csv('city_temperature.csv')

# datasets needed for plots
data = pd.read_csv('df_final.csv')
city_info_num = data.copy()

colnames_to_lower = dict(zip(
    city_info_num.drop(columns=["City", "Country", "Lat", "Long"]).columns,
    map(str.lower, city_info_num.drop(columns=["City", "Country", "Lat", "Long"]).columns)

))
city_info_num.rename(columns=colnames_to_lower, inplace=True)

city_info_num_agg = city_info_num.drop(columns=['City', 'Country']).apply(np.median)

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

    # dcc.Graph(id='radar'),
    dcc.Graph(id='bubble'),
    dcc.Graph(id='custom_dims_plot'),
    dcc.Graph(id='heatmap')

],
    id="selected_location",
    style={"display": "none"}
)

hovered_location_layout = html.Div([
    html.Div([
        html.H3("city", id='hover_title'),
        dcc.Graph("radar")
    ]),
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


@app.callback(Output('bubble','clickData'),
                [Input('map', 'clickData')])
def link_data(clickData):
    if clickData is not None:
            location = clickData['points'][0]['text']
    ###### 

@app.callback(Output('selected_location', "style"),
              Output('title_selected_location', "children"),
              Output('custom_dims_plot', "figure"),
              Output('bubble','figure'),
              [Input('map', 'clickData')],
              Input('x_close_selection', 'n_clicks'),
              [Input('filters_drop', 'value')],
              [Input('bubble', 'selectedData'),
                Input('bubble', 'clickData')],
                [State('bubble','figure')])

def update_selected_location(clickData, n_clicks, dims_selected,bubbleSelect,bubbleClick,bubbleState):
    global selected_location
    global x_close_selection_clicks
    location = ""
    if clickData is not None or dims_selected is not None:
        if clickData is not None:
            location = clickData['points'][0]['text']
        if len(location) != 0:
            selected_location = location
            style = {'display': 'block'}
        else:
            selected_location = ""
            location = selected_location
            style = {'display': 'none'}
    else:
        selected_location = ""
        location = ""
        style = {'display': 'none'}

    if n_clicks != x_close_selection_clicks:
        style = {'display': 'none'}
        selected_location = ""
        x_close_selection_clicks = n_clicks
    
    if bubbleSelect is not None or bubbleClick is not None or bubbleState is not None:
        bubble_fig = update_color(bubbleSelect, bubbleClick, bubbleState) 
    else:
        bubble_fig = build_figure()

    return style, location, update_custom_dims_plot(location, dims_selected), bubble_fig


def update_custom_dims_plot(location, dims_selected):
    if dims_selected is None:
        dims_selected = ['tourism']
    if len(location) == 0:
        return go.Figure()
    fig = custom_dims_plot(location, dims_selected, city_info_num, city_info_num_agg, dimension_mapper)
    return fig

@app.callback(Output('heatmap', 'figure'),
              Input('url', 'href'))
def update_heatmap(_):
    x = temperature_df['City'].unique()
    y = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    z = [[round(temperature_df.loc[(temperature_df['City'] == temperature_df['City'].unique()[j]) \
                                   & (temperature_df['Month'] == i), 'AvgTemperature'].values[0], 1)
          for j in range(len(x))] for i in range(1, len(y) + 1)]

    hovertext = list()
    for xi, xx in enumerate(x):
        hovertext.append(list())
        for yi, yy in enumerate(y):
            hovertext[-1].append('City: {}<br />Month: {}<br />Temperature: {}'.format(xx, yy, z[yi][xi]))

    data = [go.Heatmap(x=temperature_df['Month'],
                       y=temperature_df['City'],
                       z=temperature_df['AvgTemperature'].values.tolist(), zmin=-20, zmax=40,
                       colorscale='RdBu',
                       reversescale=True,
                       hoverinfo='text',
                       colorbar=dict(thickness=10),
                       text=hovertext)]

    layout = go.Layout(title='Avg. Temperature by City and Month',
                       xaxis=dict(
                           tickmode='array',
                           tickvals=[i for i in range(1, 13)],
                           ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
                       )

    fig = go.Figure(data=data, layout=layout)

    return fig


hovered_location = ""


@app.callback(Output('hovered_location', "style"),
              Output('radar', 'figure'),
              Output('hover_title', 'children'),
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

    return style, update_radar(location), location

# radar plot to compare index values
def update_radar(city):
    # creating a subset dataframe
    df = data[['City', 'Cost of Living Index',
               'Purchasing Power Index', 'Safety Index', 'Health Care Index',
               'Pollution Index']]

    # categories
    cat = df.columns[1:].tolist()

    select_df = df[df['City'] == city]

    Row_list = []
    r = []
    # Iterate over each row
    for index, rows in select_df.iterrows():
        for i in range(len(cat)):
            # Create list for the current
            r.append(rows[cat[i]])

            # append the list to the final list
        Row_list.append(r)
        Row_list = list(np.concatenate(Row_list).flat)

    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=Row_list,
        theta=cat,
        name=city,
        marker_color=['rgb(243,203,70)'] * 6,
        marker_line_color='white',
        hoverinfo=['theta'] * 9,
        opacity=0.7,
        base=0
    ))

    fig.add_trace(go.Barpolar(
        r=df.mean(axis=0).tolist(),
        theta=cat,
        name='Average',
        marker_color=['#986EA8'] * 6,
        marker_line_color='white',
        hoverinfo=['theta'] * 9,
        opacity=0.7,
        base=0
    ))

    fig.update_layout(
        title='',
        font_size=12,
        #hoverlabel = 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        polar=dict(
        bgcolor='rgba(0,0,0,0)',
        angularaxis=dict(linewidth=3, showline=False,showticklabels=True),
        radialaxis=dict(showline=False,
                        showticklabels=False,
                linewidth=2,
                gridcolor='rgba(0,0,0,0)',
                gridwidth=2)))

    return fig


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

md = data[['City', 'Employment', 'Startup', 'Tourism', 'Housing',
       'Transport', 'Health', 'Food', 'Internet Speed',
       'Access to Contraception', 'Gender Equality', 'Immigration Tolerance',
       'LGBT Friendly', 'Nightscene', 'Beer', 'Festival']].copy()
    
for column in md.columns.tolist()[1:]:
    md['{column}.'.format(column=column)] = pd.qcut(md[column].rank(method='first'), 4, labels=False)


# Build parcats dimensions
quartiles = ['Startup.', 'Internet Speed.', 'Gender Equality.','Immigration Tolerance.','LGBT Friendly.','Nightscene.',]


dimensions = [dict(values=md[label], label=label) for label in quartiles]

# Build colorscale
color = np.zeros(len(md), dtype='uint8')
colorscale = [[0, 'gray'], [1, 'rgb(243,203,70)']]

size = md['Employment']*20


# bubble plot related indicators
def build_figure():

    # Build figure as FigureWidget
    fig = go.Figure(
        data=[go.Scatter(x=md['Health'], y=md['Housing'],
        text=md['City'],
        hovertemplate=md['City'], 
        marker={'color': '#986EA8','size':size}, mode='markers', selected={'marker': {'color': 'rgb(243,203,70)'}},
        unselected={'marker': {'opacity': 0.3}}), go.Parcats(
            domain={'y': [0, 0.4]}, 
            dimensions=dimensions,
            line={'colorscale': colorscale, 'cmin': 0,
                'cmax': 1, 'color': color,'shape': 'hspline'})
        ])

    fig.update_layout(
            font_color='white',
            height=800, xaxis={'title': 'Employment'},
            yaxis={'title': 'Health', 'domain': [0.6, 1]},
            dragmode='lasso', hovermode='closest',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=False,
            bargap=0.35)
    return fig 

#app = dash.Dash(prevent_initial_callbacks=True)
#app.layout = html.Div([dcc.Graph(figure=build_figure(), id="graph")])


    # Update color callback
def update_color(selectedData, clickData, fig):
        
    selection = None

    # Update selection based on which event triggered the update.
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if trigger == 'bubble.clickData':
        selection = [point["pointNumber"] for point in clickData["points"]]
    if trigger == 'bubble.selectedData':
        selection = [point["pointIndex"] for point in selectedData["points"]]
    # Update scatter selection
    fig["data"][0]["selectedpoints"] = selection
    # Update parcats colors
    new_color = np.zeros(len(md), dtype='uint8')
    new_color[selection] = 1
    fig["data"][1]["line"]["color"] = new_color
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
