
from environments.env_meta_class import MetaEnv
from globals import *


class AlpacaEnv(MetaEnv):
    def __init__(self, commission=0.001, risk_rate=1, to_plot=False, list_of_assets=None):
        super().__init__(commission, risk_rate, to_plot)
        self.name = 'AlpacaEnv'
        self.list_of_assets = list_of_assets

        # for init
        self.first_init = True
        self.client = StockHistoricalDataClient(os.environ['API_KEY'], os.environ['SECRET_KEY'])
        self.days_dict = None
        self.all_daytimes = None
        self.all_daytimes_shuffled = None
        self.days_counter = None
        self.curr_day_data = None

    def build_days_dict(self, bars_df):
        first_asset = self.list_of_assets[0]
        day_format = '%Y-%m-%d'
        all_daytimes = [bar_index[1].strftime(day_format) for bar_index in bars_df.index if bar_index[0] == first_asset]
        all_daytimes = list(set(all_daytimes))
        self.all_daytimes = all_daytimes
        self.all_daytimes_shuffled = self.all_daytimes.copy()
        random.shuffle(self.all_daytimes_shuffled)
        self.days_counter = 0
        self.days_dict = {day: {asset: {'price': [], 'volume': []} for asset in self.list_of_assets} for day in all_daytimes}
        for index, row in bars_df.iterrows():
            curr_day = index[1].strftime(day_format)
            curr_asset = index[0]
            self.days_dict[curr_day][curr_asset]['price'].append(row.close)
            self.days_dict[curr_day][curr_asset]['volume'].append(row.volume)
        for day in all_daytimes:
            for asset in self.list_of_assets:
                prices = self.days_dict[day][asset]['price']
                volumes = self.days_dict[day][asset]['volume']
                print(f'{day} | {asset} | lengths: {len(prices)} - {len(volumes)}')
            print('---------------------')

    def inner_reset(self):
        """
        Sample a day
        """
        if self.first_init:
            self.first_init = False
            # download a year
            request_params = StockBarsRequest(
                symbol_or_symbols=self.list_of_assets,
                timeframe=TimeFrame.Minute,
                # start="2018-01-01 00:00:00"
                start=datetime.datetime.today() - datetime.timedelta(days=3)
            )
            bars = self.client.get_stock_bars(request_params)
            self.build_days_dict(bars.df)

        # sample a random day (without repeats)
        if self.days_counter >= len(self.all_daytimes_shuffled):
            raise RuntimeError()
        next_day = self.all_daytimes_shuffled[self.days_counter]
        self.days_counter += 1
        self.curr_day_data = self.days_dict[next_day]
        first_asset = self.list_of_assets[0]
        self.max_steps = len(self.curr_day_data[first_asset]['price'])

    def generate_next_assets(self):
        step_count = self.step_count
        for asset in self.list_of_assets:
            if step_count < len(self.curr_day_data[asset]['price']):
                self.history_assets[asset][step_count] = self.curr_day_data[asset]['price'][step_count]
                self.history_volume[asset][step_count] = self.curr_day_data[asset]['volume'][step_count]


def main():
    episodes = 1
    env = AlpacaEnv(to_plot=True, list_of_assets=stocks_names_list[:3])
    observation, info = env.reset()
    for episode in range(episodes):
        for step in range(env.max_steps):
            print(f'\r{episode=} | {step=}', end='')
            action = env.sample_action()
            env.step(action)
            if step % 200 == 0 or step == env.max_steps - 1:
                env.render(info={'episode': episode,
                                 'step': step, 'main_asset': 'SPY'})

    plt.show()


if __name__ == '__main__':
    main()



