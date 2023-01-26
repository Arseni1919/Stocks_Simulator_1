# import gymnasium as gym
# env = gym.make('Ant-v4')
#
# env.render()
import numpy as np

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

from globals import *

l = np.array([0, -1, 1, 1, 0])

out = np.where(l > 0)
for i, j in out:
    print(f'{i=}, {j=}')
print(l[out])