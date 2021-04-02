import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

##################################################################################################

# datasets needed for plots
data = pd.read_csv('age_group.csv')
index_df = pd.read_csv('Index.csv')
com = pd.read_csv('com.csv')

country_options = data['Country'].tolist()

app = dash.Dash()

app.layout = html.Div([
    html.H2("Age demographics"),
    html.Div(
        [
            dcc.Dropdown(
                id="Country",
                options=[{
                    'label': i,
                    'value': i
                } for i in country_options],
                value='All countries'
                #multi=True
                )
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
    dcc.Graph(id='radar'),
    dcc.Graph(id='bubble')
])

# plotting age groups for each country
@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Country', 'value')])

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
            barmode='stack')
            }

@app.callback(
    dash.dependencies.Output('radar', 'figure'),
    [dash.dependencies.Input('Country', 'value')])

# radar plot to compare index values
def update_radar(Country):
    # creating a subset dataframe

    # select from:
    # Quality of Life Index, Purchasing Power Index, Safety Index, Health Care Index,
    # Cost of Living Index, Property Price to Income Ratio,	Traffic Commute Time Index
    # Pollution Index, Climate Index
    selected = index_df[['Country','Safety Index', 'Health Care Index', 'Cost of Living Index', 'Climate Index','Pollution Index']]

    Row_list = []

    # get list of values for each country selected
    # Iterate over each row
    for index, row in selected.iterrows():
        # Create list for the current
        r =[row['Safety Index'], row['Health Care Index'], row['Cost of Living Index'], row['Climate Index'], row['Pollution Index']]

        # append the list to the final list
        Row_list.append(r)

    # list of attributes to be compared
    categories = ['Safety Index', 'Health Care Index', 'Cost of Living Index', 'Climate Index','Pollution Index']
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
            #go.Scatterpolar(r=country_2, theta=categories, fill='toself', name='Country 2'),
            #go.Scatterpolar(r=country_3, theta=categories, fill='toself', name='Country 3')
        ],
        layout=go.Layout(
            title=go.layout.Title(text='Country'),
            polar={'radialaxis': {'visible': True}},
            showlegend=True
            )
        )


@app.callback(
    dash.dependencies.Output('bubble', 'figure'),
    [dash.dependencies.Input('Country', 'value')])

# bubble plot for happiness and related indicators
def bubble_happiness(Country):
    return px.scatter(com, x="Logged GDP per capita", y="Healthy life expectancy",
                 size="population", color="Ladder score",
                 hover_name='Country name', log_x=True, size_max=60)

    #fig.update_layout({
        #'paper_bgcolor':'rgba(0,0,0,0)',
        #'plot_bgcolor':'rgba(0,0,0,0)'}
    #)


if __name__ == '__main__':
    app.run_server(debug=True)


