from globals import *
from environments.sin_stock_env import SinStockEnv
from environments.alpaca_env import AlpacaEnv
from environments.kirill_env import KirillEnv
from algs.alg_meta_class import MetaAlg
from plot_fucntions_and_classes.plot_functions import *


class MomentumLastHour(MetaAlg):

    def __init__(self, env, to_plot=False, params=None):
        super().__init__(env, to_plot, params)
        # init
        if params is None:
            self.params = {'w1': 40, 'w2': 20}
        self.name = f'MomentumLastHour'
        self.rolling_list = []

    @staticmethod
    def calc_slope(window_df, multiplier=100):
        result = (window_df.iloc[len(window_df) - 1] - window_df.iloc[0]) / len(window_df)
        return result * multiplier

    def return_action(self, observation):
        action = 0
        step_count, in_hand = self.update_history(observation)

        ts = pd.Series(self.history_assets[self.main_asset][0:step_count])

        slope_day_start = ts.rolling(400, min_periods=22).apply(self.calc_slope).fillna(0.0001)

        if step_count == 330 and (slope_day_start[:330] >= -2).all():
            action = 1

        if step_count == 330 and (slope_day_start[:330] <= 2).all():
            action = -1

        return [(self.main_asset, action)]

    def update_after_action(self, observation, action, portfolio_worth, next_observation, terminated, truncated):
        step_count = observation['step_count']
        last_action_asset, last_action_value = action[-1]
        self.history_actions[last_action_asset][step_count] = last_action_value
        self.history_termination[step_count] = terminated


def main():
    episodes = 1
    w1, w2 = 10, 20
    # env = SinStockEnv(risk_rate=1)
    # env = AlpacaEnv(list_of_assets=assets_names_list[:3])
    env = KirillEnv(list_of_assets=assets_names_list)
    alg = MomentumLastHour(env=env, to_plot=True)
    observation, info = env.reset()
    alg.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\repisode={episode} | step={step}', end='')
            action = alg.return_action(observation)
            next_observation, portfolio_worth, terminated, truncated, info = env.step(action)
            alg.update_after_action(observation, action, portfolio_worth, next_observation, terminated, truncated)
            observation = next_observation

            if step % 200 == 0 or step == env.max_steps - 1:
                # env.render(info={'episode': episode, 'step': step, 'alg_name': alg.name})
                alg.render(info={'episode': episode, 'step': step, 'w1': w1, 'w2': w2})

    plt.show()


if __name__ == '__main__':
    main()


