import numpy as np
import pandas as pd

from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *

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
# Analyze Volumes 
"""

with st.expander(":orange[Dollar-Volume Metric]", expanded=True):
    g_assets_1 = st.radio("Group of assets 1:", ['Custom', "# ***", "STOCKS", "GOV BONDS", "CORPORATE BONDS"], index=2,
                          horizontal=True)
    g_list_1 = g_dict[g_assets_1]
    with st.form('set_parameters_1'):
        'For the range of days:'
        s_date, f_date = st.select_slider(
            "Date:",
            options=dates_list,
            value=(dates_list[0], dates_list[-1]))
        selected_assets = st.multiselect('Select assets:', assets_names_list, g_list_1)
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.rerun()
    plot_dollar_volumes_many_days(dates_list=dates_list, data=data, s_date=s_date, f_date=f_date,
                                  selected_assets=selected_assets)

    g_assets_2 = st.radio("Group of assets 2:", ['Custom', "# ***", "STOCKS", "GOV BONDS", "CORPORATE BONDS"], index=2,
                          horizontal=True)
    g_list_2 = g_dict[g_assets_2]
    with st.form('set_parameters_2'):
        'For one specific day:'
        # selected_date = st.date_input("Select the day:", datetime.date(2021, 4, 12))
        # selected_date = str(selected_date)
        selected_date = st.select_slider("Date:", options=dates_list, value=dates_list[0])
        selected_assets = st.multiselect('Select assets:', assets_names_list, g_list_2)
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.rerun()
    plot_dollar_volumes_one_day(data=data, selected_assets=selected_assets, selected_date=selected_date)
