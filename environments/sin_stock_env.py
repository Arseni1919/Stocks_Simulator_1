import matplotlib.pyplot as plt
import numpy as np
from environments.env_meta_class import MetaEnv
from plot_fucntions_and_classes.plot_functions import *
from globals import *


class SinStockEnv(MetaEnv):
    def __init__(self, commission=0.001, risk_rate=1, to_plot=False):
        super().__init__(commission, risk_rate, to_plot)
        self.name = 'SinStockEnv'
        self.list_of_assets = ['sin']

    def generate_next_assets(self):
        step_count = self.step_count
        for asset in self.list_of_assets:
            prev_asset_value = 100 if step_count == 0 else self.history_assets[asset][step_count - 1]
            var = 3
            sin_part = np.sin(step_count / 15)
            asset_value = prev_asset_value + sin_part / 100 * prev_asset_value + np.random.randint(-var,
                                                                                                   var + 1) / 100 * prev_asset_value
            self.history_assets[asset][step_count] = asset_value
            self.history_volume[asset][step_count] = sin_part * 5 + 5 + np.random.randint(1, 10)


def main():
    episodes = 1
    env = SinStockEnv(to_plot=True)
    observation, info = env.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
            action = env.sample_action()
            env.step(action)
            if step % 200 == 0 or step == env.max_steps - 1:
                env.render(info={'episode': episode,
                                 'step': step, 'main_asset': 'sin'})

    plt.show()


if __name__ == '__main__':
    main()



