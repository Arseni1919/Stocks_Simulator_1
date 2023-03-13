from globals import *


# class PlotterBigExperiments:
#
#     def __init__(self, to_plot=True, max_steps=390):
#         self.to_plot = to_plot
#         self.name = 'PlotterBigExperiments'
#         self.max_steps = max_steps
#
#         # for plots
#         if self.to_plot:
#             self.subplot_rows = 1
#             self.subplot_cols = 2
#             self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
#             # self.ax_volume = self.ax[0, 0].twinx()
#
#     def render(self, info):
#         if self.to_plot:
#             # self.plot_rewards(self.ax[0, 0], info)
#             self.plot_rewards(self.ax[0], info)
#             self.fig.suptitle(f'{self.name}', fontsize=16)
#             plt.pause(0.001)
#
#     def plot_rewards(self, ax, info):
#         ax.cla()
#         algorithms = info['algorithms']
#         for algorithm in algorithms:
#             h_rewards = algorithm.history_portfolio_worth[:self.max_steps]
#             # cumsum_rewards = np.cumsum(h_rewards)
#             # ax.plot(cumsum_rewards, alpha=0.7, label=f'{algorithm.name}')
#             ax.plot(h_rewards, '--', alpha=0.7, label=f'{algorithm.name}')
#             ax.legend()
#             self.set_xlims(ax)
#             ax.set_title('history_portfolio_worth')
#
#     def set_xlims(self, ax):
#         ax.set_xlim([0, self.max_steps])
