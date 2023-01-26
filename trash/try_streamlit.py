import streamlit as st
import pandas as pd
from globals import *
from env_stocks_generator import StocksGeneratorEnv
# from alg_sarsa import SarsaAlg


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
            alg.learning_step(state, action, next_state, reward, done, total_return)

            # prep for next state
            state = next_state

            # print + plot
            print(f'\r[ep. {episode}, step {counter}] return: {total_return}, state: {state}', end='')
            if counter % plot_per == 0:
                fig = env.render(returns, alg)
                with placeholder.container():
                    st.pyplot(fig)

        # End of episode
        state = env.reset()
        done = False
        alg.stats_reset()

        # print + plot
        print()

    plt.close()


def main():

    st.write("# NT Dashboard")
    st.write(pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    }))

    env = StocksGeneratorEnv()
    # sarsa_alg = SarsaAlg(env=env)
    # test_alg(env=env, alg=sarsa_alg, episodes=100, plot_per=10, random_seed=random_seed, seed=seed)


if __name__ == '__main__':
    # random_seed = True
    random_seed = False
    seed = 123

    if not random_seed:
        torch.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)

    # st
    st.set_page_config(
        page_title="NT Dashboard",
        page_icon="✅",
        layout="wide",
    )
    placeholder = st.empty()

    main()
