import torch

from globals import *
from env_stocks_generator import StocksGeneratorEnv
from test_alg import test_alg


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            # nn.Linear(5, 1, dtype=torch.double),
            nn.Linear(5, 10, dtype=torch.double),
            nn.ReLU(),
            nn.Linear(10, 10, dtype=torch.double),
            nn.ReLU(),
            nn.Linear(10, 10, dtype=torch.double),
            nn.ReLU(),
            nn.Linear(10, 1, dtype=torch.double)
        )

    def forward(self, x):
        x = self.model(x)
        return x


class SarsaAlg:
    def __init__(self, env):
        self.env = env
        self.EPSILON = 0.2
        self.LR = 0.01
        self.GAMMA = 0.9
        self.v_func = SimpleModel()
        self.criterion = nn.MSELoss()  # mean-squared error for regression
        self.optimizer = torch.optim.Adam(self.v_func.parameters(), lr=self.LR)

        # for plots
        self.losses = []
        self.predictions = []
        self.g_values = []

    def choose_action(self, state):
        # return self.env.sample_action()
        prev_tick, curr_tick, time_index, arrow = state
        if curr_tick > prev_tick:
            return 1
        return 0

    def learning_step(self, state, action, next_state, reward, done):
        G = reward
        G = torch.unsqueeze(torch.tensor(G, dtype=torch.double), 0)
        G = torch.unsqueeze(torch.tensor(G), 0)
        # if done:
        #     G = reward
        #     G = torch.unsqueeze(torch.tensor(G, dtype=torch.double), 0)
        #     G = torch.unsqueeze(torch.tensor(G), 0)
        #     # print(G)
        # else:
        #     t_next_state = torch.unsqueeze(torch.tensor(next_state), 0)
        #     t_output = self.v_func(t_next_state)
        #     G = reward + self.GAMMA * t_output
        i_state = state[:]
        i_state.append(action)
        t_state = torch.unsqueeze(torch.tensor(i_state), 0)
        t_output = self.v_func(t_state)
        loss = self.criterion(t_output, G)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.losses.append(loss.item())
        self.g_values.append(G.item())
        self.predictions.append(t_output.item())

        # outputs = net(i_batch)  # forward pass
        # optimizer.zero_grad()  # caluclate the gradient, manually setting to 0
        #
        # # obtain the loss function
        # y_train_tensor = y_train_tensors[i]
        # loss = criterion(outputs, y_train_tensor)
        #
        # loss.backward()  # calculates the loss of the loss function
        #
        # optimizer.step()  # improve from loss, i.e backprop
        #
        # y_hat.append(outputs.item())
        # y_real.append(y_train_tensor.item())
        # losses.append(loss.item())
        # print(f"\rEpoch-batch: {epoch}-{i}, loss:{loss.item() : 1.5f}", end='')


def main():
    env = StocksGeneratorEnv()
    sarsa_alg = SarsaAlg(env=env)
    test_alg(env=env, alg=sarsa_alg, episodes=100, plot_per=10, random_seed=random_seed, seed=seed)


if __name__ == '__main__':
    # random_seed = True
    random_seed = False
    seed = 123

    if not random_seed:
        torch.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)

    main()


