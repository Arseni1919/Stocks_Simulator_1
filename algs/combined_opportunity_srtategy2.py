import random

import matplotlib.pyplot as plt

from globals import *
from environments.sin_stock_env import SinStockEnv
from environments.alpaca_env import AlpacaEnv
from environments.stock_env_class import StockEnv
from algs.alg_meta_class import MetaAlg
from plot_fucntions_and_classes.plot_functions import *
from indicator_functions import *

# kiril


class OpportunityAlg(MetaAlg):

    def __init__(self, env, to_plot=False, params=None):
        super().__init__(env, to_plot, params)

        # variables for the strategy
        self.no_long_count = 0
        self.no_short_count = 0

        # for plots
        if self.to_plot:
            self.subplot_rows = 2
            self.subplot_cols = 3
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            self.ax_volume = self.ax[0, 0].twinx()

    def render(self, info):
        if self.to_plot:
            info['step_count'] = self.env.step_count
            info['max_steps'] = self.max_steps
            info['history_assets'] = self.history_assets
            info['history_actions'] = self.history_actions
            info['history_volume'] = self.history_volume
            info['history_cash'] = self.history_cash
            info['history_orders'] = self.history_orders
            info['history_portion_of_asset'] = self.env.history_portion_of_asset
            info['history_portion_of_asset_worth'] = self.env.history_portion_of_asset_worth
            info['history_portfolio_worth'] = self.history_portfolio_worth
            info['history_commission_value'] = self.history_commission_value
            info['main_asset'] = self.main_asset

            plot_asset_and_actions(self.ax[0, 0], info=info)
            # plot_volume(ax_volume, info=info)
            plot_rewards(self.ax[0, 1], info=info)
            plot_commissions(self.ax[0, 2], info=info)
            plot_property(self.ax[1, 0], info=info)
            # plot_variance(ax[1, 1], info=info)
            plot_orders(self.ax[1, 1], info=info)
            # plot_average(self.ax[1, 2], info=info)
            plot_volume_is_high(self.ax[1, 2], info=info)
            # plot_volume(self.ax[1, 2], info=info)
            plt.pause(0.01)

    @staticmethod
    def calc_slope(df, multiplier=1000):
        result = (df.iloc[len(df) - 1] - df.iloc[0]) / len(df)
        return result * multiplier

    def return_action(self, observation, params):
        rsi_period = params['rsi_period']
        slope_start = params['slope_start']
        slope_angle = params['slope_angle']
        rsi_trigger = params['rsi_trigger']
        exit_after = params['exit']

        action = [0, 0]
        step_count, in_hand = self.update_history(observation)
        ts = pd.Series(self.history_assets[self.main_asset][:step_count])

        # opportunity strategy
        if step_count > rsi_period:
            # rsi = self.calc_rsi(ts, params)
            rsi = calc_rsi(ts, params)
            rsi = rsi[step_count-1]    # the last available RSI number

            slope_day_start = ts.rolling(400, min_periods=rsi_period).apply(self.calc_slope).fillna(0)

            # long entry:
            if (slope_day_start[:slope_start] >= -slope_angle).all():
                if rsi <= rsi_trigger:
                    self.no_long_count = 0
                    if in_hand == 0:
                        action[1] = 1
                    if in_hand == -1:
                        action[0] = 1
                        action[1] = 1
                else:
                    self.no_long_count += 1

            # short entry:
            if (slope_day_start[:slope_start] <= slope_angle).all():
                if rsi >= (1-rsi_trigger):
                    self.no_short_count = 0
                    if in_hand == 0:
                        action[1] = -1
                    if in_hand == 1:
                        action[0] = -1
                        action[1] = -1
                else:
                    self.no_short_count += 1

            # long exit
            if in_hand == 1:
                if self.no_long_count >= exit_after or rsi >= (1-rsi_trigger) or step_count == 388:
                    action[1] = -1

            # short exit
            if in_hand == -1:
                if self.no_short_count >= exit_after or rsi <= rsi_trigger or step_count == 388:
                    action[1] = 1

        return [(self.main_asset, action[0]), (self.main_asset, action[1])]

    def update_after_action(self, observation, action, portfolio_worth, next_observation, terminated):
        step_count = observation['step_count']
        last_action_asset, last_action_value = action[-1]
        self.history_actions[last_action_asset][step_count] = last_action_value

    def update_parameters(self):
        pass

