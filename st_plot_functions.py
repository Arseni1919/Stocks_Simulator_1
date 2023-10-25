from globals import *

"""
All the functions that define plots for the streamlit.
"""


def plot_price_and_volume(info):
    bars_df = info['bars_df']
    selected_x_axis = info['selected_x_axis']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=bars_df[selected_x_axis], y=bars_df['close'], name="Price"), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=bars_df[selected_x_axis], y=bars_df['volume'], name='Volume', fill='tozeroy', mode='lines'),
        secondary_y=True)
    return fig