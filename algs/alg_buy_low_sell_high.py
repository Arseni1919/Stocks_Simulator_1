from globals import *
from environments.sin_stock_env import SinStockEnv


class BuyLowSellHighAlg:

    def __init__(self, env):
        self.env = env
        self.name = 'BuyLowSellHighAlg'

    def return_action(self, observation):
        return self.env.sample_action()

    def update(self):
        pass


def main():
    episodes = 1
    env = SinStockEnv()
    alg = BuyLowSellHighAlg(env=env)
    observation, info = env.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            action = alg.return_action(observation)
            env.step(action)
            if step % 200 == 0 or step == env.max_steps - 1:
                env.render(info={'episode': episode, 'step': step, 'alg_name': alg.name})

    plt.show()


if __name__ == '__main__':
    main()

