import plotly.graph_objects as go
from plotly.subplots import make_subplots

import re
#from app import city_info_num, city_info_num_agg

#city_info_num = city_info_num
#city_info_num_agg = city_info_num_agg


def custom_dims_plot_deprecated(location, dims_selected, city_info_num, city_info_num_agg):
    dims_selected = [re.sub('high |low ', '', dim) for dim in dims_selected]

    vals_city = city_info_num.loc[city_info_num['City'] == location, dims_selected].values.tolist()[0]
    vals_agg = city_info_num_agg[dims_selected].values.tolist()

    data = [
        go.Bar(
            y=dims_selected,
            x=vals_agg,
            name='Median',
            orientation='h',
            marker=dict(
                color='rgba(58, 71, 80, 0.6)'
            )
        ),
        go.Bar(
            y=dims_selected,
            x=vals_city,
            name='Selected',
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)'
            )
        )
    ]

    fig = go.Figure(data)

    fig.update_layout(barmode='group')
    return fig


def custom_dims_plot(location, dims_selected, city_info_num, city_info_num_agg):
    dims_selected = [re.sub('high |low ', '', dim) for dim in dims_selected]
    print(dims_selected)
    vals_city = city_info_num.loc[city_info_num['City'] == location, dims_selected].values.tolist()[0]
    vals_agg = city_info_num_agg[dims_selected].values.tolist()

    fig = make_subplots(
        rows=len(dims_selected), cols=1,
        subplot_titles=(dims_selected)
    )
    legend = [False for _ in range(len(dims_selected))]
    legend[0] = True

    for idx, dim in enumerate(dims_selected):

        # crate traces
        trace1 = go.Bar(
            y=[dim],
            x=[vals_agg[idx]],
            name='Median',  legendgroup='Median',
            orientation='h',
            marker=dict(
                color='rgba(58, 71, 80, 0.6)'
            ),
            showlegend=legend[idx]
        )
        trace2 = go.Bar(

            y=[dim],
            x=[vals_city[idx]],
            name='Selected', legendgroup='Selected',
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)'
            ),
            showlegend=legend[idx]
            )

        fig.add_trace(trace1, row=idx+1, col=1)
        fig.add_trace(trace2, row=idx+1, col=1)


    fig.update_layout(barmode='group')
    fig.update_yaxes(visible=False)

    return fig

