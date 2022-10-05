import gymnasium as gym
env = gym.make('Ant-v4')

env.render()

# observation, info = env.reset(seed=42)
#
# for i in range(1000):
#     action = env.action_space.sample()
#     observation, reward, terminated, truncated, info = env.step(action)
#
#     if terminated or truncated:
#         observation, info = env.reset()
#
#     env.render()
#     print(i)
#
# env.close()