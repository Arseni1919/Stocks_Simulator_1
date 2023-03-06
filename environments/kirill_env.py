from environments.env_meta_class import MetaEnv
from globals import *


class KirillEnv(MetaEnv):
    def __init__(self, commission=0.001, risk_rate=1, to_plot=False, list_of_assets=None):
        super().__init__(commission, risk_rate, to_plot)
        self.name = 'KirillEnv'
        self.list_of_assets = list_of_assets

        # for init
        self.first_init = True
        self.days_dict = None
        self.all_daytimes = None
        self.all_daytimes_shuffled = None
        self.days_counter = None
        self.curr_day_data = None

    def build_days_dict(self, bars_df, to_load=True):
        all_daytimes = [i_index[:10] for i_index in bars_df['index']]
        all_daytimes = list(set(all_daytimes))
        self.all_daytimes = all_daytimes
        self.all_daytimes_shuffled = self.all_daytimes.copy()
        random.shuffle(self.all_daytimes_shuffled)
        self.days_counter = 0

        if to_load:
            # Opening JSON file
            with open('../data/data.json') as json_file:
                self.days_dict = json.load(json_file)
        else:
            self.days_dict = {day: {asset: {'price': [], 'volume': []} for asset in self.list_of_assets} for day in all_daytimes}
            for index, row in bars_df.iterrows():
                curr_day = row[0][:10]
                for i_asset, i_value in row.iteritems():
                    if 'Close' in i_asset:
                        self.days_dict[curr_day][i_asset[6:]]['price'].append(i_value)
                    if 'Volume' in i_asset:
                        self.days_dict[curr_day][i_asset[7:]]['volume'].append(i_value)

            with open("../data/data.json", "w") as outfile:
                json.dump(self.days_dict, outfile)

    def inner_reset(self):
        """
        Sample a day
        """
        if self.first_init:
            self.first_init = False
            # download a csv

            bars_df = pd.read_csv('../data/all_data_up_to_15_1_22.csv')
            self.build_days_dict(bars_df)

        # sample a random day (without repeats)
        if self.days_counter >= len(self.all_daytimes_shuffled):
            self.days_counter = 0
            print('[INFO] finished round on data')
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
    env = KirillEnv(to_plot=True, list_of_assets=stocks_names_list)
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



