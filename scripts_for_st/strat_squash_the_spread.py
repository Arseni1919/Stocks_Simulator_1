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
        commission = st.slider('Select commission:', 0.0, 0.01, 0.001, 0.001, format='%.3f')

        part1, part2, part3 = st.tabs(["Correlation", "Asset's Graphs", "Spread"])
        with part1:
            corr_hidden = st.toggle('Hide correlation graph', value=False)
            if not corr_hidden:
                st.write(f'## First, checking correlation:')
                corr_list = []
                for date in dates_list:
                    a1_prices = data[date][asset_1]['price']
                    a2_prices = data[date][asset_2]['price']
                    correlation, p_value = sp.stats.pearsonr(a1_prices, a2_prices)
                    corr_list.append(correlation)
                plot_dict = {'Dates': dates_list, "Pearson's R": corr_list}
                fig = px.line(plot_dict, x='Dates', y="Pearson's R")
                st.plotly_chart(fig, use_container_width=True)

        with part2:
            assets_hidden = st.toggle("Hide asset's graph", value=False)
            if not assets_hidden:
                st.write(f"## Then, let's look at the stocks:")
                plot_dict = {'Dates': dates_list, f'{asset_1}': [], f'{asset_2}': []}
                for date in dates_list:
                    a1_prices = np.array(data[date][asset_1]['price']) / data[date][asset_1]['price'][0]
                    a2_prices = np.array(data[date][asset_2]['price']) / data[date][asset_2]['price'][0]
                    plot_dict[f'{asset_1}'].append(np.mean(a1_prices))
                    plot_dict[f'{asset_2}'].append(np.mean(a2_prices))

                fig = px.line(plot_dict, x='Dates', y=[f'{asset_1}', f'{asset_2}'])
                st.plotly_chart(fig, use_container_width=True)

        with part3:
            st.write(f"## Finally, let's examine the spread:")
            plot_dict = {'Dates': dates_list, 'spread': [], 'spread_prices': []}
            for date in dates_list:
                a1_prices = np.array(data[date][asset_1]['price']) / data[date][asset_1]['price'][0]
                a2_prices = np.array(data[date][asset_2]['price']) / data[date][asset_2]['price'][0]
                plot_dict['spread'].append(abs(np.mean(a1_prices) - np.mean(a2_prices)))

                a1_prices = np.array(data[date][asset_1]['price'])
                a2_prices = np.array(data[date][asset_2]['price'])
                plot_dict['spread_prices'].append(abs(np.mean(a1_prices) - np.mean(a2_prices)))

            fig = px.line(plot_dict, x='Dates', y=['spread'])
            st.plotly_chart(fig, use_container_width=True)
            fig = px.line(plot_dict, x='Dates', y=['spread_prices'])
            st.plotly_chart(fig, use_container_width=True)


