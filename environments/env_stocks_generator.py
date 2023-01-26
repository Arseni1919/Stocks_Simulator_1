from globals import *


class StocksGeneratorEnv:
    def __init__(self, n_actions=2):
        self.n_actions = n_actions
        self.action_space = list(range(self.n_actions))
        self.state_space = [0]
        self.ticks = []
        self.max_length = 200
        self.data = np.sin(np.arange(self.max_length)/10)
        self.prev_tick = 0
        self.arrow = 0
        self.arrows = []
        # render
        self.fig, self.axs = plt.subplots(1, 3, figsize=(10, 4))  # , figsize=(9, 3), sharey=True

    def sample_action(self):
        return random.choice(self.action_space)

    def sample_state(self):
        pass

    def reset(self):
        tick = self.data[0]
        self.ticks = [tick]
        self.arrow = 0
        self.arrows = []
        self.arrows.append([len(self.ticks) - 1, tick, self.arrow])
        self.prev_tick = tick
        state = self.calc_next_state(action=1, reset=True)
        return state

    def calc_arrow(self, action, next_tick):
        prev_arrow = self.arrow
        if action == 0:
            self.arrow = -1
        elif action == 1:
            self.arrow = 1
        # elif action == 2:
        #     self.arrow = 1
        else:
            raise RuntimeError('wrong arrow')
        if prev_arrow != self.arrow:
            self.arrows.append([len(self.ticks) - 1, next_tick, self.arrow])

    def calc_next_state(self, action, reset=False):
        if reset:
            next_state = [self.data[0], self.data[0], 0, self.arrow]
            return next_state
        data_index = len(self.ticks)
        next_tick = self.data[data_index]
        self.ticks.append(next_tick)
        self.calc_arrow(action, next_tick)
        next_state = [self.prev_tick, next_tick, data_index, self.arrow]
        return next_state

    def calc_reward(self, next_tick):
        if self.prev_tick < next_tick:
            if self.arrow == 1:
                return 1
        # elif self.prev_tick == next_tick:
        #     if self.arrow == 0:
        #         return 1
        elif self.prev_tick > next_tick:
            if self.arrow == -1:
                return 1
        return -1

    def calc_done(self):
        done = len(self.ticks) == self.max_length
        return done

    def step(self, action):

        next_state = self.calc_next_state(action)
        prev_tick, curr_tick, time_index, arrow = next_state
        reward = self.calc_reward(next_tick=curr_tick)
        done = self.calc_done()
        self.prev_tick = curr_tick
        return next_state, reward, done

    def render(self, returns=None, alg=None):
        for ax_i in self.axs:
            ax_i.cla()

        # self.axs[0]
        self.axs[0].set_xlim([0, self.max_length])
        self.axs[0].set_ylim([-1, 1])
        self.axs[0].plot(self.ticks, c='k')
        ups_x = [i[0] for i in self.arrows if i[2] == 1]
        ups_y = [i[1] for i in self.arrows if i[2] == 1]
        downs_x = [i[0] for i in self.arrows if i[2] == -1]
        downs_y = [i[1] for i in self.arrows if i[2] == -1]
        self.axs[0].scatter(ups_x, ups_y, marker='^', c='g')
        self.axs[0].scatter(downs_x, downs_y, marker='v', c='r')
        self.axs[0].set_title('Stock')

        # self.axs[1]
        self.axs[1].set_title('Total Reward')
        self.axs[1].set_xlim([0, self.max_length])
        if returns:
            self.axs[1].plot(returns, label='actual return')
        if alg:
            self.axs[1].plot(alg.predictions, label='predictions')
            self.axs[1].plot(alg.g_values, label='g_values')
        self.axs[1].legend()

        # self.axs[2]
        self.axs[2].set_title('Loss')
        if alg:
            self.axs[2].plot(alg.losses)
        # self.axs[2].set_xlim([0, self.max_length])

        plt.pause(0.001)

        return self.fig


def greedy_strategy(state):
    prev_tick, curr_tick, data_index, arrow = state
    if curr_tick > prev_tick:
        return 1
    return 0


def main():
    env = StocksGeneratorEnv()
    state = env.reset()
    done = False

    for episode in range(EPISODES):
        counter = 0
        total_return = 0
        returns = []
        while not done:
            counter += 1
            # action = env.sample_action()
            action = greedy_strategy(state)
            next_state, reward, done = env.step(action)

            # stats
            total_return += reward
            returns.append(total_return)

            # Learning
            pass

            state = next_state

            # print + plot
            print(f'\r[ep. {episode}, step {counter}] return: {total_return}, state: {state}', end='')
            if counter % PLOT_PER == 0:
                env.render(returns)

        # End of episode
        state = env.reset()
        done = False

        # print + plot
        print()

    plt.close()


if __name__ == '__main__':
    EPISODES = 100
    PLOT_PER = 1
    main()
