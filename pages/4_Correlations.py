from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *


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
# Main
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

st.write(f'# Correlation Analysis')

st.write('## Data')

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

if len(data) > 0:
    st.success(f'Data is loaded.')

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

'''
## Day correlation matrix:
'''
tab1, tab2 = st.tabs(["Specific Day", "Run All Days"])


with tab1:
    selected_date = st.select_slider("Date:", options=dates_list, value=dates_list[0])
    g_assets_2 = st.radio("Group of assets 2:", ['Custom', "# ***", "STOCKS", "GOV BONDS", "CORPORATE BONDS"], index=1, horizontal=True)
    g_list_1 = g_dict[g_assets_2]
    selected_assets = st.multiselect('Select assets:', assets_names_list, g_list_1)
    data_for_corr = get_data_for_corr(data, selected_date, selected_assets)
    fig = px.imshow(data_for_corr.corr(), text_auto=True, zmin=-1, zmax=1)
    st.plotly_chart(fig)

with tab2:
    g_assets_1 = st.radio("Group of assets 1:", ['Custom', "# ***", "STOCKS", "GOV BONDS", "CORPORATE BONDS"], index=1,
                          horizontal=True)
    g_list_1 = g_dict[g_assets_1]
    with st.form('set_parameters_1'):
        rate = st.slider('Rate:', 1, 10, 9, 1)
        selected_assets = st.multiselect('Select assets:', assets_names_list, g_list_1)
        s_date, f_date = st.select_slider(
            "Select range of dates:",
            options=dates_list,
            value=(dates_list[0], dates_list[-1]))
        submitted = st.form_submit_button("Run")
        my_bar = st.progress(0, text='Press "Run" Button')
    # stop_button = st.button('Reset')
    # if stop_button:
    #     st.stop()
    if submitted:
        plotly_obj = st.plotly_chart(px.line({'a': [1]}))
        selected_dates = dates_list[dates_list.index(s_date):dates_list.index(f_date) + 1]
        for date_i, date in enumerate(selected_dates):
            data_for_corr = get_data_for_corr(data, date, selected_assets)
            fig = px.imshow(data_for_corr.corr(), text_auto=True, zmin=-1, zmax=1)
            plotly_obj.plotly_chart(fig)
            # time.sleep(0.001)
            my_bar.progress((date_i + 1) / len(selected_dates), text=f'{date=}')
            time.sleep(1 - rate / 10)

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #



# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# END
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #

