import numpy as np

from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *


def strat_squash_the_spread(**kwargs):
    data = kwargs['data']
    dates_list = kwargs['dates_list']
    asset_1 = kwargs['asset_1']
    asset_2 = kwargs['asset_2']
    # day_volumes = data[date][asset]['volume'][1:]
    # day_prices = data[date][asset]['price'][1:]
    with st.expander(f":orange[Squash The Spread]", expanded=False):
        st.write("""
        ### Description:
        Take two super correlated stocks (for example Amazon and Apple) and monitor the following: 
        if there is a spread between them, execute a short position on the upper stock and 
        the long position on the lower stock. The volume is needed to be usual.
        """)
        asset_1 = st.selectbox('Select asset 1:', assets_names_list, index=assets_names_list.index(asset_1))
        asset_2 = st.selectbox('Select asset 2:', assets_names_list, index=assets_names_list.index(asset_2))
        commission = st.radio('Select commission:', [0, 0.0002, 0.001, 0.003], horizontal=True, index=2)

        part1, part2, part3, part4 = st.tabs(["Show Assets", "Correlation", "Asset's Graphs", "Spread"])
        #
        with part1:
            st.write(f"## First, let's look at the stocks:")
            plot_dict = {'Dates': dates_list, f'{asset_1}': [], f'{asset_2}': []}
            for date in dates_list:
                a1_prices = np.array(data[date][asset_1]['price'])
                a1_prices_df = values_to_zero_based(asset_1, a1_prices)
                plot_dict[f'{asset_1}'].append(np.mean(a1_prices_df[asset_1]))

                a2_prices = np.array(data[date][asset_2]['price'])
                a2_prices_df = values_to_zero_based(asset_2, a2_prices)
                plot_dict[f'{asset_2}'].append(np.mean(a2_prices_df[asset_2]))

            fig = px.line(plot_dict, x='Dates', y=[f'{asset_1}', f'{asset_2}'])
            st.plotly_chart(fig, use_container_width=True)

            selected_date = st.select_slider("Date:", options=dates_list, value=dates_list[0])
            day_plot_dict = {f'{asset_1}': [], f'{asset_2}': []}
            a1_prices = np.array(data[selected_date][asset_1]['price'])
            a1_prices_df = values_to_zero_based(asset_1, a1_prices)
            day_plot_dict[f'{asset_1}'] = a1_prices_df[asset_1]

            a2_prices = np.array(data[selected_date][asset_2]['price'])
            a2_prices_df = values_to_zero_based(asset_2, a2_prices)
            day_plot_dict[f'{asset_2}'] = a2_prices_df[asset_2]

            fig = px.line(day_plot_dict)
            st.plotly_chart(fig, use_container_width=True)

        with part2:
            st.write(f"## Then, let's checking correlation:")
            st.image(f'pics/corr_formula.png', caption='Correlation Formula', width=400)
            corr_list = []
            for date in dates_list:
                a1_prices = np.array(data[date][asset_1]['price'])
                a1_prices_df = values_to_zero_based(asset_1, a1_prices)
                a2_prices = np.array(data[date][asset_2]['price'])
                a2_prices_df = values_to_zero_based(asset_2, a2_prices)
                correlation, p_value = sp.stats.pearsonr(a1_prices_df[asset_1], a2_prices_df[asset_2])
                corr_list.append(correlation)
            plot_dict = {'Dates': dates_list, "Pearson's R": corr_list}
            fig = px.line(plot_dict, x='Dates', y="Pearson's R")
            st.plotly_chart(fig, use_container_width=True)

        with part3:
            st.write(f"## Then, let's examine the spread:")
            plot_dict = {'Dates': dates_list, f'{asset_1}': [], f'{asset_2}': []}
            for date in dates_list:
                a1_prices = np.array(data[date][asset_1]['price'])
                a1_prices_df = values_to_zero_based(asset_1, a1_prices)
                a2_prices = np.array(data[date][asset_2]['price'])
                a2_prices_df = values_to_zero_based(asset_2, a2_prices)

                plot_dict[f'{asset_1}'].append(np.mean(a1_prices))
                plot_dict[f'{asset_2}'].append(np.mean(a2_prices))

            fig = px.line(plot_dict, x='Dates', y=[f'{asset_1}', f'{asset_2}'])
            st.plotly_chart(fig, use_container_width=True)

        with part4:
            st.write(f"## Finally, let's examine the spread:")
            plot_dict = {'Dates': dates_list, 'spread %': [], 'spread_prices': []}
            for date in dates_list:
                a1_prices = np.array(data[date][asset_1]['price'])
                a2_prices = np.array(data[date][asset_2]['price'])
                a1_prices = np.diff(a1_prices) / a1_prices[:-1]
                a2_prices = np.diff(a2_prices) / a2_prices[:-1]
                plot_dict['spread %'].append(abs(np.mean(a1_prices) - np.mean(a2_prices)) * 100)

                a1_prices = np.array(data[date][asset_1]['price'])
                a2_prices = np.array(data[date][asset_2]['price'])
                plot_dict['spread_prices'].append(abs(np.mean(a1_prices) - np.mean(a2_prices)))

            fig = px.line(plot_dict, x='Dates', y=['spread %'])
            st.plotly_chart(fig, use_container_width=True)
            fig = px.line(plot_dict, x='Dates', y=['spread_prices'])
            st.plotly_chart(fig, use_container_width=True)

        st.write(f"### :red[Questions:]")
        st.write("""
        - How to calc spread exactly?
        """)


