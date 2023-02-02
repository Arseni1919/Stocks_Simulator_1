from globals import *
from environments.sin_stock_env import SinStockEnv
from algs.alg_meta_class import MetaAlg
from plot_fucntions_and_classes.plot_functions import *


class BuyLowSellHighAlg(MetaAlg):

    def __init__(self, env, to_plot=False, params=None):
        super().__init__()
        # init
        if params is None:
            params = {'w1': 40, 'w2': 20}
        self.env = env
        self.params = params
        self.name = f'BLSH-{self.params["w1"]}-{self.params["w2"]}'
        self.to_plot = to_plot
        self.max_steps = self.env.max_steps
        # global data
        self.list_of_assets = self.env.list_of_assets
        self.main_asset = self.list_of_assets[0]
        self.history_assets = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        self.history_volume = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        # agents data
        self.history_actions = np.zeros((self.max_steps,))
        self.history_cash = np.zeros((self.max_steps,))
        self.history_holdings = np.zeros((self.max_steps,))
        self.history_holdings_worth = np.zeros((self.max_steps,))
        self.history_orders = np.zeros((self.max_steps,))
        self.history_portfolio_worth = np.zeros((self.max_steps,))
        self.history_commission_value = np.zeros((self.max_steps,))
        self.history_property = np.zeros((self.max_steps,))
        self.history_termination = np.zeros((self.max_steps,))
        # for plots
        if self.to_plot:
            self.subplot_rows = 2
            self.subplot_cols = 3
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            self.ax_volume = self.ax[0, 0].twinx()

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

    def update_history(self, observation):
        # current state data:
        step_count = observation['step_count']
        in_hand = observation['in_hand']
        # global data:
        for asset in self.list_of_assets:
            self.history_assets[asset][step_count] = observation['asset'][asset]
            self.history_volume[asset][step_count] = observation['asset_volume'][asset]
        # agent data:
        self.history_cash[step_count] = observation['history_cash']
        self.history_holdings[step_count] = observation['history_holdings']
        self.history_holdings_worth[step_count] = observation['history_holdings_worth']
        self.history_orders[step_count] = observation['history_orders']
        self.history_portfolio_worth[step_count] = observation['history_portfolio_worth']
        self.history_commission_value[step_count] = observation['history_commission_value']
        return step_count, in_hand

    def update_after_action(self, observation, action, portfolio_worth, next_observation, terminated, truncated):
        step_count = observation['step_count']
        last_action_asset, last_action_value = action[-1]
        self.history_actions[step_count] = last_action_value
        self.history_termination[step_count] = terminated

    def render(self, info):
        if self.to_plot:
            info['main_asset'] = self.main_asset
            self.env.render_graphs(self.ax, self.ax_volume, info)
            self.fig.suptitle(f'Alg: {self.name}', fontsize=16)
            plt.pause(0.001)


def main():
    episodes = 1
    w1, w2 = 10, 20
    env = SinStockEnv(risk_rate=1)
    alg = BuyLowSellHighAlg(env=env, to_plot=True, params={'w1': w1, 'w2': w2})
    observation, info = env.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
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


