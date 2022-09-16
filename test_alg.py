from globals import *


def test_alg(env, alg, episodes=100, plot_per=1, random_seed=True, seed=123):

    state = env.reset()
    done = False

    for episode in range(episodes):
        counter = 0
        total_return = 0
        returns = []
        while not done:
            counter += 1
            # action = env.sample_action()
            action = alg.choose_action(state)
            next_state, reward, done = env.step(action)

            # stats
            total_return += reward
            returns.append(total_return)

            # Learning
            alg.learning_step(state, action, next_state, reward, done)

            # prep for next state
            state = next_state

            # print + plot
            print(f'\r[ep. {episode}, step {counter}] return: {total_return}, state: {state}', end='')
            if counter % plot_per == 0:
                env.render(returns, alg)

        # End of episode
        state = env.reset()
        done = False

        # print + plot
        print()

    plt.close()


def main():
    pass
    # test_alg()


if __name__ == '__main__':
    main()


