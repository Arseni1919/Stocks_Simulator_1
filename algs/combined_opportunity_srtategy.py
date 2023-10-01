from globals import *
from environments.sin_stock_env import SinStockEnv
from environments.alpaca_env import AlpacaEnv
from environments.kirill_env import KirillEnv
from algs.alg_meta_class import MetaAlg
from plot_fucntions_and_classes.plot_functions import *


class OpportunityAlg(MetaAlg):

    def __init__(self, env, to_plot=False, params=None):
        super().__init__(env, to_plot, params)
        # init
        if params is None:
            self.params = {'w1': 40, 'w2': 20}
        self.name = f'BLSH-{self.params["w1"]}-{self.params["w2"]}'
        self.no_long_count = 0
        self.no_short_count = 0

    @staticmethod
    def calc_rsi(series, rsi_period=14):
        chg = series.diff(1)
        gain = chg.mask(chg < 0, 0)
        loss = chg.mask(chg > 0, 0)
        avg_gain = gain.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        avg_loss = loss.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        rs = abs(avg_gain / avg_loss)
        rsi = 1 - (1 / (1 + rs))
        rsi[:rsi_period] = 0.5
        return rsi

    @staticmethod
    def calc_slope(window_df, multiplier=1000):
        result = (window_df.iloc[len(window_df) - 1] - window_df.iloc[0]) / len(window_df)
        return result * multiplier

    def return_action(self, observation, rsi_period, rsi_trigger, slope_start, slope_angle, exit):
        action = [0, 0]
        step_count, in_hand = self.update_history(observation)
        ts = pd.Series(self.history_assets[self.main_asset][0:step_count])

        # opportunity strategy
        if step_count > rsi_period:
            if step_count > rsi_period:
                rsi = self.calc_rsi(ts, rsi_period)
                rsi = rsi[step_count - 1]    # the last available RSI number

            slope_day_start = ts.rolling(400, min_periods=rsi_period).apply(self.calc_slope).fillna(0)

            # long entry:
            if (slope_day_start[:slope_start] >= -slope_angle).all():
                if rsi <= rsi_trigger:
                    self.no_long_count = 0
                    if in_hand == 0:
                        action[0] = 1
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
                        action[0] = -1
                    if in_hand == 1:
                        action[0] = -1
                        action[1] = -1
                else:
                    self.no_short_count += 1

            # long exit
            if in_hand == 1:
                if self.no_long_count >= exit or rsi >= (1-rsi_trigger) or step_count == 388:
                    action[0] = -1

            # short exit
            if in_hand == -1:
                if self.no_short_count >= exit or rsi <= rsi_trigger or step_count == 388:
                    action[0] = 1

        return [(self.main_asset, action[0]), (self.main_asset, action[1])]

    def update_after_action(self, observation, action, portfolio_worth, next_observation, terminated, truncated):
        step_count = observation['step_count']
        last_action_asset, last_action_value = action[-1]
        self.history_actions[last_action_asset][step_count] = last_action_value
        self.history_termination[step_count] = terminated


def main():
    episodes = 10
    rsi_period = 7
    rsi_trigger = 0.3
    slope_start = 60
    slope_angle = 0.05
    exit = 20         # exit_after_consecutive
    env = KirillEnv(list_of_assets=stocks_names_list, to_shuffle=False)
    alg = OpportunityAlg(env=env, to_plot=True)
    observation, info = env.reset()
    alg.reset()

    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode} | {step}', end='')
            action = alg.return_action(observation, rsi_period, rsi_trigger, slope_start, slope_angle, exit)
            next_observation, portfolio_worth, terminated, truncated, info = env.step(action)
            alg.update_after_action(observation, action, portfolio_worth, next_observation, terminated, truncated)
            observation = next_observation

            if step % 200 == 0 or step == env.max_steps - 1:
                # env.render(info={'episode': episode, 'step': step, 'alg_name': alg.name})
                alg.render(info={'episode': episode, 'step': step, 'w1': 10, 'w2': 20})

    plt.pause(0.1)

    ###
    # A function I used to get a df with result for all the day,
    # please check all the days and make one in this format so we can check the simulator.

    # @staticmethod
    # def update_results(results, df, strategy_name, rsi_period, rsi_trigger, slope_start, slope_angle, exit):
    #     ### With rsi_period, rsi_trigger and slope and slope angle in the results ###
    #     results = results.append({
    #         "strategy_name": strategy_name,
    #         "rsi_period": rsi_period,
    #         "rsi_trigger": rsi_trigger,
    #         "slope_start": slope_start,
    #         "slope_angle": slope_angle,
    #         "exit_after_consecutive": exit,
    #         "day": day.index[0].date(),
    #         "amount_of_orders": (df['orders'].abs().sum()) / 2,
    #         "SPY_day_end": df['Adj_SPY'][389],
    #         "min_portfolio_worth": df['current_portfolio_worth'].min(),
    #         "max_portfolio_worth": df['current_portfolio_worth'].max(),
    #         "min_max_drawdown": df['current_portfolio_worth'].max() - df['current_portfolio_worth'].min(),
    #         "final_portfolio_worth": df['current_portfolio_worth'][len(df) - 1],
    #         "kinda_sharp": (df['current_portfolio_worth'][len(df) - 1] - 100) / (
    #                     df['current_portfolio_worth'].max() - df['current_portfolio_worth'].min())
    #     },
    #         ignore_index=True)
    #     return results


    ###




if __name__ == '__main__':
    main()


