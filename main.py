import pickle
import numpy as np
from gurobipy import *

with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

with open('G18/G3/R.pickle', 'rb') as handle:
    R = pickle.load(handle)

m = Model("Cargo")

print(B)
print(R)

n = len(R)
m = len(B)



g = {}
h = {}
s = {}
eta_1 = {}
eta_3 = {}
beta = {}

A = [i for i in R]
B = [k for k in R]
C = [j for j in B]
D = [(i,k) for i in R for k in R]
E = [(i,j) for i in R for j in B]
F = [(j,k) for j in B for k in R]
G = [(i,k,l) for i in R for k in R for l in V]

#Create model

m = Model('Cargo')

#Decision variables


g = m.addVars(A,vtype=GRB.BINARY, lb=0, name="g")
h = m.addVars(D,vtype=GRB.BINARY, lb=0, name="h")
s = m.addVars(D,vtype=GRB.BINARY, lb=0, name="s")
eta_1 = m.addVars(D,vtype=GRB.BINARY, lb=0, name="eta_1")
eta_2 = m.addVars(D,vtype=GRB.BINARY, lb=0, name="eta_2")
beta = m.addVars(G,vtype=GRB.BINARY, lb=0, name="beta")



