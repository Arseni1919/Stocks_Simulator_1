from globals import *


class MetaAlg(ABC):
    def __init__(self, env, to_plot=False, params=None):
        self.name = 'Alg'
        self.env = env
        self.params = params
        self.to_plot = to_plot
        self.max_steps = None
        # global data
        self.list_of_assets = self.env.list_of_assets
        self.main_asset = self.list_of_assets[0]
        self.history_assets = None
        self.history_volume = None
        # agents data
        self.history_actions = None
        self.history_cash = None
        self.history_holdings = None
        self.history_holdings_worth = None
        self.history_orders = None
        self.history_portfolio_worth = None
        self.history_commission_value = None
        # for plots
        if self.to_plot:
            self.subplot_rows = 2
            self.subplot_cols = 3
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            self.ax_volume = self.ax[0, 0].twinx()

    def reset(self):
        self.max_steps = self.env.max_steps
        # global data
        self.history_assets = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        self.history_volume = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        # agents data
        self.history_actions = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        self.history_cash = np.zeros((self.max_steps,))
        self.history_holdings = np.zeros((self.max_steps,))
        self.history_holdings_worth = np.zeros((self.max_steps,))
        self.history_orders = np.zeros((self.max_steps,))
        self.history_portfolio_worth = np.zeros((self.max_steps,))
        self.history_commission_value = np.zeros((self.max_steps,))

    @abstractmethod
    def return_action(self, observation):
        """
        :param observation:
        :return: action
        """
        pass

    @abstractmethod
    def update_after_action(self, observation, action, reward, next_observation, terminated, truncated):
        pass

    def update_history(self, observation):
        # current state data:
        step_count = observation['step_count']
        in_hand = observation['in_hand'][self.main_asset]
        # global data:
        for asset in self.list_of_assets:
            self.history_assets[asset][step_count] = observation['asset'][asset]
            self.history_volume[asset][step_count] = observation['asset_volume'][asset]
        # agent data:
        self.history_cash[step_count] = observation['history_cash']
        self.history_holdings[step_count] = observation['history_portion_of_asset']
        self.history_holdings_worth[step_count] = observation['history_portion_of_asset_worth']
        self.history_orders[step_count] = observation['history_orders']
        self.history_portfolio_worth[step_count] = observation['history_portfolio_worth']
        self.history_commission_value[step_count] = observation['history_commission_value']
        return step_count, in_hand

    def render(self, info):
        if self.to_plot:
            info['main_asset'] = self.main_asset
            self.env.render_graphs(self.ax, self.ax_volume, info)
            self.fig.suptitle(f'Sim: {self.env.name}, Alg: {self.name}', fontsize=16)
            plt.pause(0.001)
