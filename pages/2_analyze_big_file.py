import pandas as pd

from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *

# init
st.set_page_config(layout="wide")
data = load_big_json()
dates_list = load_dates_list(data)

"# Analyze Big JSON File With All The Data"

# -------------------------------------------------------------------------------------------------------------------- #
'---'
# -------------------------------------------------------------------------------------------------------------------- #

"## All data:"

# st.write(dates_list)
st.write(f'#### We have dates from {dates_list[:2]}... until ...{dates_list[-2:]}.')
st.write(f'### There are {len(dates_list)} days.')

"#### Lets take one date:"

selected_date = st.select_slider(
    "Date:",
    options=dates_list,
    value=dates_list[0])

selected_asset = st.selectbox('Select asset:', assets_names_list)
fig, ax = plt.subplots(2, 1, figsize=(20, 6))
ax[0].plot(data[selected_date][selected_asset]['price'], label='price', c='c')
ax[0].legend()
ax[1].plot(data[selected_date][selected_asset]['volume'][1:], label='volume', c='brown')
ax[1].legend()
st.pyplot(fig)

before_df = {'assets': [], 'infos': [], 'prices': [], 'volumes': []}
for asset in assets_names_list:
    before_df['assets'].append(asset)
    before_df['infos'].append(assets_names_dict[asset]['info'])
    before_df['prices'].append(data[selected_date][asset]['price'])
    before_df['volumes'].append(data[selected_date][asset]['volume'][1:])

daily_df = pd.DataFrame(before_df)

with st.expander(":orange[Big Table]", expanded=False):
    st.dataframe(daily_df, column_config={
        'assets': 'assets',
        'infos': 'infos',
        'prices': st.column_config.LineChartColumn('prices'),
        'volumes': st.column_config.LineChartColumn('volumes'),
    }, hide_index=True, use_container_width=True, height=880)


with st.expander(":orange[Total Volume]", expanded=False):
    s_date, f_date = st.select_slider(
        "Date:",
        options=dates_list,
        value=(dates_list[0], dates_list[-1]))
    total_volume_list = []
    total_volume_daily_list = []
    for date in dates_list[dates_list.index(s_date):dates_list.index(f_date)]:
        curr_total_volume = 0
        curr_total_volume_daily = np.zeros(390)
        for asset in assets_names_list:
            # day_volumes = data[date][asset]['volume'] * data[date][asset]['price']
            dv_value = data[date][asset]['volume'] 
            curr_total_volume += np.sum(dv_value)
            curr_total_volume_daily += dv_value
        total_volume_list.append(curr_total_volume)
        total_volume_daily_list.extend(curr_total_volume_daily)

    fig, ax = plt.subplots(2, 1, figsize=(20, 6))
    ax[0].plot(total_volume_list, label='Volume')
    ax[0].legend()
    ax[1].plot(total_volume_daily_list, label='Volume Minutes')
    ax[1].legend()
    st.pyplot(fig)
    st.line_chart(total_volume_daily_list)
    # st.dataframe(daily_df, column_config={
    #     'assets': 'assets',
    #     'infos': 'infos',
    #     'prices': st.column_config.LineChartColumn('prices'),
    #     'volumes': st.column_config.LineChartColumn('volumes'),
    # }, hide_index=True, use_container_width=True, height=880)

# -------------------------------------------------------------------------------------------------------------------- #
'---'
# -------------------------------------------------------------------------------------------------------------------- #

'## Average Daily Return'

with st.expander(":orange[Click to open/close...]", expanded=False):
    '''
    Let's look at the average daily return. 
    The hypothesis is that it has to be around 0.
    '''
    before_df['diff_day_mean'] = []
    before_df['diff_day_std'] = []
    for asset in assets_names_list:
        curr_diff_day_list = []
        for curr_date in dates_list:
            cur_diff_day = 100 * (data[curr_date][asset]['price'][-1] - data[curr_date][asset]['price'][0]) / \
                           data[curr_date][asset]['price'][0]
            curr_diff_day_list.append(cur_diff_day)
        # :red[Streamlit] :orange[can] :green[write]
        mean = np.mean(curr_diff_day_list)
        mean_str = f'🟩 {mean:.4f} %' if mean > 0 else f'🟥 {mean:.4f} %'
        before_df['diff_day_mean'].append(mean_str)
        before_df['diff_day_std'].append(f'🔃{np.std(curr_diff_day_list):.4f} %')

    mean_std_df = pd.DataFrame(before_df)
    st.dataframe(mean_std_df, column_config={
        'assets': 'assets',
        'infos': 'infos',
        'diff_day_mean': 'diff_day_mean',
        'diff_day_std': 'diff_day_std',
        'prices': None,
        'volumes': None,
    }, hide_index=True, use_container_width=True, height=880)

    '''
    What do we see: 
    - ETF on stocks are all around the 0.02 % exept for the QQQ
    - DIA is out of this trend completely
    - VIXY is less than 0 - why?
    - stocks are crazy here
    - TSLA has the highest average daily growth
    - SHY is really near 0
    - The longer the Gov bond the higher yield
    - Gold is around the 0.02
    - (DIA, VIXY, AMZN, NFLX, SHY are with a negative value)
    - _
    - VIXY by far has the highest std
    - Next highest stds are the stocks - expected
    - Next are ETFs on stocks
    - Then -> bonds with gold
    '''

