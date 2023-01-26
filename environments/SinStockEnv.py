import matplotlib.pyplot as plt
import numpy as np

from globals import *


class SinStockEnv:
    def __init__(self, interest=0.02):
        self.interest = interest  # in percentage
        self.name = 'SinStockEnv'
        self.action_space = np.array([-1, 0, 1])
        self.last_action = -100
        self.step_count = -1
        self.max_steps = 390  # minutes
        self.revenue = None
        self.history_asset = None
        self.history_volume = None
        self.history_actions = None
        self.history_rewards = None
        self.in_hand = None
        self.last_purchased = None

        # for plots
        self.subplot_rows = 2
        self.subplot_cols = 2
        self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
        self.ax_volume = self.ax[0, 0].twinx()

    def reset(self):
        """
        :return: observation, info
        """
        self.step_count = 0
        self.last_action = 0
        self.in_hand = 0  # -1 -> short, 0 -> nothing, 1 -> long
        self.last_purchased = None
        self.revenue = np.zeros((self.max_steps,))
        self.history_asset = np.zeros((self.max_steps,))
        self.history_volume = np.zeros((self.max_steps,))
        self.history_actions = np.zeros((self.max_steps,))
        self.history_rewards = np.zeros((self.max_steps,))

        observation = self.generate_next_observation()
        info = {}
        return observation, info

    def reset_check(self):
        if self.step_count == -1:
            raise RuntimeError('Do a resset first!')

    def generate_next_observation(self):
        observation = {}
        prev_asset_value = 50 if self.step_count == 0 else self.history_asset[self.step_count - 1]
        self.history_asset[self.step_count] = prev_asset_value + np.random.randint(-2, 3)
        self.history_volume[self.step_count] = np.random.randint(10, 100)
        observation['SPY'] = self.history_asset[self.step_count]
        observation['SPY_volume'] = self.history_volume[self.step_count]
        return observation

    def sample_action(self):
        return np.random.choice(self.action_space, p=[0.05, 0.9, 0.05])

    def filter_action(self, action):
        pass

    def calc_reward(self, action):
        current_price = self.history_asset[self.step_count]
        if self.step_count + 1 == self.max_steps:
            if self.in_hand in [-1, 1]:
                reward = current_price - self.last_purchased
                self.last_purchased = None
                self.in_hand = 0
                return reward
        if action == 1:
            if self.in_hand == -1:
                reward = current_price - self.last_purchased
                self.last_purchased = None
                self.in_hand = 0
                return reward
            if self.in_hand == 0:
                self.last_purchased = current_price
                self.in_hand = 1
        if action == -1:
            if self.in_hand == 0:
                self.last_purchased = current_price
                self.in_hand = -1
            if self.in_hand == 1:
                reward = current_price - self.last_purchased
                self.last_purchased = None
                self.in_hand = 0
                return reward
        return 0

    def step(self, action):
        """
        :return: observation, reward, terminated, truncated, info
        """
        self.reset_check()
        observation, reward, terminated, truncated, info = {}, 0, False, False, {}

        # execute action
        self.history_actions[self.step_count] = action

        # get reward
        self.history_rewards[self.step_count] = self.calc_reward(action)

        # is it terminated / truncated?
        self.step_count += 1
        if self.step_count >= self.max_steps:
            terminated = True
            self.step_count = -1

        # get NEXT observation
        observation = self.generate_next_observation()

        # gather info
        info = {}

        return observation, reward, terminated, truncated, info

    def close(self):
        pass

    # For rendering ------------------------------------------------------------------------------- #
    def render(self, info=None):
        self.cla_axes()
        self.plot_asset_and_actions(self.ax[0, 0], info=info)
        # self.plot_volume(self.ax_volume, info=info)
        self.plot_rewards(self.ax[0, 1], info=info)
        plt.pause(0.001)

    def plot_asset_and_actions(self, ax, info):
        ax.plot(self.history_asset[:self.step_count], c='lightblue')
        buy_steps = np.where(self.history_actions[:self.step_count] == 1)
        ax.scatter(buy_steps, self.history_asset[buy_steps], c='green', marker='^')
        sell_steps = np.where(self.history_actions[:self.step_count] == -1)
        ax.scatter(sell_steps, self.history_asset[sell_steps], c='red', marker='v')
        self.set_xlims(ax)

        if info is not None:
            episode = info['episode']
            step = info['step']
            ax.set_title(f"{episode=} | {step=}")

    def plot_volume(self, ax, info):
        ax.cla()
        ax.bar(np.arange(self.step_count), self.history_volume[:self.step_count], alpha=0.2)
        ax.set_ylim(0, 1000)

    def plot_rewards(self, ax, info):
        cumsum_rewards = np.cumsum(self.history_rewards[:self.step_count])
        color = 'green' if cumsum_rewards[-1] > 0 else 'red'
        ax.plot(cumsum_rewards, c=color, alpha=0.7)
        self.set_xlims(ax)
        ax.set_title('Cumulative Rewards')

    def set_xlims(self, ax):
        ax.set_xlim([0, self.max_steps])

    def cla_axes(self):
        self.ax_volume.cla()
        if self.ax.ndim == 1:
            for i_ax in self.ax:
                i_ax.cla()
        if self.ax.ndim == 2:
            for row_ax in self.ax:
                for col_ax in row_ax:
                    col_ax.cla()


def main():
    episodes = 1
    env = SinStockEnv()
    observation, info = env.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            action = env.sample_action()
            env.step(action)
            if step % 100 == 0 or step == env.max_steps - 1:
                env.render(info={'episode': episode, 'step': step})

    plt.show()




if __name__ == '__main__':
    main()




# class Env:
#     def __init__(self):
#         self.name = 'SinStockEnv'
#         self.needed_reset = True
#         self.action_space = []
#         self.state_space = []
#
#     def reset(self):
#         """
#         :return: observation, info
#         """
#         self.needed_reset = False
#
#     def sample_action(self):
#         pass
#
#     def step(self):
#         """
#         :return: observation, reward, terminated, truncated, info
#         """
#         if self.needed_reset:
#             pass
#
#     def close(self):
#         pass
#
#     def render(self):
#         pass




