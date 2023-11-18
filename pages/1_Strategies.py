from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *
from scripts_for_st.strat_simple_follow_stock import strat_simple_follow_stock

# init
st.set_page_config(layout="wide")
data = load_big_json()
dates_list = list(data.keys())
dates_list.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))
g_dict = {
    'Custom': ['SPY'],
    '# ***': assets_names_list,
    'STOCKS': ['AAPL', 'AMZN', 'GOOG', 'GOOGL', 'MSFT', 'FB', 'NFLX', 'TSLA'],
    'GOV BONDS': ['SHY', 'IEF', 'GOVT', 'TLT'],
    'CORPORATE BONDS': ['VCSH', 'IGSB', 'VCIT', 'LQD'],
}

"""
# Strategies
"""

strat_simple_follow_stock(data=data, dates_list=dates_list, asset='TSLA')