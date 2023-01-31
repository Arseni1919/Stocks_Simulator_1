from globals import *


class PlotterBigExperiments:

    def __init__(self, to_plot=True, max_steps=390):
        self.to_plot = to_plot
        self.name = 'PlotterBigExperiments'
        self.max_steps = max_steps

        # for plots
        if self.to_plot:
            self.subplot_rows = 1
            self.subplot_cols = 2
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            # self.ax_volume = self.ax[0, 0].twinx()

    def render(self, info):
        if self.to_plot:
            self.cla_axes()
            # self.plot_rewards(self.ax[0, 0], info)
            self.plot_rewards(self.ax[0], info)
            self.fig.suptitle(f'Alg: {self.name}', fontsize=16)
            plt.pause(0.001)

    def plot_rewards(self, ax, info):
        algorithms = info['algorithms']
        step_count = info['step']
        for algorithm in algorithms:
            h_rewards = algorithm.history_cash[:self.max_steps]
            h_rewards_fee = algorithm.history_rewards_fee[:self.max_steps]
            cumsum_rewards = np.cumsum(h_rewards)
            # ax.plot(cumsum_rewards, alpha=0.7, label=f'{algorithm.name}')
            ax.plot(np.cumsum(h_rewards_fee), '--', alpha=0.7, label=f'{algorithm.name} (fees)')
            ax.legend()
            self.set_xlims(ax)
            ax.set_title('Cumulative Rewards')

    def set_xlims(self, ax):
        ax.set_xlim([0, self.max_steps])

    def cla_axes(self):
        # self.ax.cla()
        # self.ax_volume.cla()
        for ax_i in self.ax.reshape(-1):
            ax_i.cla()
