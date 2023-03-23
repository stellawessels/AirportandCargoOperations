import pickle
import numpy as np

with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

with open('G18/G3/R.pickle', 'rb') as handle:
    R = pickle.load(handle)

print(B)
print(R)

n = len(R)
m = len(B)
print(n)


""" Parameters
R[i][0] #li
R[i][i] #hi
B[j][1][0] #Lj
B[j][1][1] #Hj
"""




