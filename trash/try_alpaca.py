import dotenv
import os
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.live import StockDataStream

import matplotlib.pyplot as plt


def historical_data():
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
    request_params = StockBarsRequest(
        symbol_or_symbols=["SPY"],
        timeframe=TimeFrame.Day,
        start="2022-01-01 00:00:00"
    )
    bars = client.get_stock_bars(request_params)
    bars_df = bars.df
    bars_df[['open', 'close', 'high', 'low']].plot()
    plt.show()
    print(bars_df)


def life_data():
    stock_stream = StockDataStream(API_KEY, SECRET_KEY)

    async def bar_callback(bar):
        for property_name, value in bar:
            print(f"\"{property_name}\": {value}")

    # Subscribing to bar event
    symbol = "TSLA"
    stock_stream.subscribe_bars(bar_callback, symbol)

    stock_stream.run()


def trading():
    trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)
    # Getting account information and printing it
    account = trading_client.get_account()
    for property_name, value in account:
        print(f"\"{property_name}\": {value}")


def main():
    pass






if __name__ == '__main__':
    dotenv.load_dotenv()
    API_KEY = os.environ['API_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    main()
