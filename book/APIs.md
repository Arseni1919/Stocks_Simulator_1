## Simulators API

### Usage:

```python
def main():
    episodes = 1
    env = SomeEnv(to_plot=True, list_of_assets=stocks_names_list)
    observation, info = env.reset()
    main_asset = 'SPY'
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
            action = env.sample_action(main_asset)
            env.step(action)
            if step % 200 == 0 or step == env.max_steps - 1:
                env.render(info={'episode': episode,
                                 'step': step, 'main_asset': main_asset})

    plt.show()
```
## Algorithms API

### Need To Implement:

```python
from algs.alg_meta_class import MetaAlg

class SomeAlg(MetaAlg):

    def __init__(self, env, to_plot=False, params=None):
        super().__init__(env, to_plot, params)
        # init
        # <your init>
        self.name = f'<give a name>'

    def return_action(self, observation):
        """
        --- INPUT --- 
        observation:
            # global data:
            observation['asset'] = {asset: NUMBER for asset in self.list_of_assets}
            observation['asset_volume'] = {asset: NUMBER for asset in self.list_of_assets}
            # current state data:
            observation['step_count'] = step_count (int)
            observation['in_hand'] = NUMBER (-1, 0, 1)
            # agent data:
            observation['history_cash'] = NUMBER
            observation['history_holdings'] = NUMBER
            observation['history_holdings_worth'] = NUMBER
            observation['history_orders'] = NUMBER
            observation['history_portfolio_worth'] = NUMBER
            observation['history_commission_value'] = NUMBER
        
        --- OUTPUT ---
        List of (asset, action) tuples. 
        Examples: 
            return [(self.main_asset, 0)]
            return [(self.main_asset, 0), (self.main_asset, -1)]
        """
        # <calculate something>
        # <...>
        # return list of actions
        return [(self.main_asset, 0)]
        # or
        return [(self.main_asset, 0), (self.main_asset, -1)]


    def update_after_action(self, observation, action, portfolio_worth, next_observation, terminated, truncated):
        # <do something after taking an action>
        pass
```

### Usage:

```python
def main():
    episodes = 1
    w1, w2 = 10, 20
    # env = SinStockEnv(risk_rate=1)
    env = SomeEnv(list_of_assets=stocks_names_list)
    alg = SomeAlg(env=env, to_plot=True, params={...})
    for episode in range(episodes):
        observation, info = env.reset()
        alg.reset()
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
```