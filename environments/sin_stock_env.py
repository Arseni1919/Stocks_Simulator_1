import matplotlib.pyplot as plt
import numpy as np
from environments.env_meta_class import MetaEnv
from globals import *


class SinStockEnv(MetaEnv):
    def __init__(self, commission=0.001, risk_rate=1, to_plot=False):
        super().__init__()
        self.commission = commission  # in percentage
        self.risk_rate = risk_rate
        self.to_plot = to_plot
        self.name = 'SinStockEnv'
        self.action_space = np.array([-1, 0, 1])
        self.last_action = -100
        self.step_count = -1
        self.max_steps = 390  # minutes
        # global data:
        self.history_asset = None
        self.history_volume = None
        # agent:
        self.history_actions = None
        self.history_orders = None  # how many orders we did in any kind
        self.history_holdings = None  # a portion of long or short
        self.history_holdings_worth = None  # a worth of a portion of long or short
        self.history_cash = None  # in dollars
        self.history_commission_value = None
        self.history_portfolio_worth = None
        self.in_hand = None
        self.last_purchased = None
        self.portion_of_asset = 0
        self.cash = 100
        self.short_cash = 0
        self.commission_value = 0

        # for plots
        if self.to_plot:
            self.subplot_rows = 2
            self.subplot_cols = 3
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            self.ax_volume = self.ax[0, 0].twinx()

    def reset(self):
        """
        :return: observation, info
        """
        self.step_count = 0
        self.last_action = 0
        self.in_hand = 0  # -1 -> short, 0 -> nothing, 1 -> long
        self.cash = 100
        self.short_cash = 0
        self.portion_of_asset = 0
        self.commission_value = 0
        self.last_purchased = None
        self.history_asset = np.zeros((self.max_steps,))
        self.history_volume = np.zeros((self.max_steps,))
        self.history_actions = np.zeros((self.max_steps,))
        self.history_cash = np.zeros((self.max_steps,))
        # self.history_rewards_fee = np.zeros((self.max_steps,))
        self.history_holdings = np.zeros((self.max_steps,))
        self.history_holdings_worth = np.zeros((self.max_steps,))
        self.history_orders = np.zeros((self.max_steps,))
        self.history_portfolio_worth = np.zeros((self.max_steps,))
        self.history_commission_value = np.zeros((self.max_steps,))
        self.history_cash[0] = self.cash
        observation = self.generate_next_observation()
        info = {}
        return observation, info

    def reset_check(self):
        if self.step_count == -1:
            raise RuntimeError('Do a resset first!')

    def generate_next_observation(self):
        observation = {}
        prev_asset_value = 100 if self.step_count == 0 else self.history_asset[self.step_count - 1]
        var = 3
        sin_part = np.sin(self.step_count / 15)
        # print(f'\n{sin_part}')
        asset_value = prev_asset_value + sin_part / 100 * prev_asset_value + np.random.randint(-var, var+1) / 100 * prev_asset_value
        self.history_asset[self.step_count] = asset_value
        # self.history_asset[self.step_count] = prev_asset_value + sin_part + np.random.randint(-var, var+1)
        # prev_volume_value = 50 if self.step_count == 0 else self.history_volume[self.step_count - 1]
        self.history_volume[self.step_count] = sin_part * 5 + 5 + np.random.randint(1, 10)
        observation['asset'] = self.history_asset[self.step_count]
        observation['asset_volume'] = self.history_volume[self.step_count]
        observation['step_count'] = self.step_count
        # observation['reward_fee'] = reward_fee
        observation['in_hand'] = self.in_hand
        return observation

    def sample_action(self):
        # return np.random.choice(self.action_space, p=[0.9, 0.05, 0.05])
        return np.random.choice(self.action_space, p=[0.05, 0.9, 0.05])

    def update_history_after_action(self, current_price):
        self.history_orders[self.step_count] += 1
        self.history_holdings[self.step_count] = self.portion_of_asset
        self.history_holdings_worth[self.step_count] = self.portion_of_asset * current_price
        self.history_cash[self.step_count] = self.cash
        self.history_commission_value[self.step_count] = self.commission_value

    def enter_short(self, current_price):
        self.in_hand = -1
        cash_to_invest_before_commission = self.cash * self.risk_rate
        self.cash -= cash_to_invest_before_commission
        cash_to_invest_after_commission = cash_to_invest_before_commission / (1 + self.commission)
        self.portion_of_asset = - cash_to_invest_after_commission / current_price
        self.short_cash = cash_to_invest_after_commission
        self.commission_value = self.commission * cash_to_invest_after_commission

        self.update_history_after_action(current_price)
        return 0, True

    def exit_short(self, current_price):
        self.in_hand = 0
        loan_to_receive_before_commission = self.portion_of_asset * current_price * -1
        self.commission_value = self.commission * loan_to_receive_before_commission
        loan_to_receive_after_commission = loan_to_receive_before_commission - self.commission_value
        cash_to_receive_after_commission = self.short_cash - loan_to_receive_after_commission
        self.cash += cash_to_receive_after_commission
        self.portion_of_asset = 0
        self.short_cash = 0

        self.update_history_after_action(current_price)
        return True

    def enter_long(self, current_price):
        self.in_hand = 1
        cash_to_invest_before_commission = self.cash * self.risk_rate
        self.cash = self.cash - cash_to_invest_before_commission
        cash_to_invest_after_commission = cash_to_invest_before_commission / (1 + self.commission)
        self.portion_of_asset = cash_to_invest_after_commission / current_price
        self.commission_value = self.commission * cash_to_invest_after_commission

        self.update_history_after_action(current_price)
        return True

    def exit_long(self, current_price):
        self.in_hand = 0
        cash_to_receive_before_commission = self.portion_of_asset * current_price
        self.commission_value = self.commission * cash_to_receive_before_commission
        cash_to_receive_after_commission = cash_to_receive_before_commission - self.commission_value
        self.cash += cash_to_receive_after_commission
        self.portion_of_asset = 0

        self.update_history_after_action(current_price)
        return True

    def exec_action(self, action):
        """
        :return:
        """
        current_price = self.history_asset[self.step_count]
        if self.in_hand == 0:
            if self.step_count + 1 == self.max_steps:
                return 0, 0, False
            if action == 1:
                return self.enter_long(current_price)
            if action == -1:
                return self.enter_short(current_price)
        elif self.in_hand == -1:
            if self.step_count + 1 == self.max_steps:
                return self.exit_short(current_price)
            if action == 1:
                return self.exit_short(current_price)
        elif self.in_hand == 1:
            if self.step_count + 1 == self.max_steps:
                return self.exit_long(current_price)
            if action == -1:
                return self.exit_long(current_price)
        else:
            raise RuntimeError('in_hand - wrong')
        return 0, 0, False

    def step(self, action):
        """
        :return: observation, reward, terminated, truncated, info
        """
        self.reset_check()
        observation, reward, terminated, truncated, info = {}, 0, False, False, {}

        # execute action + get reward
        executed = self.exec_action(action)  # reward in dollars
        # TODO:
        self.history_portfolio_worth[self.step_count] = self.history_cash[self.step_count] + self.history_holdings_worth[self.step_count]
        if executed:
            self.history_actions[self.step_count] = action

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
        if self.to_plot:
            self.cla_axes()
            self.plot_asset_and_actions(self.ax[0, 0], info=info)
            self.plot_volume(self.ax_volume, info=info)
            self.plot_rewards(self.ax[0, 1], info=info)
            self.plot_rewards_differences(self.ax[0, 2], info=info)
            self.plot_property(self.ax[1, 0], info=info)
            self.plot_variance(self.ax[1, 1], info=info)
            self.plot_average(self.ax[1, 2], info=info)
            if "alg_name" in info:
                self.fig.suptitle(f'Alg: {info["alg_name"]}', fontsize=16)
            plt.pause(0.001)

    def plot_asset_and_actions(self, ax, info):
        ax.plot(self.history_asset[:self.step_count], c='lightblue')
        buy_steps = np.where(self.history_actions[:self.step_count] == 1)
        ax.scatter(buy_steps, self.history_asset[buy_steps], c='green', marker='^', label='long order')
        sell_steps = np.where(self.history_actions[:self.step_count] == -1)
        ax.scatter(sell_steps, self.history_asset[sell_steps], c='red', marker='v', label='short order')

        if 'w1' in info:
            ts = pd.Series(self.history_asset[0:self.step_count])
            data = ts.rolling(window=info['w1']).mean().to_numpy()
            ax.plot(data, label=f"w: {info['w1']}")

            ts = pd.Series(self.history_asset[0:self.step_count])
            data = ts.rolling(window=info['w2']).mean().to_numpy()
            ax.plot(data, label=f"w: {info['w2']}")

        ax.legend()
        self.set_xlims(ax)

        if info is not None:
            episode = info['episode']
            step = info['step']
            ax.set_title(f"{episode=} | {step=}")

    def plot_volume(self, ax, info):
        ax.cla()
        step_count = self.step_count if self.step_count >= 0 else self.max_steps - 1
        ax.bar(np.arange(step_count), self.history_volume[:self.step_count], alpha=0.2)
        ax.set_ylim(0, 50)

    def plot_property(self, ax, info):
        ax.cla()
        step_count = self.step_count if self.step_count >= 0 else self.max_steps - 1
        ax.plot(self.history_holdings[:self.step_count], c='brown', alpha=0.7)
        ax.fill_between(np.arange(step_count), np.zeros(step_count), self.history_holdings[:self.step_count],
                        color='coral', alpha=0.5)
        # ax.set_yticks([-1, 0, 1])
        # ax.set_yticklabels(['Short', 'Hold', 'Long'])
        self.set_xlims(ax)
        ax.set_title('In Hand')

    def plot_rewards(self, ax, info):
        h_cash = self.history_cash[:self.step_count]
        h_hold_w = self.history_holdings_worth[:self.step_count]
        h_port_w = self.history_portfolio_worth[:self.step_count]
        # h_rewards_fee = self.history_rewards_fee[:self.step_count]
        # cumsum_rewards = np.cumsum(h_rewards)
        color = 'green' if h_cash[-1] > 100 else 'red'
        ax.plot(h_cash, c=color, alpha=0.7, label='cash')
        ax.plot(h_hold_w, alpha=0.7, label='holdings_worth')
        ax.plot(h_port_w, alpha=0.7, label='portfolio_worth')
        # ax.plot(np.cumsum(h_rewards_fee), '--', c='gray', alpha=0.7, label='with fees')
        self.set_xlims(ax)
        ax.legend()
        ax.set_title('Cumulative Rewards')

    def plot_rewards_differences(self, ax, info):
        h_rewards = np.cumsum(self.history_cash[:self.step_count])
        # h_rewards_fee = np.cumsum(self.history_rewards_fee[:self.step_count])
        # ax.plot(h_rewards - h_rewards_fee)
        self.set_xlims(ax)
        ax.set_title('Difference With and Without Fees')

    def plot_variance(self, ax, info):
        ts = pd.Series(self.history_asset[1:self.step_count] - self.history_asset[0:self.step_count-1])
        for window in [10, 40, 70, 100]:
            data = ts.rolling(window=window).std().to_numpy()
            ax.plot(data, label=f'w:{window}')
        self.set_xlims(ax)
        ax.legend()
        ax.set_title('Asset Residuals')

    def plot_average(self, ax, info):
        ts = pd.Series(self.history_asset[0:self.step_count])
        for window in [10, 40, 70, 100]:
            data = ts.rolling(window=window).mean().to_numpy()
            ax.plot(data, label=f'w:{window}')
        self.set_xlims(ax)
        ax.legend()
        ax.set_title('Asset Average')

    def set_xlims(self, ax):
        ax.set_xlim([0, self.max_steps])

    def cla_axes(self):
        self.ax_volume.cla()
        for ax_i in self.ax.reshape(-1):
            ax_i.cla()


def main():
    episodes = 1
    env = SinStockEnv(to_plot=True)
    observation, info = env.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
            action = env.sample_action()
            env.step(action)
            if step % 200 == 0 or step == env.max_steps - 1:
                env.render(info={'episode': episode, 'step': step})

    plt.show()


if __name__ == '__main__':
    main()


# def cla_axes(self):
#     self.ax_volume.cla()
#     if self.ax.ndim == 1:
#         for i_ax in self.ax:
#             i_ax.cla()
#     if self.ax.ndim == 2:
#         for row_ax in self.ax:
#             for col_ax in row_ax:
#                 col_ax.cla()



