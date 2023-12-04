import pandas as pd

from indicator_functions import *
from st_plot_functions import *
from st_functions import *
from functions import *
from st_strategies.strat_simple_follow_stock import strat_simple_follow_stock
from st_strategies.strat_squash_the_spread import strat_squash_the_spread

with st.echo():
    data_dict = {'a': [10], 'b': [20]}

    data_dict

'# Hello Kiril'
'## Hello Kiril'
'### Hello Kiril'
'#### Hello Kiril'


data_df = pd.DataFrame(data_dict)
data_df