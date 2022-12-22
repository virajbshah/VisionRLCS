from itertools import product
import numpy as np

weights = np.load(r'weights.npy')

for i in product(range(3), range(3), range(3)):
    print(i)
    print(weights[i])
    print()
    