def plot_volume_is_high(ax, info):
    ax.cla()
    step_count = info['step_count']
    history_volume = info['history_volume']
    max_steps = info['max_steps']
    main_asset = info['main_asset']
    mm_days = info['mm_days']

    step_count = step_count if step_count >= 0 else max_steps - 1

    # data preparation in pandas
    volumes = pd.DataFrame(history_volume[main_asset][:step_count], columns=['volume'])
    emm_values = volumes['volume'].rolling(mm_days).median().fillna(0)
    volumes['index'] = volumes.index
    volumes[f'Moving_median_{mm_days}'] = pd.Series(emm_values)
    volumes['STD_shifted'] = volumes['volume'].rolling(30, min_periods=30).std().shift(mm_days + 1)
    volumes[f'MM_shifted_{mm_days + 5}'] = volumes[f'Moving_median_{mm_days}'].shift(mm_days + 5)
    volumes['High_Volume_MM'] = np.where(volumes[f'Moving_median_{mm_days}'] > volumes[f'MM_shifted_{mm_days + 5}']
                                         + 1.9 * volumes['STD_shifted'], True, False)

    # plot
    ax.plot(volumes.index, volumes['volume'], color='blue', label='Volume', linewidth=1)
    ax.scatter(volumes.loc[volumes['High_Volume_MM'], 'index'],
               volumes.loc[volumes['High_Volume_MM'], 'volume'], color='red', label='High_Volume_MM (True)', s=30)
    ax.scatter(volumes.loc[~volumes['High_Volume_MM'], 'index'],
               volumes.loc[~volumes['High_Volume_MM'], 'volume'], color='black', label='High_Volume_MM (False)', s=3)
    ax.set_title('Volume Is High indicator')
    ax.legend(loc='upper left')
    # print(volumes)
    # print(volumes['High_Volume_MM'].describe())


def plot_rsi(ax, info):
    ax.cla()
    step_count = info['step_count']
    max_steps = info['max_steps']
    history_asset = info['history_assets']
    main_asset = info['main_asset']

    step_count = step_count if step_count >= 0 else max_steps - 1

    ts = pd.Series(history_asset[main_asset][:step_count])
    rsi = calc_rsi(ts, params)

    ax.plot(rsi, c='brown', alpha=0.7)
    set_xlims(ax, 0, max_steps)
    ax.set_title('In Hand')


def main():

    indicator_params = {}
    indicator_params['slope_multiplier'] = 1000
    indicator_params['rsi_period'] = 14
    indicator_params['mm_days'] = 5

    indicator_params['rsi_period'] = 7
    indicator_params['rsi_trigger'] = 0.3
    indicator_params['slope_start'] = 60
    indicator_params['slope_angle'] = 0.05
    indicator_params['exit'] = 20           # exit_after_consecutive

    episodes = 1
    env = StockEnv(list_of_assets=stocks_names_list, to_shuffle=False)
    alg = OpportunityAlg(env=env, to_plot=False)
    observation, info = env.reset()
    alg.reset()

    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
            action = alg.return_action(observation, indicator_params)
            next_observation, portfolio_worth, terminated, _ = env.step(action)
            alg.update_after_action(observation, action, portfolio_worth, next_observation, terminated)
            observation = next_observation

            if step % 50 == 0 or step == env.max_steps - 1:
                # env.render(info={'episode': episode, 'step': step, 'alg_name': alg.name})
                alg.render(info={'episode': episode, 'step': step, 'w1': 10, 'w2': 20,
                                 'mm_days': indicator_params['mm_days']})

    plt.show()


if __name__ == '__main__':
    main()


