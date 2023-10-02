from globals import *
from plot_fucntions_and_classes.plot_functions import *


def to_datestr(input_str):
    if '/' in input_str:
        datetime_var = datetime.datetime.strptime(input_str[:10], '%d/%m/%Y')
    elif '-' in input_str:
        datetime_var = datetime.datetime.strptime(input_str[:10], '%Y-%m-%d')
    else:
        raise RuntimeError('')
    output_str = datetime_var.strftime('%Y-%m-%d')
    return output_str


class StockEnv:
    def __init__(self, commission=0.001, risk_rate=1, to_plot=False, list_of_assets=None,
                 data_dir='../data/data.json', to_shuffle=True, to_load=True):
        self.name = 'StockEnv'
        self.commission = commission  # in ratio
        self.risk_rate = risk_rate  # in ratio
        self.to_plot = to_plot
        self.list_of_assets = list_of_assets
        self.data_dir = data_dir
        self.to_shuffle = to_shuffle
        self.action_space = np.array([-1, 0, 1])
        self.step_count = -1
        self.max_steps = 390  # minutes
        # global data:
        self.history_assets = None
        self.history_volume = None
        # agent data:
        self.history_actions = None
        self.history_orders = None  # how many orders we did in any kind
        self.history_portion_of_asset = None  # a portion of long or short
        self.history_portion_of_asset_worth = None  # a worth of a portion of long or short
        self.history_cash = None  # in dollars
        self.history_commission_value = None
        self.history_portfolio_worth = None
        # agent's instant data
        self.in_hand = None
        self.portion_of_asset = None
        self.cash = 100
        self.short_cash = None
        self.commission_value = 0

        self.days_dict = None
        self.all_daytimes = None
        self.all_daytimes_shuffled = None
        self.days_counter = None
        self.curr_day_data = None
        self.n_days = None

        self.build_days_dict(to_load)

        # for plots
        if self.to_plot:
            self.subplot_rows = 2
            self.subplot_cols = 3
            self.fig, self.ax = plt.subplots(self.subplot_rows, self.subplot_cols, figsize=(14, 7))
            self.ax_volume = self.ax[0, 0].twinx()

    def build_days_dict(self, to_load=True):
        if to_load:
            # Opening JSON file
            with open(self.data_dir) as json_file:
                self.days_dict = json.load(json_file)
                self.all_daytimes = list(self.days_dict.keys())
        else:
            bars_df = pd.read_csv('../data/all_data_up_to_15_1_22.csv')
            all_daytimes = [to_datestr(i_index) for i_index in bars_df['index']]
            self.all_daytimes = list(set(all_daytimes))
            self.all_daytimes.sort(key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
            self.days_dict = {day: {asset: {'price': [], 'volume': []} for asset in self.list_of_assets} for day in all_daytimes}
            for index, row in bars_df.iterrows():
                curr_day = to_datestr(row[0])
                for i_asset, i_value in row.iteritems():
                    if 'Close' in i_asset:
                        self.days_dict[curr_day][i_asset[6:]]['price'].append(i_value)
                    if 'Volume' in i_asset:
                        self.days_dict[curr_day][i_asset[7:]]['volume'].append(i_value)

            with open(self.data_dir, "w") as outfile:
                json.dump(self.days_dict, outfile)

        self.all_daytimes_shuffled = self.all_daytimes.copy()
        if self.to_shuffle:
            random.shuffle(self.all_daytimes_shuffled)
        self.days_counter = 0
        self.n_days = len(self.all_daytimes_shuffled)

    def reset_check(self):
        if self.step_count == -1:
            raise RuntimeError('Do a resset first!')

    def reset(self, params=None):
        """
        :return: observation, info
        """
        self.max_steps = 390  # minutes
        self.inner_reset(params)
        # global data
        # self.history_assets = np.zeros((self.max_steps,))
        # self.history_volume = np.zeros((self.max_steps,))
        self.history_assets = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        self.history_volume = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        # instant data
        self.step_count = 0
        self.in_hand = {asset: 0 for asset in self.list_of_assets}  # -1 -> short, 0 -> nothing, 1 -> long
        self.cash = 100
        self.short_cash = {asset: 0 for asset in self.list_of_assets}
        self.portion_of_asset = {asset: 0 for asset in self.list_of_assets}
        self.commission_value = 0
        # agent data
        self.history_actions = {asset: np.zeros((self.max_steps,)) for asset in self.list_of_assets}
        self.history_cash = np.zeros((self.max_steps,))
        self.history_portion_of_asset = np.zeros((self.max_steps,))
        self.history_portion_of_asset_worth = np.zeros((self.max_steps,))
        self.history_orders = np.zeros((self.max_steps,))
        self.history_portfolio_worth = np.zeros((self.max_steps,))
        self.history_commission_value = np.zeros((self.max_steps,))
        self.history_cash[0] = self.cash
        self.history_portfolio_worth[0] = self.cash

        observation = self.generate_next_observation()
        info = {}
        return observation, info

    def inner_reset(self, params=None):
        """
        Sample a day
        """
        # sample a random day (without repeats)
        if self.days_counter >= len(self.all_daytimes_shuffled):
            self.days_counter = 0
            print('[INFO] finished round on data')
        if params and 'episode' in params:
            self.days_counter = params['episode'] % self.n_days
        next_day = self.all_daytimes_shuffled[self.days_counter]
        self.days_counter += 1
        self.curr_day_data = self.days_dict[next_day]
        # print(f'\n{next_day=}\n')
        # first_asset = self.list_of_assets[0]
        # self.max_steps = len(self.curr_day_data[first_asset]['price'])

    def generate_next_assets(self):
        step_count = self.step_count
        for asset in self.list_of_assets:
            if step_count < len(self.curr_day_data[asset]['price']):
                self.history_assets[asset][step_count] = self.curr_day_data[asset]['price'][step_count]
                self.history_volume[asset][step_count] = self.curr_day_data[asset]['volume'][step_count]

    def generate_next_observation(self):
        observation = {}
        step_count = self.step_count
        self.generate_next_assets()
        # global data:
        observation['asset'] = {asset: self.history_assets[asset][step_count] for asset in self.list_of_assets}
        observation['asset_volume'] = {asset: self.history_volume[asset][step_count] for asset in self.list_of_assets}
        # current state data:
        observation['step_count'] = step_count
        observation['in_hand'] = self.in_hand
        # agent data:
        step_count = 1 if step_count == 0 else step_count
        step_count = 0 if step_count == -1 else step_count
        observation['history_cash'] = self.history_cash[step_count - 1]
        observation['history_portion_of_asset'] = self.history_portion_of_asset[step_count - 1]
        observation['history_portion_of_asset_worth'] = self.history_portion_of_asset_worth[step_count - 1]
        observation['history_orders'] = self.history_orders[step_count - 1]
        observation['history_portfolio_worth'] = self.history_portfolio_worth[step_count - 1]
        observation['history_commission_value'] = self.history_commission_value[step_count - 1]

        return observation

    def sample_action(self, asset=None):
        # return np.random.choice(self.action_space, p=[0.9, 0.05, 0.05])
        if asset:
            return [(asset, np.random.choice(self.action_space, p=[0.05, 0.9, 0.05]))]
        return [(i_asset, np.random.choice(self.action_space, p=[0.05, 0.9, 0.05])) for i_asset in self.list_of_assets]

    def enter_short(self, asset, current_price):
        self.in_hand[asset] = -1
        cash_to_invest_before_commission = self.cash * self.risk_rate
        self.cash -= cash_to_invest_before_commission
        cash_to_invest_after_commission = cash_to_invest_before_commission / (1 + self.commission)
        self.portion_of_asset[asset] = - cash_to_invest_after_commission / current_price
        self.short_cash[asset] = cash_to_invest_after_commission
        self.commission_value = self.commission * cash_to_invest_after_commission
        return True

    def exit_short(self, asset, current_price):
        self.in_hand[asset] = 0
        loan_to_receive_before_commission = abs(self.portion_of_asset[asset]) * current_price
        self.commission_value = self.commission * loan_to_receive_before_commission
        loan_to_receive_after_commission = loan_to_receive_before_commission - self.commission_value
        revenue_to_receive_after_commission = self.short_cash[asset] - loan_to_receive_after_commission
        self.cash += self.short_cash[asset] + revenue_to_receive_after_commission
        self.portion_of_asset[asset] = 0
        self.short_cash[asset] = 0
        return True

    def enter_long(self, asset, current_price):
        self.in_hand[asset] = 1
        cash_to_invest_before_commission = self.cash * self.risk_rate
        self.cash -= cash_to_invest_before_commission
        cash_to_invest_after_commission = cash_to_invest_before_commission / (1 + self.commission)
        self.portion_of_asset[asset] = cash_to_invest_after_commission / current_price
        self.commission_value = self.commission * cash_to_invest_after_commission
        return True

    def exit_long(self, asset, current_price):
        self.in_hand[asset] = 0
        cash_to_receive_before_commission = self.portion_of_asset[asset] * current_price
        self.commission_value = self.commission * cash_to_receive_before_commission
        cash_to_receive_after_commission = cash_to_receive_before_commission - self.commission_value
        self.cash += cash_to_receive_after_commission
        self.portion_of_asset[asset] = 0
        return True

    def check_margin_call(self, asset, current_price):
        loan_to_receive_before_commission = abs(self.portion_of_asset[asset]) * current_price
        commission_value = self.commission * loan_to_receive_before_commission
        loan_to_receive_after_commission = loan_to_receive_before_commission - commission_value
        if 1.8 * self.short_cash[asset] < loan_to_receive_after_commission:
            print('\n-----\nMARGIN CALL\n-----\n')
            return True
        return False

    def exec_action(self, asset, action, current_price):
        """
        :return:
        """
        # asset_in_hand = self.in_hand[asset]
        if self.in_hand[asset] == 0:
            if self.step_count + 1 == self.max_steps:
                return False
            if action == 1:
                return self.enter_long(asset, current_price)
            if action == -1:
                return self.enter_short(asset, current_price)
        elif self.in_hand[asset] == -1:
            margin_call = self.check_margin_call(asset, current_price)
            if self.step_count + 1 == self.max_steps or margin_call:
                return self.exit_short(asset, current_price)
            if action == 1:
                return self.exit_short(asset, current_price)
        elif self.in_hand[asset] == 1:
            if self.step_count + 1 == self.max_steps:
                return self.exit_long(asset, current_price)
            if action == -1:
                return self.exit_long(asset, current_price)
        else:
            raise RuntimeError('in_hand - wrong')
        return False

    def step(self, actions):
        """
        :return: observation, reward, terminated, truncated, info
        """
        self.reset_check()
        observation, reward, terminated, truncated, info = {}, 0, False, False, {}

        # execute actions
        for action_tuple in actions:
            asset, action = action_tuple
            current_price = self.history_assets[asset][self.step_count]
            executed = self.exec_action(asset, action, current_price)  # reward in dollars
            self.update_history_after_action(asset, current_price)
            self.commission_value = 0
            if executed:
                self.history_orders[self.step_count] += 1
                self.history_actions[asset][self.step_count] = action

        # get reward
        portfolio_worth = self.history_portfolio_worth[self.step_count]

        # is it terminated / truncated?
        self.step_count += 1
        if self.step_count >= self.max_steps:
            terminated = True
            self.step_count = -1

        # get NEXT observation
        observation = self.generate_next_observation()

        # gather info
        info = {}

        return observation, portfolio_worth, terminated, truncated, info

    def update_history_after_action(self, asset, current_price):
        self.history_portion_of_asset[self.step_count] = self.portion_of_asset[asset]
        self.history_cash[self.step_count] = self.cash
        self.history_commission_value[self.step_count] += self.commission_value
        if self.portion_of_asset[asset] > 0:  # long
            h_holdings_worth = self.portion_of_asset[asset] * current_price
        elif self.portion_of_asset[asset] < 0:  # short
            loan_to_receive_before_commission = abs(self.portion_of_asset[asset]) * current_price
            revenue_to_receive_before_commission = self.short_cash[asset] - loan_to_receive_before_commission
            h_holdings_worth = self.short_cash[asset] + revenue_to_receive_before_commission
        else:  # portion_of_asset is 0
            h_holdings_worth = 0
        self.history_portion_of_asset_worth[self.step_count] = h_holdings_worth
        if self.cash + h_holdings_worth == 0:
            print('here')
        self.history_portfolio_worth[self.step_count] = self.cash + h_holdings_worth

    def close(self):
        pass

    def render(self, info=None):
        if self.to_plot:
            self.render_graphs(self.ax, self.ax_volume, info)
            main_asset = info['main_asset']
            title = f'main_asset: {main_asset}'
            if "alg_name" in info:
                title += f' Alg: {info["alg_name"]}'
            self.fig.suptitle(title, fontsize=16)
            plt.pause(0.001)

    def render_graphs(self, ax, ax_volume, info=None):
        info['step_count'] = self.step_count
        info['max_steps'] = self.max_steps
        info['history_assets'] = self.history_assets
        info['history_actions'] = self.history_actions
        info['history_volume'] = self.history_volume
        info['history_cash'] = self.history_cash
        info['history_orders'] = self.history_orders
        info['history_portion_of_asset'] = self.history_portion_of_asset
        info['history_portion_of_asset_worth'] = self.history_portion_of_asset_worth
        info['history_portfolio_worth'] = self.history_portfolio_worth
        info['history_commission_value'] = self.history_commission_value

        plot_asset_and_actions(ax[0, 0], info=info)
        plot_volume(ax_volume, info=info)
        plot_rewards(ax[0, 1], info=info)
        plot_commissions(ax[0, 2], info=info)
        plot_property(ax[1, 0], info=info)
        # plot_variance(ax[1, 1], info=info)
        plot_orders(ax[1, 1], info=info)
        plot_average(ax[1, 2], info=info)



def main():
    episodes = 1
    env = StockEnv(to_plot=True, list_of_assets=stocks_names_list, to_load=True)
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


if __name__ == '__main__':
    main()










