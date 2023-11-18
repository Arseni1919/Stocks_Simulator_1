import pandas as pd

from globals import *

"""
All the functions that have 'st' in them.
"""


@st.cache_data
def load_big_json():
    f = open('data/data.json')
    data = json.load(f)
    return data


@st.cache_data
def load_dates_list(data):
    dates_list = list(data.keys())
    dates_list.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))
    return dates_list


def get_data_for_corr(data, selected_date, selected_assets):
    plot_dict = {}
    for asset in selected_assets:
        plot_dict[asset] = data[selected_date][asset]['price']
    data_for_corr = pd.DataFrame.from_dict(plot_dict)
    return data_for_corr


# @st.cache_data
# def get_sample_data():
#     name = 'data_for_Correl3.pickle'
#     with open(name, 'rb') as f:
#         curr_data = pickle.load(f)
#         for day_data_df in curr_data:
#             new_names_dict = {}
#             for name in day_data_df.columns:
#                 new_names_dict[name] = name[4:]
#             day_data_df.rename(columns=new_names_dict, inplace=True)
#         return curr_data
#
#
# @st.cache_data
# def get_columns_and_np_data():
#     big_corr_list = []
#     curr_columns = list(data[0].columns)
#     for day_data_df in data:
#         big_corr_list.append(day_data_df.corr().to_numpy())
#     curr_corr_np = np.array(big_corr_list)
#     return curr_columns, curr_corr_np


