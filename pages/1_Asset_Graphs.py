from indicator_functions import *
from functions import *


st.set_page_config(layout="wide")


# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# LOCAL FUNCTIONS
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
pass

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
# Sidebar
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# st.sidebar.write('## Select a stock:')
with st.sidebar:
    pass

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Main
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
alert_of_stock_exchange()
with st.form("my_form"):
    st.write('# Parameters')

    selected_asset = st.radio(
        "Select an asset:",
        assets_names_list,
        captions=[assets_names_dict[item]['info'] for item in assets_names_list],
        horizontal=True)

    cols_names = ['1D', '5D', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
    selected_time_period = st.radio("Select time period:", cols_names, horizontal=True)
    selected_x_axis = st.radio("Select X-axis:", ['datetime', 'num'], horizontal=True, index=1)

    st.write('Select indicators to show:')
    rsi_bool = st.toggle('rsi', value=True, disabled=False)
    ma_bool = st.toggle('ma', value=True, disabled=False)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.toast('Renewed!', icon='✅')

st.write(f'# Asset Analysis - {selected_asset}')

bars_df = historical_data(selected_asset, selected_time_period)
fig = plot_price_and_volume(info={'bars_df': bars_df, 'selected_x_axis': selected_x_axis})
st.plotly_chart(fig, use_container_width=True)

expander = st.expander(f"See The '{selected_asset}' Data")
expander.write(bars_df)

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Indicators
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
if rsi_bool:
    st.write(f'### RSI')
    fig = set_indicator_graph(bars_df[selected_x_axis], rsi_calc(bars_df['close']))
    st.plotly_chart(fig, theme=None, use_container_width=True)

if ma_bool:
    st.write(f'### MA')
    fig = set_indicator_graph(bars_df[selected_x_axis], macd_func(bars_df['close']))
    st.plotly_chart(fig, theme=None, use_container_width=True)

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #





# fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2], name="(1,2)"), row=1, col=2)
#
# fig = px.line(bars_df, x=selected_x_axis, y='close', title='Close Prices')
# st.plotly_chart(fig, theme=None, use_container_width=True)
# fig = px.line(bars_df, x=selected_x_axis, y='volume', title='Volume')
