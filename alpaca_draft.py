# from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.live import StockDataStream
import datetime
import dotenv
import os


dotenv.load_dotenv()
API_KEY = os.environ['API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
print(client)


def get_time_period_start(time_period):
    # cols_names = ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
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


def life_data():
    stock_stream = StockDataStream(API_KEY, SECRET_KEY)

    async def bar_callback(bar):
        for property_name, value in bar:
            print(f"\"{property_name}\": {value}")

    # Subscribing to bar event
    symbol = "TSLA"
    stock_stream.subscribe_bars(bar_callback, symbol)

    stock_stream.run()