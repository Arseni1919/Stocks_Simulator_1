from globals import *

"""
All the functions that define plots for the streamlit.
"""


def plot_price_and_volume(info):
    bars_df = info['bars_df']
    selected_x_axis = info['selected_x_axis']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=bars_df[selected_x_axis], y=bars_df['close'], name="Price"), secondary_y=False)
    fig.add_trace(
        go.Scatter(x=bars_df[selected_x_axis], y=bars_df['volume'], name='Volume', fill='tozeroy', mode='lines'),
        secondary_y=True)
    return fig


def plot_dollar_volumes_many_days(**kwargs):
    dates_list = kwargs['dates_list']
    data = kwargs['data']
    s_date = kwargs['s_date']
    f_date = kwargs['f_date']
    selected_assets = kwargs['selected_assets']

    plot_dict = {}
    n_of_datapoints = 0
    for asset in selected_assets:
        plot_dict[asset] = []
        for date in dates_list[dates_list.index(s_date):dates_list.index(f_date)]:
            day_volumes = data[date][asset]['volume'][1:]
            day_prices = data[date][asset]['price'][1:]
            day_dollar_volumes = np.multiply(day_volumes, day_prices)
            plot_dict[asset].append(np.sum(day_dollar_volumes))
            n_of_datapoints += 1

    plot_df = pd.DataFrame.from_dict(plot_dict)
    if (n_of_datapoints := sum([len(plot_df[column]) for column in plot_df])) < 1e3:
        fig = px.line(plot_df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(plot_df)


def plot_dollar_volumes_one_day(**kwargs):
    data = kwargs['data']
    selected_assets = kwargs['selected_assets']
    selected_date = kwargs['selected_date']

    plot_dict = {}
    for asset in selected_assets:
        day_volumes = data[selected_date][asset]['volume'][1:]
        day_prices = data[selected_date][asset]['price'][1:]
        day_dollar_volumes = np.multiply(day_volumes, day_prices)
        plot_dict[asset] = day_dollar_volumes

    plot_df = pd.DataFrame.from_dict(plot_dict)
    n_of_datapoints = sum([len(plot_df[column]) for column in plot_df])
    if n_of_datapoints < 1e3:
        fig = px.line(plot_df)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(plot_df)
