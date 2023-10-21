from indicator_functions import *
from functions import *


"# Analyze Big JSON File With All The Data"

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
}, hide_index=True, use_container_width=True, height=900)

