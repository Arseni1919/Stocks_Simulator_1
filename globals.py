import random
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import os
import datetime
import json

# import pymongo
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

stocks_names_list = [
    'SPY',
    'TLT',
    'AAPL',
    'AMZN',
    'DIA',
    'FB',
    'GLD',
    'GOOG',
    'GOOGL',
    'GOVT',
    'IAU',
    'IEF',
    'IGSB',
    'IVV',
    'LQD',
    'MSFT',
    'NFLX',
    'QQQ',
    'SHY',
    'TSLA',
    'VCIT',
    'VCSH',
    'VIXY',
    'VOO',
]