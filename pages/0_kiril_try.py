from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *


def make_zero_based(day):
    day = day.pct_change()
    day.iloc[0] = 0
    day = (day + 1).cumprod()-1
    # day += 1
    day *= 100
    return day


def plot_prices_one_day(**kwargs):
    data = kwargs['data']
    selected_assets = kwargs['selected_assets']
    selected_date = kwargs['selected_date']

    plot_dict = {}
    for asset in selected_assets:
        day_prices = data[selected_date][asset]['price'][1:]
        plot_dict[asset] = day_prices

    plot_df = pd.DataFrame.from_dict(plot_dict)
    plot_df = make_zero_based(plot_df)
    fig = px.line(plot_df, render_mode='svg')
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Main
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #


st.write(f'# Looking at one day')
st.write('#### Data')

data = load_big_json()
dates_list = list(data.keys())
dates_list.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))

if len(data) > 0:
    st.success(f'Data is loaded.')

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

'''
## View specific day prices:
'''

selected_date = st.select_slider("Date:", options=dates_list, value=dates_list[0])
g_assets_2 = st.radio("Group of assets 2:", list(g_dict.keys()), index=1, horizontal=True)
g_list_1 = g_dict[g_assets_2]
selected_assets = st.multiselect('Select assets:', assets_names_list, g_list_1)
plot_prices_one_day(data=data, selected_assets=selected_assets, selected_date=selected_date)


# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# END
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #

