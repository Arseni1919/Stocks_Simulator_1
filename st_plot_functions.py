import numpy as np
import pandas as pd

from globals import *

"""
All the functions that define plots for the streamlit.
"""


def plot_asset_volumes(**kwargs):
    data = kwargs['data']
    selected_dates = kwargs['selected_dates']
    asset = kwargs['asset']
    if 'ignore_first_minute' in kwargs:
        ignore_first_minute = kwargs['ignore_first_minute']
    else:
        ignore_first_minute = False

    asset_prices = []
    asset_volumes = []

    for date in selected_dates:
        if ignore_first_minute:
            volumes = np.sum(data[date][asset]['volume'][1:])
        else:
            volumes = np.sum(data[date][asset]['volume'])
        asset_volumes.append(volumes)

    plot_dict = {
        f'{asset}_volume': asset_volumes,
        f'dates': selected_dates
    }
    plot_df = pd.DataFrame.from_dict(plot_dict)
    fig2 = px.line(plot_df, x="dates", y=f'{asset}_volume')
    st.plotly_chart(fig2, use_container_width=True)


def plot_asset_prices(**kwargs):
    data = kwargs['data']
    selected_dates = kwargs['selected_dates']
    asset = kwargs['asset']
    if 'ignore_first_minute' in kwargs:
        ignore_first_minute = kwargs['ignore_first_minute']
    else:
        ignore_first_minute = False

    asset_prices = []
    asset_volumes = []

    for date in selected_dates:
        if ignore_first_minute:
            prices = np.sum(data[date][asset]['price'][1:])
        else:
            prices = np.sum(data[date][asset]['price'])
        asset_prices.append(prices)

    plot_dict = {
        f'{asset}_price': asset_prices,
        f'dates': selected_dates
    }
    plot_df = pd.DataFrame.from_dict(plot_dict)
    fig1 = px.line(plot_df, x="dates", y=f'{asset}_price')
    st.plotly_chart(fig1, use_container_width=True)


def plot_asset(**kwargs):
    data = kwargs['data']
    selected_dates = kwargs['selected_dates']
    asset = kwargs['asset']
    if 'ignore_first_minute' in kwargs:
        ignore_first_minute = kwargs['ignore_first_minute']
    else:
        ignore_first_minute = False

    asset_prices = []
    asset_volumes = []

    for date in selected_dates:
        if ignore_first_minute:
            prices = np.sum(data[date][asset]['price'][1:])
            volumes = np.sum(data[date][asset]['volume'][1:])
        else:
            prices = np.sum(data[date][asset]['price'])
            volumes = np.sum(data[date][asset]['volume'])
        asset_prices.append(prices)
        asset_volumes.append(volumes)


    plot_dict = {
        f'{asset}_volume': asset_volumes,
        f'{asset}_price': asset_prices,
        f'dates': selected_dates
    }
    plot_df = pd.DataFrame.from_dict(plot_dict)
    fig1 = px.line(plot_df, x="dates", y=f'{asset}_price')
    st.plotly_chart(fig1, use_container_width=True)
    fig2 = px.line(plot_df, x="dates", y=f'{asset}_volume')
    st.plotly_chart(fig2, use_container_width=True)


def plot_price_and_volume(info):
    bars_df = info['bars_df']
    selected_x_axis = info['selected_x_axis']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=bars_df[selected_x_axis], y=bars_df['close'], name="Price"), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=bars_df[selected_x_axis], y=bars_df['volume'], name='Volume', fill='tozeroy', mode='lines'),
        secondary_y=True)
    return fig


def plot_dollar_volumes_many_days(**kwargs):
    dates_list = kwargs['dates_list']
    data = kwargs['data']
    s_date = kwargs['s_date']
    f_date = kwargs['f_date']
    selected_assets = kwargs['selected_assets']
    selected_dates = dates_list[dates_list.index(s_date):dates_list.index(f_date)]

    plot_dict = {'Dates': selected_dates}
    n_of_datapoints = 0
    for asset in selected_assets:
        plot_dict[asset] = []
        for date in selected_dates:
            day_volumes = data[date][asset]['volume'][1:]
            day_prices = data[date][asset]['price'][1:]
            day_dollar_volumes = np.multiply(day_volumes, day_prices)
            plot_dict[asset].append(np.sum(day_dollar_volumes))
            n_of_datapoints += 1

    plot_df = pd.DataFrame.from_dict(plot_dict)
    # n_of_datapoints = sum([len(plot_df[column]) for column in plot_df])
    fig = px.line(plot_df, x='Dates', y=selected_assets, render_mode='svg')
    st.plotly_chart(fig, use_container_width=True)
    # st.line_chart(plot_df, x='Dates', y=selected_assets)


def plot_dollar_volumes_one_day(**kwargs):
    data = kwargs['data']
    selected_assets = kwargs['selected_assets']
    selected_date = kwargs['selected_date']

    plot_dict = {}
    for asset in selected_assets:
        day_volumes = data[selected_date][asset]['volume'][1:]
        day_prices = data[selected_date][asset]['price'][1:]
        day_dollar_volumes = np.multiply(day_volumes, day_prices)
        plot_dict[asset] = day_dollar_volumes

    plot_df = pd.DataFrame.from_dict(plot_dict)
    fig = px.line(plot_df, render_mode='svg')
    st.plotly_chart(fig, use_container_width=True)
    # n_of_datapoints = sum([len(plot_df[column]) for column in plot_df])
    # st.line_chart(plot_df)


def plot_prices_one_day(**kwargs):
    data = kwargs['data']
    selected_assets = kwargs['selected_assets']
    selected_date = kwargs['selected_date']

    plot_dict = {}
    for asset in selected_assets:
        day_prices = data[selected_date][asset]['price'][1:]
        plot_dict[asset] = day_prices

    plot_df = pd.DataFrame.from_dict(plot_dict)
    fig = px.line(plot_df, render_mode='svg')
    st.plotly_chart(fig, use_container_width=True)
