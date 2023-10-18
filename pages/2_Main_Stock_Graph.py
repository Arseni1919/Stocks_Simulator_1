import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
from datetime import timezone
import pandas as pd
import numpy as np
# from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.live import StockDataStream
from globals import stocks_names_list
from indicator_functions import *


st.set_page_config(layout="wide")
API_KEY = st.secrets.alpaca_api_key
SECRET_KEY = st.secrets.alpaca_secret_key


# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# FUNCTIONS
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #

def get_time_period_start(time_period):
    # cols_names = ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
    start_datetime = None
    if time_period == '1D':
        start_datetime = datetime.datetime.today() - datetime.timedelta(days=1)
    elif time_period == '5D':
        start_datetime = datetime.datetime.today() - datetime.timedelta(days=5)
    elif time_period == '1M':
        start_datetime = datetime.datetime.today() - datetime.timedelta(days=30)
    elif time_period == '6M':
        start_datetime = datetime.datetime.today() - datetime.timedelta(days=180)
    elif time_period == 'YTD':
        start_datetime = datetime.date.today()
    elif time_period == '1Y':
        start_datetime = datetime.datetime.today() - datetime.timedelta(days=365)
    elif time_period == '5Y':
        start_datetime = datetime.datetime.today() - datetime.timedelta(days=1825)
    elif time_period == 'MAX':
        start_datetime = datetime.datetime.today() - datetime.timedelta(days=1825)
    else:
        raise RuntimeError('incorrect time period')
    return start_datetime


@st.cache(allow_output_mutation=True)
def historical_data(stock, time_period):
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
    request_params = StockBarsRequest(
        symbol_or_symbols=[stock],
        timeframe=TimeFrame.Minute,
        # start="2018-01-01 00:00:00"
        start=get_time_period_start(time_period)
    )
    bars = client.get_stock_bars(request_params)
    curr_bars_df = bars.df
    curr_bars_df['datetime'] = [index[1] for index in curr_bars_df.index]
    curr_bars_df['num'] = [num for num in range(len(curr_bars_df.index))]
    # return bars.df
    return curr_bars_df


def set_indicator_graph(name, data_to_show):
    st.write(f'### {name}')
    curr_fig = px.line(bars_df, x=selected_x_axis, y=data_to_show)
    curr_fig.update_layout(height=indicators_height, margin=dict(l=10, r=10, b=10, t=10, pad=4))
    curr_fig.update_yaxes(title=None)
    st.plotly_chart(curr_fig, theme=None, use_container_width=True)


def alert_of_stock_exchange():
    # 2:30 pm to 9 pm - UTC
    # col1, col2 = st.columns(2)
    now = datetime.datetime.now(timezone.utc)
    start_time = now.replace(hour=14, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=21, minute=0, second=0, microsecond=0)
    st.info(f'The current date and time is **{now.strftime("%H:%M")}** ({now.strftime("%m/%d/%y")})')
    # st.info(f'{start_time}, {end_time}')
    if start_time < now < end_time:
        st.success('#### The US markets are opened now!')
    else:
        st.error('#### The US markets are closed now.')

# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ST
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Sidebar
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# st.sidebar.write('## Select a stock:')
selected_stock = st.sidebar.selectbox("Select a stock:", stocks_names_list)  # , label_visibility='hidden'
rsi_bool = st.sidebar.checkbox('rsi', value=True, disabled=False)
ma_bool = st.sidebar.checkbox('ma', value=False, disabled=False)

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Main
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

alert_of_stock_exchange()
st.write(f'# Stock Analysis - {selected_stock}')

cols_names = ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
selected_time_period = st.radio("Time Period:", cols_names, horizontal=True)
selected_x_axis = st.radio("X-axis:", ['datetime', 'num'], horizontal=True, index=1)

bars_df = historical_data(selected_stock, selected_time_period)

fig = make_subplots(rows=2, cols=1, print_grid=True, shared_xaxes=True, row_heights=[0.7, 0.3])
fig.add_trace(go.Scatter(x=bars_df[selected_x_axis], y=bars_df['close'], name='Close', mode='lines'), row=1, col=1)
fig.add_trace(go.Scatter(x=bars_df[selected_x_axis], y=bars_df['volume'], name='Volume', fill='tozeroy', mode='lines+markers'), row=2, col=1)
fig.update_layout(height=500, margin=dict(l=10, r=10, b=10, t=10, pad=10), legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=0.17
))

st.plotly_chart(fig, theme=None, use_container_width=True)
expander = st.expander(f"See The '{selected_stock}' Data")
expander.write(bars_df)

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Indicators
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

indicators_height = 200

if rsi_bool:
    set_indicator_graph('RSI', rsi_calc(bars_df['close']))

if ma_bool:
    set_indicator_graph('MA', macd_func(bars_df['close']))

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #






# fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2], name="(1,2)"), row=1, col=2)
#
# fig = px.line(bars_df, x=selected_x_axis, y='close', title='Close Prices')
# st.plotly_chart(fig, theme=None, use_container_width=True)
# fig = px.line(bars_df, x=selected_x_axis, y='volume', title='Volume')
