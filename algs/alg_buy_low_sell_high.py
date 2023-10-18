from globals import *
from environments.sin_stock_env import SinStockEnv
from environments.alpaca_env import AlpacaEnv
from environments.stock_env_class import StockEnv
from algs.alg_meta_class import MetaAlg
from plot_fucntions_and_classes.plot_functions import *


class BuyLowSellHighAlg(MetaAlg):

    def __init__(self, env, to_plot=False, params=None):
        super().__init__(env, to_plot, params)
        # init
        if params is None:
            self.params = {'w1': 40, 'w2': 20}
        self.name = f'BLSH-{self.params["w1"]}-{self.params["w2"]}'

    @staticmethod
    def action_decision(in_hand, det_big, det_small):
        next_in_hand = 0
        action = 0
        if in_hand == 0:
            if det_big > 0 and det_small > 0:
                action = 1
                next_in_hand = 1
            if det_big < 0 and det_small < 0:
                action = -1
                next_in_hand = -1
        if in_hand == 1:
            if det_big > 0 and det_small < 0:
                action = -1
            if det_big < 0 and det_small < 0:
                action = -1
        if in_hand == -1:
            if det_big < 0 and det_small > 0:
                action = 1
            if det_big > 0 and det_small > 0:
                action = 1
        return action, next_in_hand

    def return_action(self, observation):
        # self.params['w1'] = self.params['w1'] * 1.2
        action = [0, 0]
        step_count, in_hand = self.update_history(observation)
        w1, w2 = self.params['w1'], self.params['w2']
        if step_count > max(w1, w1) + 2:
            ts = pd.Series(self.history_assets[self.main_asset][0:step_count])
            data = ts.rolling(window=w1).mean().to_numpy()
            data_sw = ts.rolling(window=w2).mean().to_numpy()
            det_big = data[-1] - data[-2]
            det_small = data_sw[-1] - data_sw[-2]
            action[0], next_in_hand = self.action_decision(in_hand, det_big, det_small)
            action[1], _ = self.action_decision(next_in_hand, det_big, det_small)

        return [(self.main_asset, action[0]), (self.main_asset, action[1])]

    def update_after_action(self, observation, action, portfolio_worth, next_observation, terminated):
        step_count = observation['step_count']
        last_action_asset, last_action_value = action[-1]
        self.history_actions[last_action_asset][step_count] = last_action_value

    def update_parameters(self):
        pass


def main():
    episodes = 1
    w1, w2 = 10, 20
    # env = SinStockEnv(risk_rate=1)
    # env = AlpacaEnv(list_of_assets=stocks_names_list[:3])
    env = StockEnv(list_of_assets=stocks_names_list)
    alg = BuyLowSellHighAlg(env=env, to_plot=True, params={'w1': w1, 'w2': w2})
    observation, info = env.reset()
    alg.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
            action = alg.return_action(observation)
            next_observation, portfolio_worth, terminated, info = env.step(action)
            alg.update_after_action(observation, action, portfolio_worth, next_observation, terminated)
            observation = next_observation

            if step % 10 == 0 or step == env.max_steps - 1:
                # env.render(info={'episode': episode, 'step': step, 'alg_name': alg.name})
                alg.render(info={'episode': episode, 'step': step, 'w1': w1, 'w2': w2})

    plt.show()


if __name__ == '__main__':
    main()


