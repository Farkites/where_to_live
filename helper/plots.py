import plotly.graph_objects as go
import re
#from app import city_info_num, city_info_num_agg

#city_info_num = city_info_num
#city_info_num_agg = city_info_num_agg


def custom_dims_plot(location, dims_selected, city_info_num, city_info_num_agg):
    dims_selected = [re.sub('high |low ', '', dim) for dim in dims_selected]
    print(dims_selected)
    vals_city = city_info_num.loc[city_info_num['City'] == location, dims_selected].values.tolist()[0]
    vals_agg = city_info_num_agg[dims_selected].values.tolist()


    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=dims_selected,
        x=vals_agg,
        name='Median',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)'
        )
    )
    )
    fig.add_trace(go.Bar(
        y=dims_selected,
        x=vals_city,
        name='Selected',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)'
        )
    )
    )

    fig.update_layout(barmode='group')
    return fig