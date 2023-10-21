from indicator_functions import *
from functions import *


"# Analyze Big JSON File With All The Data"

'---'

"## The list of dates in the data:"

data = load_big_json()
dates_list = list(data.keys())
dates_list.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))
st.write(dates_list)
st.write(f'#### We have dates from {dates_list[:3]}... until ...{dates_list[-3:]}.')
st.write(f'### There are {len(dates_list)} days.')

"#### Lets take one date:"

first_date = st.select_slider(
    "Date:",
    options=dates_list,
    value=dates_list[0])
# first_date = dates_list[10]
st.code(first_date)
# st.json(data[first_date]['SPY'])

before_df = {'assets': [], 'infos': [], 'prices': [], 'volumes': []}

for asset in assets_names_list:
    before_df['assets'].append(asset)
    before_df['infos'].append(assets_names_dict[asset]['info'])
    before_df['prices'].append(data[first_date][asset]['price'])
    before_df['volumes'].append(data[first_date][asset]['volume'][1:])

daily_df = pd.DataFrame(before_df)

st.dataframe(daily_df, column_config={
    'assets': 'assets',
    'infos': 'infos',
    'prices': st.column_config.LineChartColumn('prices'),
    'volumes': st.column_config.LineChartColumn('volumes'),
}, hide_index=True, use_container_width=True, height=880)

'---'

'## Average Daily Return'

'''
Let's look at the average daily return. 
The hypothesis is that it has to be around 0.
'''
before_df['diff_day_mean'] = []
before_df['diff_day_std'] = []
for asset in assets_names_list:
    curr_diff_day_list = []
    for curr_date in dates_list:
        cur_diff_day = 100 * (data[curr_date][asset]['price'][-1] - data[curr_date][asset]['price'][0]) / data[curr_date][asset]['price'][0]
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





