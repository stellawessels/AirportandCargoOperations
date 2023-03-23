import pickle
import numpy as np
from gurobipy import *

with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

with open('G18/G3/R.pickle', 'rb') as handle:
    R = pickle.load(handle)

#Vertices
V = [1,2]
print(B)
print(R)

n = len(R)
m = len(B)



""" Parameters
R[i][0] #li
R[i][i] #hi
B[j][1][0] #Lj
B[j][1][1] #Hj
"""

#Create model

m = Model('Cargo')

#Decision variables


A = [i for i in R]
B = [k for k in R]
C = [j for j in B]
D = [(i,k) for i in R for k in R]
E = [(i,j) for i in R for j in B]
F = [(j,k) for j in B for k in R]
G = [(i,k,l) for i in R for k in R for l in V]




