from globals import *
from plot_fucntions_and_classes.plot_functions import *


class MetaEnv(ABC):
    def __init__(self, commission=0.001, risk_rate=1, to_plot=False):
        self.name = 'MetaEnv'
        self.commission = commission  # in ratio
        self.risk_rate = risk_rate  # in ratio
        self.to_plot = to_plot
        self.action_space = np.array([-1, 0, 1])
        self.step_count = -1
        self.max_steps = 390  # minutes
        # global data:
        self.list_of_assets = []
        self.history_assets = None
        self.history_volume = None
        # agent:
        self.history_actions = None
        self.history_orders = None  # how many orders we did in any kind
        self.history_holdings = None  # a portion of long or short
        self.history_holdings_worth = None  # a worth of a portion of long or short
        self.history_cash = None  # in dollars
        self.history_commission_value = None
        self.history_portfolio_worth = None
        # agent's current values
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

    def reset_check(self):
        if self.step_count == -1:
            raise RuntimeError('Do a resset first!')

    def reset(self):
        """
        :return: observation, info
        """
        # global data
        # self.history_assets = np.zeros((self.max_steps,))
        # self.history_volume = np.zeros((self.max_steps,))
        self.history_assets = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        self.history_volume = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        # instant data
        self.step_count = 0
        self.in_hand = 0  # -1 -> short, 0 -> nothing, 1 -> long
        self.cash = 100
        self.short_cash = 0
        self.portion_of_asset = 0
        self.commission_value = 0
        self.last_purchased = None
        # agent data
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

    @abstractmethod
    def generate_next_assets(self):
        pass

    def generate_next_observation(self):
        observation = {}
        step_count = self.step_count
        self.generate_next_assets()
        # global data:
        observation['asset'] = {asset: self.history_assets[asset][step_count] for asset in self.list_of_assets}
        observation['asset_volume'] = {asset: self.history_volume[asset][step_count] for asset in self.list_of_assets}
        # current state data:
        observation['step_count'] = step_count
        observation['in_hand'] = self.in_hand
        # agent data:
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
        return [(asset, np.random.choice(self.action_space, p=[0.05, 0.9, 0.05])) for asset in self.list_of_assets]

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

    def check_margin_call(self, current_price):
        loan_to_receive_before_commission = abs(self.portion_of_asset) * current_price
        commission_value = self.commission * loan_to_receive_before_commission
        loan_to_receive_after_commission = loan_to_receive_before_commission - commission_value
        if 1.8 * self.short_cash < loan_to_receive_after_commission:
            print('\n-----\nMARGIN CALL\n-----\n')
            return True
        return False

    def exec_action(self, asset, action, current_price):
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
            margin_call = self.check_margin_call(current_price)
            if self.step_count + 1 == self.max_steps or margin_call:
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

    def step(self, actions):
        """
        :return: observation, reward, terminated, truncated, info
        """
        self.reset_check()
        observation, reward, terminated, truncated, info = {}, 0, False, False, {}

        # execute actions
        for action_tuple in actions:
            asset, action = action_tuple
            current_price = self.history_assets[asset][self.step_count]
            executed = self.exec_action(asset, action, current_price)  # reward in dollars
            self.update_history_after_action(asset, current_price)
            self.commission_value = 0
            if executed:
                self.history_orders[self.step_count] += 1
                self.history_actions[self.step_count] = action

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

    def update_history_after_action(self, asset, current_price):
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

    def close(self):
        pass

    def render(self, info=None):
        if self.to_plot:
            self.render_graphs(self.ax, self.ax_volume, info)
            main_asset = info['main_asset']
            title = f'main_asset: {main_asset}'
            if "alg_name" in info:
                title += f' Alg: {info["alg_name"]}'
            self.fig.suptitle(title, fontsize=16)
            plt.pause(0.001)

    def render_graphs(self, ax, ax_volume, info=None):
        info['step_count'] = self.step_count
        info['max_steps'] = self.max_steps
        info['history_assets'] = self.history_assets
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