# -------------------------------------------------------------------------------------------------------------------- #
'---'
# -------------------------------------------------------------------------------------------------------------------- #

'## SHY'
with st.expander(":orange[Click to open/close...]", expanded=False):
    '## Let\'s look at the SHY stock'

    '''
    Shy seems to be the most stable with the mean of :red[-0.0005%] and std of **0.0318%**.
    Let's see the graph of price and volume for the whole period.
    '''

    full_shy_price_list, full_shy_volume_list = [], []
    shy_volume_per_day_lists = {}
    for date in dates_list:
        full_shy_price_list.extend(data[date]['SHY']['price'])
        full_shy_volume_list.extend(data[date]['SHY']['volume'])
        shy_volume_per_day_lists[date] = data[date]['SHY']['volume']

    start_i, end_i = st.select_slider(
        'Select a range of time-steps:',
        options=range(len(full_shy_price_list)),
        value=(0, len(full_shy_price_list) - 1))
    x_list = list(range(start_i, end_i))
    fig, ax = plt.subplots(2, 1, figsize=(20, 10))
    ax[0].plot(x_list, full_shy_price_list[start_i:end_i])
    ax[1].plot(x_list, full_shy_volume_list[start_i:end_i])
    st.pyplot(fig)

    '''
    Now let's look at the volume with the moving median:
    '''
    df = pd.DataFrame(shy_volume_per_day_lists)

    window = st.slider('Select a window:', 1, 50, 3)
    # Calculate the rolling median for window = 1
    roll_median = df.rolling(window=window).median()
    st.line_chart(roll_median)
    # roll_list = df.values.tolist()
    # roll_list = list(itertools.chain(*roll_list))
    # st.line_chart(roll_list)

    '''
    ❓Question: _What was in those days?_
    '''

# -------------------------------------------------------------------------------------------------------------------- #
'---'
# -------------------------------------------------------------------------------------------------------------------- #

'## The Optimal Strategy'

with st.expander(":orange[Click to open/close...]", expanded=False):
    '''
    Let's look at the best possible strategy, that we can make given that we know the future. \n
    The setting:
    - We are doing the daily bids. That means, we start and finish at the same day always.
    - We start each day with the 100$.
    - We are allowed to make actions each minute, including swapping from long to short and vise-versa.
    - We examine two cases: with commissions and without them. 
    - We use the SPY stock.
    '''

    '### Without Commissions'
    # data[selected_date][asset]['price']
    on_100 = st.toggle('Start with 100 each day', value=True)
    with st.echo():
        cash_history = []
        for date in dates_list:
            spy_day_prices = np.array(data[date]['SPY']['price'])  # len = 390
            percent_change = np.abs(np.diff(spy_day_prices) / spy_day_prices[:-1])
            percent_change += 1
            prod_percent_change = np.prod(percent_change)
            if on_100:
                cash_history.append(100 * prod_percent_change)
            else:
                if len(cash_history) == 0:
                    cash_history.append(100 * prod_percent_change)
                else:
                    cash_history.append(cash_history[-1] * prod_percent_change)
            # cash_history.append(prod_percent_change)
        cumsum_list = np.array(cash_history) - 100
        cumsum_list[0] += 100
        cumsum_list = np.cumsum(cumsum_list)
        chart_data = pd.DataFrame({'dates': dates_list, 'cash': cash_history, 'cumsum': cumsum_list})

    st.line_chart(chart_data, x="dates", y="cash")
    st.line_chart(chart_data, x="dates", y="cumsum")

    '### With Commissions'
    commission = st.slider('Select commission:', 0.0, 0.01, 0.002, 0.001, format='%.3f')  # percentage - out of 1
    f'{commission=}'
    f'''
    If we do action every minute, we will pay from 
    {commission * 100 * 390}\$ and up to {commission * 100 * 390 * 2}\$ each day (probably even more). \n
    The less actions we do the less commissions we pay. The minimum amount of actions we can do is two: 
    - enter long/short position at the first minute
    - exit the position at the last minute
    '''
    on_100_com = st.toggle('Start with 100 each day (commission)', value=True)
    with st.echo():
        cash_history = []
        for date in dates_list:
            spy_day_prices = np.array(data[date]['SPY']['price'])  # len = 390
            percent_change = np.abs((spy_day_prices[0] - spy_day_prices[-1]) / spy_day_prices[0])
            percent_change += 1
            if on_100_com:
                start_cash = 100
            else:
                start_cash = 100 if len(cash_history) == 0 else cash_history[-1]

            enter_pos = start_cash * (1 - commission) * percent_change
            exit_pos = enter_pos * (1 - commission)
            cash_history.append(exit_pos)
            # cash_history.append(prod_percent_change)
        cumsum_list = np.array(cash_history) - 100
        cumsum_list[0] += 100
        cumsum_list = np.cumsum(cumsum_list)
        chart_data = pd.DataFrame({'dates': dates_list, 'cash': cash_history, 'cumsum': cumsum_list})

    st.line_chart(chart_data, x="dates", y="cash")
    st.line_chart(chart_data, x="dates", y="cumsum")