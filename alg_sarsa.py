import torch

from globals import *
from env_stocks_generator import StocksGeneratorEnv
from test_alg import test_alg


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(3, 1, dtype=torch.double)
        )

    def forward(self, x):
        x = self.model(x)
        return x


class SarsaAlg:
    def __init__(self, env):
        self.env = env
        self.nn_model = SimpleModel()

    def choose_action(self, state):
        return self.env.sample_action()
        # prev_tick, curr_tick, arrow = state
        # if curr_tick > prev_tick:
        #     return 1
        # return 0

    def learning_step(self, state, action, next_state, reward, done):
        t_state = torch.unsqueeze(torch.tensor(state), 0)
        t_output = self.nn_model(t_state)
        print(t_output)


def main():
    env = StocksGeneratorEnv()
    sarsa_alg = SarsaAlg(env=env)
    test_alg(env=env, alg=sarsa_alg, episodes=100, plot_per=50, random_seed=random_seed, seed=seed)


if __name__ == '__main__':
    # random_seed = True
    random_seed = False
    seed = 123

    if not random_seed:
        torch.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)

    main()


