from globals import *


@st.cache_data
def load_big_json():
    f = open('data/data.json')
    data = json.load(f)
    return data


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


@st.cache_data
def historical_data(stock, time_period):
    API_KEY = st.secrets.alpaca_api_key
    SECRET_KEY = st.secrets.alpaca_secret_key
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


def set_indicator_graph(x_data, y_data):
    fig = make_subplots()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name="Price"))
    # curr_fig.update_layout(height=indicators_height, margin=dict(l=10, r=10, b=10, t=10, pad=4))
    return fig


def plot_price_and_volume(info):
    bars_df = info['bars_df']
    selected_x_axis = info['selected_x_axis']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=bars_df[selected_x_axis], y=bars_df['close'], name="Price"), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=bars_df[selected_x_axis], y=bars_df['volume'], name='Volume', fill='tozeroy', mode='lines'),
        secondary_y=True)
    return fig



