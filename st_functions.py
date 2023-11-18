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


