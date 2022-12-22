from game import Environment
import numpy as np

from config import *

env = Environment('human')

observation, info = env.reset()

steps = 2 ** 10

q_table = np.load(r'weights.npy')

observation, info = env.reset()
state = tuple(observation)

for step in range(steps):
    if state == (1,) * SENSOR_COUNT:
        action = (0, 0)
    else:
        action = np.unravel_index(np.argmax(q_table[state]), (2, 3))

    observation, reward, terminated, truncated, info = env.step(action)
    state = tuple(observation)
    
    if terminated or truncated:
        observation, info = env.reset()
        state = tuple(observation)

    # print(*state, end=' ' * 32 + '\r')

env.close()
