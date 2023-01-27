from algs.alg_buy_low_sell_high import BuyLowSellHighAlg
from environments.sin_stock_env import SinStockEnv
from plot_fucntions_and_classes.plotter import PlotterBigExperiments
from globals import *


def main():
    episodes = 1
    plotter = PlotterBigExperiments()
    env = SinStockEnv()
    # alg = BuyLowSellHighAlg(env=env)
    window_sizes = [10, 20, 30, 40, 50]
    algorithms = [BuyLowSellHighAlg(env, window=w) for w in window_sizes]
    for episode in range(episodes):
        for alg_index, alg in enumerate(algorithms):
            observation, info = env.reset()
            for step in range(env.max_steps):
                print(f'\r{episode=} | {alg.name=} | {step=}', end='')
                action = alg.return_action(observation)
                next_observation, reward, terminated, truncated, info = env.step(action)
                alg.update(observation, action, reward, next_observation, terminated, truncated)
                observation = next_observation
                if step % 200 == 0 or step == env.max_steps - 1:
                    plotter.render(info={
                        'episode': episode,
                        'step': step,
                        'algorithms': algorithms,
                    })

    plt.show()


if __name__ == '__main__':
    main()

