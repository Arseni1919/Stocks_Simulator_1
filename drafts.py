import numpy as np

from globals import *

a = np.array([2,2,1])
b = np.array([2,2,1])

# print(np.dot(a, b))
# print(np.multiply(a, b))
print(np.corrcoef(a, b))
correlation, p_value = sp.stats.pearsonr(a, b)
print(correlation)
print(p_value)

