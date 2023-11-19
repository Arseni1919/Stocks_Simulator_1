import numpy as np

from globals import *

a = np.array([1,2,1])
b = np.array([2,1,2])

result = np.diff(b) / b[:-1]
print(f'{result=}')

# print(np.dot(a, b))
# print(np.multiply(a, b))
print(np.corrcoef(a, b))
correlation, p_value = sp.stats.pearsonr(a, b)
print(correlation)
print(p_value)

