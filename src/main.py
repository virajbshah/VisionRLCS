from game import Environment
import numpy as np

from config import *

env = Environment('human')

observation, info = env.reset()

steps = 2 ** 12

alpha = 0.15
gamma = 0.995
eps = 0.1

try:
    q_table = np.load(r'weights.npy')
except OSError:
    q_table = np.zeros((3,) * SENSOR_COUNT + (2, 3), dtype=np.float64)

observation, info = env.reset()
state = tuple(observation)

for step in range(steps):
    if np.random.uniform(0, 1) < eps:
        action = tuple(env.action_space.sample())
    elif state == (1,) * SENSOR_COUNT:
        action = (0, 0)
    else:
        action = np.unravel_index(np.argmax(q_table[state]), (2, 3))

    prevState = state
    observation, reward, terminated, truncated, info = env.step(action)
    state = tuple(observation)
    
    q_table[prevState + action] = (1 - alpha) * q_table[prevState + action] + \
        alpha * (reward + (gamma * np.max(q_table[state]) if not terminated else 0))

    if terminated or truncated:
        observation, info = env.reset()
        state = tuple(observation)

    print(f'Step {step + 1} / {steps}', end=' ' * 32 + '\r')

env.close()

np.save(r'weights', q_table)
