from algs.alg_buy_low_sell_high import BuyLowSellHighAlg
from algs.momentum_last_hour import MomentumLastHour
from environments.sin_stock_env import SinStockEnv
from environments.stock_env_class import StockEnv
from plot_fucntions_and_classes.plot_functions import *
from globals import *


class AlgsTester:

    def __init__(self, env, algs_to_test, to_render=False, episodes=1):
        self.env = env
        self.algs_to_test = algs_to_test
        self.to_render = to_render
        self.episodes = episodes
        self.name = 'Algorithms-Tester'
        self.max_steps = self.env.max_steps
        self.n_days = self.env.n_days

        # for stats
        self.stats_dict = {
            alg.name: {
                "returns": np.ones((episodes, self.max_steps)) * 100,
            } for alg in self.algs_to_test
        }

        # for plots
        if self.to_render:
            self.subplot_rows = 1
            self.subplot_cols = 2
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            # self.ax_volume = self.ax[0, 0].twinx()

    def evaluate(self):

        for episode in range(self.episodes):
            for alg_index, alg in enumerate(self.algs_to_test):

                # reset both the env and the algorithm
                observation, info = self.env.reset(params={'episode': episode})
                alg.reset()

                for step in range(self.max_steps):
                    print(f'\r{episode=} | {alg.name=} | {step=}', end='')

                    action = alg.return_action(observation)
                    next_observation, portfolio_worth, terminated, truncated, info = self.env.step(action)
                    alg.update_after_action(observation, action, portfolio_worth, next_observation, terminated)
                    observation = next_observation

                    # update stats
                    self.stats_dict[alg.name]['returns'][episode, step] = portfolio_worth

                    # plot
                    self.render(episode, alg_index, alg, step)

        return self.stats_dict

    def render(self, episode, alg_index, alg, step):
        if self.to_render:
            if episode % 1 == 0 and alg_index == len(self.algs_to_test) - 1 and step == self.max_steps - 1:
                info = {
                    'episode': episode,
                    'alg_index': alg_index,
                    'alg': alg,
                    'step': step,
                    'stats_dict': self.stats_dict,
                    'max_steps': self.max_steps,
                }
                plot_algs_returns(self.ax[0], info=info)
                self.fig.suptitle(f'{self.name}', fontsize=16)
                plt.pause(0.001)


def main():
    episodes = 100
    # env = SinStockEnv()
    env = StockEnv(list_of_assets=assets_names_list, data_dir='data/data.json', to_shuffle=True)
    # alg = BuyLowSellHighAlg(env=env)
    window_sizes = [10, 20, 30, 40, 50, 60, 70]
    algorithms = [
        BuyLowSellHighAlg(env, params={'w1': 10, 'w2': 20}),
        BuyLowSellHighAlg(env, params={'w1': 40, 'w2': 20}),
        BuyLowSellHighAlg(env, params={'w1': 70, 'w2': 20}),
        MomentumLastHour(env)
    ]

    algs_tester = AlgsTester(env=env, algs_to_test=algorithms, to_render=True, episodes=episodes)
    stats_dict = algs_tester.evaluate()

    plt.show()


if __name__ == '__main__':
    main()

