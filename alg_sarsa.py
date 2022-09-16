from globals import *
from env_stocks_generator import StocksGeneratorEnv
from test_alg import test_alg


class SarsaAlg:
    def __init__(self, env):
        self.env = env

    def choose_action(self, state):
        return self.env.sample_action()
        # prev_tick, curr_tick, arrow = state
        # if curr_tick > prev_tick:
        #     return 1
        # return 0

    def learning_step(self, state, action, next_state, reward, done):
        pass


def main():
    env = StocksGeneratorEnv()
    sarsa_alg = SarsaAlg(env=env)
    test_alg(env=env, alg=sarsa_alg, episodes=100, plot_per=1)


if __name__ == '__main__':
    main()


