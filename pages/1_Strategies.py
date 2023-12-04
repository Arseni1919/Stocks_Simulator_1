from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *
from st_strategies.strat_simple_follow_stock import strat_simple_follow_stock
from st_strategies.strat_squash_the_spread import strat_squash_the_spread

# init
st.set_page_config(layout="wide")
data = load_big_json()
dates_list = list(data.keys())
dates_list.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))

"""
# Strategies
"""

to_show = st.toggle('Show general data', value=False)
if to_show:
    asset = st.selectbox('Select asset:', assets_names_list)
    st.write(f'# All Periods of {asset}')
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write('## Prices')
        plot_asset_prices(data=data, selected_dates=dates_list, asset=asset, ignore_first_minute=False)
    with col2:
        st.write('## Volumes')
        plot_asset_volumes(data=data, selected_dates=dates_list, asset=asset, ignore_first_minute=True)


strat_simple_follow_stock(data=data, dates_list=dates_list, asset='TSLA')
strat_squash_the_spread(data=data, dates_list=dates_list, asset_1='AMZN', asset_2='AAPL')