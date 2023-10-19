import random
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import os
import datetime
from datetime import timezone
import json

# import pymongo
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim
# from torch.autograd import Variable

# from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.live import StockDataStream

load_dotenv()

assets_names_list = [
    'SPY',
    'IVV',
    'VOO',
    'QQQ',
    'DIA',
    'VIXY',
    'AAPL',
    'AMZN',
    'GOOG',
    'GOOGL',
    'MSFT',
    'FB',
    'NFLX',
    'TSLA',
    'VCSH',
    'IGSB',
    'VCIT',
    'LQD',
    'SHY',
    'IEF',
    'GOVT',
    'TLT',
    'GLD',
    'IAU',
]

assets_names_dict = {
    'SPY': {'info': 'ETF on Stocks'},
    'IVV': {'info': 'ETF on Stocks'},
    'VOO': {'info': 'ETF on Stocks'},
    'QQQ': {'info': 'ETF on Stocks'},
    'DIA': {'info': 'ETF on Stocks'},
    'VIXY': {'info': 'S&P500 Volatility Index'},
    'AAPL': {'info': 'Stock'},
    'MSFT': {'info': 'Stock'},
    'AMZN': {'info': 'Stock'},
    'GOOG': {'info': 'Stock'},
    'GOOGL': {'info': 'Stock'},
    'FB': {'info': 'Stock'},
    'NFLX': {'info': 'Stock'},
    'TSLA': {'info': 'Stock'},
    'VCSH': {'info': '(1-3) ETF of Corp Bonds'},
    'IGSB': {'info': '(1-5) ETF of Corp Bonds'},
    'VCIT': {'info': '(~6) ETF of Corp Bonds'},
    'LQD': {'info': '(~9) ETF of Corp Bonds'},
    'SHY': {'info': '(1-3) ETF of Gov Bonds'},
    'IEF': {'info': '(7-10) ETF of Gov Bonds'},
    'GOVT': {'info': '(~6) ETF of Gov Bonds'},
    'TLT': {'info': '(~20) ETF of Gov Bonds'},
    'GLD': {'info': 'Commodities'},
    'IAU': {'info': 'Commodities'},
}

indicators_height = 200