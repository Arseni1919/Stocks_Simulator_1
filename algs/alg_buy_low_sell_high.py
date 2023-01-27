from globals import *
from environments.sin_stock_env import SinStockEnv


class BuyLowSellHighAlg:

    def __init__(self, env, to_plot=False, window=40):
        self.env = env
        self.name = f'BLSH-{window}'
        self.to_plot = to_plot
        self.window = window
        self.max_steps = self.env.max_steps
        self.history_asset = np.zeros((self.max_steps,))
        self.history_volume = np.zeros((self.max_steps,))
        self.history_actions = np.zeros((self.max_steps,))
        self.history_rewards = np.zeros((self.max_steps,))
        self.history_rewards_fee = np.zeros((self.max_steps,))
        self.history_property = np.zeros((self.max_steps,))
        self.history_termination = np.zeros((self.max_steps,))


        # for plots
        if self.to_plot:
            self.subplot_rows = 2
            self.subplot_cols = 3
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            self.ax_volume = self.ax[0, 0].twinx()

    def return_action(self, observation):
        action = 0
        step_count = observation['step_count']
        if step_count > self.window + 2:
            ts = pd.Series(self.history_asset[0:step_count])
            data = ts.rolling(window=self.window).mean().to_numpy()
            p1 = data[-1]
            p2 = data[-2]
            if p1 - p2 > 0:
                action = 1
            elif p1 == p2:
                action = 0
            else:
                action = -1
        return action

    def update(self, observation, action, reward, next_observation, terminated, truncated):
        step_count = observation['step_count']
        self.history_asset[step_count] = observation['asset']
        self.history_volume[step_count] = observation['asset_volume']
        self.history_actions[step_count] = action
        self.history_rewards[step_count] = reward
        self.history_rewards_fee[step_count] = next_observation['reward_fee']
        self.history_property[step_count] = next_observation['in_hand']
        self.history_termination[step_count] = terminated

    def render(self, info):
        if self.to_plot:
            self.cla_axes()
            self.env.plot_asset_and_actions(self.ax[0, 0], info=info)
            self.env.plot_volume(self.ax_volume, info=info)
            self.env.plot_rewards(self.ax[0, 1], info=info)
            self.env.plot_rewards_differences(self.ax[0, 2], info=info)
            self.env.plot_property(self.ax[1, 0], info=info)
            self.env.plot_variance(self.ax[1, 1], info=info)
            self.env.plot_average(self.ax[1, 2], info=info)
            self.fig.suptitle(f'Alg: {self.name}', fontsize=16)
            plt.pause(0.001)

    def cla_axes(self):
        self.ax_volume.cla()
        for ax_i in self.ax.reshape(-1):
            ax_i.cla()


def main():
    episodes = 1
    env = SinStockEnv()
    alg = BuyLowSellHighAlg(env=env, to_plot=True)
    observation, info = env.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
            action = alg.return_action(observation)
            next_observation, reward, terminated, truncated, info = env.step(action)
            alg.update(observation, action, reward, next_observation, terminated, truncated)
            observation = next_observation
            if step % 200 == 0 or step == env.max_steps - 1:
                # env.render(info={'episode': episode, 'step': step, 'alg_name': alg.name})
                alg.render(info={'episode': episode, 'step': step})

    plt.show()


if __name__ == '__main__':
    main()


# class Alg:
#
#     def __init__(self, env):
#         self.env = env
#         self.name = 'Alg'
#
#     def return_action(self, observation):
#         return self.env.sample_action()
#
#     def update(self):
#         pass

