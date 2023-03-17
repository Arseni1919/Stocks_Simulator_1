import datetime

from environments.env_meta_class import MetaEnv
from globals import *


def to_datestr(input_str):
    if '/' in input_str:
        datetime_var = datetime.datetime.strptime(input_str[:10], '%d/%m/%Y')
    elif '-' in input_str:
        datetime_var = datetime.datetime.strptime(input_str[:10], '%Y-%m-%d')
    else:
        raise RuntimeError('')
    output_str = datetime_var.strftime('%Y-%m-%d')
    return output_str


class KirillEnv(MetaEnv):
    def __init__(self, commission=0.0002, risk_rate=1, to_plot=False, list_of_assets=None,
                 data_dir='../data/data.json', to_shuffle=True, to_load=True):
        super().__init__(commission, risk_rate, to_plot)
        self.name = 'KirillEnv'
        self.list_of_assets = list_of_assets
        self.data_dir = data_dir
        self.to_shuffle = to_shuffle

        # for init
        self.days_dict = None
        self.all_daytimes = None
        self.all_daytimes_shuffled = None
        self.days_counter = None
        self.curr_day_data = None
        self.n_days = None

        self.build_days_dict(to_load)

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


def main():
    episodes = 1
    env = KirillEnv(to_plot=True, list_of_assets=stocks_names_list, to_load=True)
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

# for day in all_daytimes:
#     for asset in self.list_of_assets:
#         prices = self.days_dict[day][asset]['price']
#         volumes = self.days_dict[day][asset]['volume']
#         print(f'{day} | {asset} | lengths: {len(prices)} - {len(volumes)}')
#     print('---------------------')



