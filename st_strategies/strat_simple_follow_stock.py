from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *


def run_simple_follow_stock(**kwargs):
    data = kwargs['data']
    dates_list = kwargs['dates_list']
    asset = kwargs['asset']
    commission = kwargs['commission']
    margin_call_percentage = kwargs['margin_call_percentage']

    # with st.echo(code_location="below"):
    # first init
    profit_list = []
    percentage_list = []

    day_before = dates_list[0]
    for next_day in dates_list[1:]:
        basis_price = data[day_before][asset]['price'][-1]
        start_price = data[next_day][asset]['price'][0]
        end_price = data[next_day][asset]['price'][-1]
        day_prices_list = data[next_day][asset]['price'][1:]

        if start_price > basis_price:
            # BUY
            profit = end_price - (start_price + start_price * commission)
            # margin call
            for next_price in day_prices_list:
                if next_price < start_price * margin_call_percentage:
                    profit = next_price - (start_price + start_price * commission)
                    break
                # fix profit
                # if next_price > start_price * 1.2:
                #     profit = next_price - (start_price + start_price * commission)
                #     break
        else:
            # SHORT
            profit = (start_price + start_price * commission) - end_price
            # margin call
            for next_price in day_prices_list:
                if next_price > start_price * margin_call_percentage:
                    profit = (start_price + start_price * commission) - next_price
                    break
                # fix profit
                # if next_price < start_price * 1.2:
                #     profit = (start_price + start_price * commission) - next_price
                #     break

        profit -= end_price * commission
        profit_list.append(profit)
        percent = profit / start_price
        percentage_list.append(percent)

        day_before = next_day

    return profit_list, percentage_list


def strat_simple_follow_stock(**kwargs):
    data = kwargs['data']
    dates_list = kwargs['dates_list']
    asset = kwargs['asset']
    # day_volumes = data[date][asset]['volume'][1:]
    # day_prices = data[date][asset]['price'][1:]

    with st.expander(f":orange[Simple Follow Stock]", expanded=False):
        with st.form('set_asset'):
            asset = st.selectbox('Select asset:', assets_names_list, index=assets_names_list.index(asset))
            # commission = st.slider('Select commission:', 0.0, 0.01, 0.001, 0.001, format='%.3f')
            commission = st.radio('Select commission:', [0, 0.0002, 0.001, 0.003], horizontal=True, index=2)
            margin_call_percentage = st.slider('margin_call_percentage:', 0.0, 1.0, 0.9, 0.1, format='%.1f')
            submitted = st.form_submit_button("Run")
        if submitted:
            st.rerun()

        hidden = st.toggle('Hide general data', value=True)
        if not hidden:
            st.write(f'# All Periods of {asset}')
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write('## Prices')
                plot_asset_prices(data=data, selected_dates=dates_list, asset=asset, ignore_first_minute=False)
            with col2:
                st.write('## Volumes')
                plot_asset_volumes(data=data, selected_dates=dates_list, asset=asset, ignore_first_minute=True)

        st.write("# Let's make some groshhi:")
        st.write("""
        ## Description:
        Take any stock. Let’s define the basis as the last price of the previous day. 
        If the stock opens above the basis then buy and hold until the end of the day / stop loss. 
        Else, if stock opens below the basis, then short the stock.
        """)
        profit_list, percentage_list = run_simple_follow_stock(
            data=data, dates_list=dates_list, asset=asset,
            commission=commission, margin_call_percentage=margin_call_percentage
        )

        # plot the results
        plot_dict = {
            'Dates': dates_list[1:],
            'Profit': profit_list, 'Cumulative Profit': np.cumsum(profit_list),
            'Percentage': percentage_list, 'Cumulative Percentage': np.cumsum(percentage_list),
            'Baseline': np.zeros(len(profit_list))
        }
        tab1, tab2 = st.tabs(["Percentage", "Profit"])
        with tab1:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write('### Percentage Daily')
                fig = px.line(plot_dict, x='Dates', y=['Percentage', 'Baseline'])
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.write('### Cumulative Percentage Daily')
                fig = px.line(plot_dict, x='Dates', y='Cumulative Percentage')
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write('### Profit Daily')
                fig = px.line(plot_dict, x='Dates', y=['Profit', 'Baseline'])
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.write('### Cumulative Profit Daily')
                fig = px.line(plot_dict, x='Dates', y='Cumulative Profit')
                st.plotly_chart(fig, use_container_width=True)

        st.write(f"### :red[Questions:]")
        st.write("""
        - Why no stock can benefit from the strategy? what stops it?
        - How the market knows to through the simple strategy?
        """)
