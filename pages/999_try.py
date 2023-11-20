import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import time

# fig, ax = plt.subplots()
plt.rcParams["figure.figsize"] = (20, 3)

# max_data = 100
max_data = 10
y_data = []
x_data = []

the_plot = st.pyplot(plt)
the_plot_2 = st.pyplot(plt)


def animate(i):  # update the y values (every 1000ms)
    plt.cla()
    plt.title(f'Iteration {i}')
    plt.plot(x_data, y_data)
    the_plot.pyplot(plt)
    the_plot_2.pyplot(plt)


# for i in range(max_data):
#     x_data.append(i)
#     y_data.append(i + np.random.random())
#     animate(i)
#     time.sleep(0.001)

from globals import *
N = 1001
plot_dict = {'data': np.random.random(N)}
plot_df = pd.DataFrame.from_dict(plot_dict)
n_of_datapoints = sum([len(plot_df[column]) for column in plot_df])
fig = px.line(plot_df, render_mode='svg')
st.plotly_chart(fig, use_container_width=True)
st.line_chart(plot_df)
