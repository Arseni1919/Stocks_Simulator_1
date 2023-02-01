import matplotlib.pyplot as plt
import numpy as np
from environments.env_meta_class import MetaEnv
from plot_fucntions_and_classes.plot_functions import *
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
        self.history_holdings = np.zeros((self.max_steps,))
        self.history_holdings_worth = np.zeros((self.max_steps,))
        self.history_orders = np.zeros((self.max_steps,))
        self.history_portfolio_worth = np.zeros((self.max_steps,))
        self.history_commission_value = np.zeros((self.max_steps,))
        self.history_cash[0] = self.cash
        self.history_portfolio_worth[0] = self.cash
        observation = self.generate_next_observation()
        info = {}
        return observation, info

    def reset_check(self):
        if self.step_count == -1:
            raise RuntimeError('Do a resset first!')

    def generate_next_observation(self):
        observation = {}
        step_count = self.step_count

        prev_asset_value = 100 if step_count == 0 else self.history_asset[step_count - 1]
        var = 3
        sin_part = np.sin(step_count / 15)
        asset_value = prev_asset_value + sin_part / 100 * prev_asset_value + np.random.randint(-var, var+1) / 100 * prev_asset_value
        self.history_asset[step_count] = asset_value
        self.history_volume[step_count] = sin_part * 5 + 5 + np.random.randint(1, 10)

        observation['asset'] = self.history_asset[step_count]
        observation['asset_volume'] = self.history_volume[step_count]
        observation['step_count'] = step_count
        observation['in_hand'] = self.in_hand
        step_count = 1 if step_count == 0 else step_count
        step_count = 0 if step_count == -1 else step_count
        observation['history_cash'] = self.history_cash[step_count - 1]
        observation['history_holdings'] = self.history_holdings[step_count - 1]
        observation['history_holdings_worth'] = self.history_holdings_worth[step_count - 1]
        observation['history_orders'] = self.history_orders[step_count - 1]
        observation['history_portfolio_worth'] = self.history_portfolio_worth[step_count - 1]
        observation['history_commission_value'] = self.history_commission_value[step_count - 1]

        return observation

    def sample_action(self):
        # return np.random.choice(self.action_space, p=[0.9, 0.05, 0.05])
        return [np.random.choice(self.action_space, p=[0.05, 0.9, 0.05]) for _ in range(2)]

    def update_history_after_action(self, current_price):
        self.history_holdings[self.step_count] = self.portion_of_asset
        self.history_cash[self.step_count] = self.cash
        self.history_commission_value[self.step_count] += self.commission_value
        if self.portion_of_asset > 0:  # long
            h_holdings_worth = self.portion_of_asset * current_price
        elif self.portion_of_asset < 0:  # short
            loan_to_receive_before_commission = abs(self.portion_of_asset) * current_price
            revenue_to_receive_before_commission = self.short_cash - loan_to_receive_before_commission
            h_holdings_worth = self.short_cash + revenue_to_receive_before_commission
        else:  # portion_of_asset is 0
            h_holdings_worth = 0
        self.history_holdings_worth[self.step_count] = h_holdings_worth
        self.history_portfolio_worth[self.step_count] = self.cash + h_holdings_worth

    def enter_short(self, current_price):
        self.in_hand = -1
        cash_to_invest_before_commission = self.cash * self.risk_rate
        self.cash -= cash_to_invest_before_commission
        cash_to_invest_after_commission = cash_to_invest_before_commission / (1 + self.commission)
        self.portion_of_asset = - cash_to_invest_after_commission / current_price
        self.short_cash = cash_to_invest_after_commission
        self.commission_value = self.commission * cash_to_invest_after_commission
        return True

    def exit_short(self, current_price):
        self.in_hand = 0
        loan_to_receive_before_commission = abs(self.portion_of_asset) * current_price
        self.commission_value = self.commission * loan_to_receive_before_commission
        loan_to_receive_after_commission = loan_to_receive_before_commission - self.commission_value
        revenue_to_receive_after_commission = self.short_cash - loan_to_receive_after_commission
        self.cash += self.short_cash + revenue_to_receive_after_commission
        self.portion_of_asset = 0
        self.short_cash = 0
        return True

    def enter_long(self, current_price):
        self.in_hand = 1
        cash_to_invest_before_commission = self.cash * self.risk_rate
        self.cash = self.cash - cash_to_invest_before_commission
        cash_to_invest_after_commission = cash_to_invest_before_commission / (1 + self.commission)
        self.portion_of_asset = cash_to_invest_after_commission / current_price
        self.commission_value = self.commission * cash_to_invest_after_commission
        return True

    def exit_long(self, current_price):
        self.in_hand = 0
        cash_to_receive_before_commission = self.portion_of_asset * current_price
        self.commission_value = self.commission * cash_to_receive_before_commission
        cash_to_receive_after_commission = cash_to_receive_before_commission - self.commission_value
        self.cash += cash_to_receive_after_commission
        self.portion_of_asset = 0
        return True

    def exec_action(self, action, current_price):
        """
        :return:
        """
        if self.in_hand == 0:
            if self.step_count + 1 == self.max_steps:
                return False
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
        return False

    def step(self, action):
        """
        :return: observation, reward, terminated, truncated, info
        """
        self.reset_check()
        observation, reward, terminated, truncated, info = {}, 0, False, False, {}

        # execute actions
        current_price = self.history_asset[self.step_count]
        for sub_action in action:
            executed = self.exec_action(sub_action, current_price)  # reward in dollars
            self.update_history_after_action(current_price)
            if executed:
                self.history_orders[self.step_count] += 1
                self.history_actions[self.step_count] = sub_action
                self.commission_value = 0

        # get reward
        portfolio_worth = self.history_portfolio_worth[self.step_count]

        # is it terminated / truncated?
        self.step_count += 1
        if self.step_count >= self.max_steps:
            terminated = True
            self.step_count = -1

        # get NEXT observation
        observation = self.generate_next_observation()

        # gather info
        info = {}

        return observation, portfolio_worth, terminated, truncated, info

    def close(self):
        pass

    # For rendering ------------------------------------------------------------------------------- #
    def render(self, info=None):
        if self.to_plot:
            self.render_graphs(self.ax, self.ax_volume, info)
            if "alg_name" in info:
                self.fig.suptitle(f'Alg: {info["alg_name"]}', fontsize=16)
            plt.pause(0.001)

    def render_graphs(self, ax, ax_volume, info=None):
        info['step_count'] = self.step_count
        info['max_steps'] = self.max_steps
        info['history_asset'] = self.history_asset
        info['history_actions'] = self.history_actions
        info['history_volume'] = self.history_volume
        info['history_cash'] = self.history_cash
        info['history_orders'] = self.history_orders
        info['history_holdings'] = self.history_holdings
        info['history_holdings_worth'] = self.history_holdings_worth
        info['history_portfolio_worth'] = self.history_portfolio_worth
        info['history_commission_value'] = self.history_commission_value

        plot_asset_and_actions(ax[0, 0], info=info)
        plot_volume(ax_volume, info=info)
        plot_rewards(ax[0, 1], info=info)
        plot_commissions(ax[0, 2], info=info)
        plot_property(ax[1, 0], info=info)
        # plot_variance(ax[1, 1], info=info)
        plot_orders(ax[1, 1], info=info)
        plot_average(ax[1, 2], info=info)


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

# def cla_axes(self):
#     self.ax_volume.cla()
#     for ax_i in self.ax.reshape(-1):
#         ax_i.cla()


