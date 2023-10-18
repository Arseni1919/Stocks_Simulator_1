import time

from globals import *


# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# FUNCTIONS
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
@st.cache(allow_output_mutation=True)
def get_sample_data():
    name = 'data_for_Correl3.pickle'
    with open(name, 'rb') as f:
        curr_data = pickle.load(f)
        for day_data_df in curr_data:
            new_names_dict = {}
            for name in day_data_df.columns:
                new_names_dict[name] = name[4:]
            day_data_df.rename(columns=new_names_dict, inplace=True)
        return curr_data


@st.cache(allow_output_mutation=True)
def get_columns_and_np_data():
    big_corr_list = []
    curr_columns = list(data[0].columns)
    for day_data_df in data:
        big_corr_list.append(day_data_df.corr().to_numpy())
    curr_corr_np = np.array(big_corr_list)
    return curr_columns, curr_corr_np


def select_all_func(curr_options, curr_columns):
    curr_options = curr_columns


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


# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Main
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

st.write(f'# Correlation Analysis')

st.write('## Data')

data = get_sample_data()
if len(data) > 0:
    st.success(f'Data is loaded.')

st.write("""
# _____________________________________ 
""")
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

st.write(f'## Day correlation matrix:')

color = st.select_slider('Select a day:', options=[i for i in range(len(data))])
# st.write(data[0].columns)
fig = px.imshow(data[color].corr(), text_auto=True, zmin=-1, zmax=1)
st.plotly_chart(fig)

st.write(f"""
## Analysis
- SHY - short Gov. bonds
- TLT - long gov. bonds
- QQQ - ETF stock
- VIXY - short options on SPY (volume is important)
- LQD - long corp. bonds
- GOVT - treasury medium
- IEF - 7-10 years treasury
- IAU - gold

$\\alpha$
""")


st.write("""
# _____________________________________ 
""")
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #

st.write('## Correlation progress through days:')

columns, corr_np = get_columns_and_np_data()


if st.button('Refresh'):
    st.experimental_rerun()
to_show = st.slider('How many to choose:', 0, len(columns), 7)
options = st.multiselect('Stocks/Bonds:', columns, columns[:to_show])

if len(options) > 0:
    fig = make_subplots(rows=len(options), cols=len(options))
    counter = 0
    for i_row, option_row in enumerate(options):
        for i_col, option_col in enumerate(options):
            corr_data = corr_np[:, columns.index(option_row), columns.index(option_col)]
            fig.add_trace(
                go.Scatter(x=list(range(len(corr_data))), y=corr_data, name=f'{option_row}-{option_col}'),
                row=i_row + 1, col=i_col + 1)
            counter += 1
    # fig.update_layout(yaxis_range=[-4, 4])
    # fig.update(layout_yaxis_range=[-4, 4])
    fig.update_yaxes(range=[-1, 1])
    fig.update_layout(height=800, width=900, title_text="Side By Side Subplots")
    st.plotly_chart(fig)

# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #
# Indicators
# ------------------------------------ #
# ------------------------------------ #
# ------------------------------------ #


# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# END
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------ #

# fig, ax = plt.subplots()
# arr = np.random.normal(1, 1, size=100)
# ax.hist(arr, bins=20)
# st.pyplot(fig)
