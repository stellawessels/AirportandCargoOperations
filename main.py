import pickle
import numpy as np
from gurobipy import *

with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

with open('G18/G3/R.pickle', 'rb') as handle:
    R = pickle.load(handle)

#create model
MILP = Model('Mixed Integer Linear Problem')



#Vertices and other parameters
V = [1,2]

""" Parameters
R[i][0] #li
R[i][i] #hi
B[j][1][0] #Lj
B[j][1][1] #Hj
"""

n = len(R)
m = len(B)


#L and H
container_heights = []
container_lengths = []
for container in B:
    container_heights.append(B[container][1][1])
    container_lengths.append(B[container][1][0])

H = max(container_heights)
L = max(container_lengths)

#decision variables geometric
p = {}
u = {}
x = {}
z = {}
x_prime = {}
z_prime = {}
r = {}
xp = {}
zp = {}

a = [1,3]
b = [1,3]

for i in range(n):
    x[i] = MILP.addVar(vtype=GRB.CONTINUOUS)
    z[i] = MILP.addVar(vtype=GRB.CONTINUOUS)
    x_prime[i] = MILP.addVar(vtype=GRB.CONTINUOUS)
    z_prime[i] = MILP.addVar(vtype=GRB.CONTINUOUS)
    for j in range(m):
        p[i, j] = MILP.addVar(vtype=GRB.BINARY)
        u[j] = MILP.addVar(vtype=GRB.BINARY)
    for aa, value_a in enumerate(a):
        for bb, value_b in enumerate(b):
            r[i, value_a, value_b] = MILP.addVar(vtype=GRB.BINARY)

    for k in range(n):
        xp[i, k] = MILP.addVar(vtype=GRB.BINARY)
        zp[i, k] = MILP.addVar(vtype=GRB.BINARY)

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


#Decision variables


g = MILP.addVars(A,vtype=GRB.BINARY, lb=0, name="g")
h = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="h")
s = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="s")
eta_1 = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="eta_1")
eta_2 = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="eta_2")
beta = MILP.addVars(G,vtype=GRB.BINARY, lb=0, name="beta")

#Add mik
#def m_ik(z_prime,z):




#Constraints

#Constraint 26

for i in R:
    MILP.addConstr(quicksum(quicksum(beta[l][i][k] for k in R) for l in V), GRB.GREATER_EQUAL, 2*(1-g[i]), name='C26')

#Constraint 27

for i in R:
    MILP.addConstr(z[i], GRB.LESS_EQUAL, (1-g[i])*H, name='C27')

#Constraint 28

for i in R:
    for k in R:
        MILP.addConstr(z_prime[k] - z[i], GRB.LESS_EQUAL, abs(z_prime[k] - z[i]), name='C28')

#Constraint 29

for i in R:
    for k in R:
        MILP.addConstr(z[i] - z_prime[k], GRB.LESS_EQUAL, abs(z_prime[k] - z[i]), name='C29')

#Constraint 30

for i in R:
    for k in R:
        MILP.addConstr(abs(z_prime[k] - z[i]), GRB.LESS_EQUAL, z_prime[k] - z[i] + 2*H(1 - m[i][k]), name='C30')

#Constraint 31

for i in R:
    for k in R:
        MILP.addConstr(abs(z_prime[k] - z[i]), GRB.LESS_EQUAL, z[i] - z_prime[k] + 2*H*m[i][k], name='C31')

#Constraint 32


for i in R:
    for k in R:
        MILP.addConstr(h[d], GRB.LESS_EQUAL, abs(z_prime[k]-z[i]), name ="C32")

#Constraint 33


for i in R:
    for k in R:
        MILP.addConstr(abs(z_prime[k]-z[i]), GRB.LESS_EQUAL, h*H, name="C33")

#Constraint 36


for i in R:
    for k in R:
        MILP.addConstr(p[i]-p[k], GRB.LESS_EQUAL, 1 - s, name="C35")

#Constraint 37


for i in R:
    for k in R:
        MILP.addConstr(p[k]-p[i], GRB.LESS_EQUAL, 1 - s, name="C36")


# Constraint 39 & 41 (edited)
for i in R:
    for k in R:
        MILP.addConstr(eta_1[i,k], GRB.LESS_EQUAL, 1-beta[i,k,0]) # dit gaat fout denk

for i in R:
    for k in R:
        MILP.addConstr(eta_3[i,k], GRB.LESS_EQUAL, 1-beta[i,k,1]) # dit gaat fout denk

# Constraints 43 & 45
for i in R:
    for k in R:
        MILP.addConstr(x[k], GRB.LESS_EQUAL, x[i] + eta_1[i,k] * L, name='C43')

for i in R:
    for k in R:
        MILP.addConstr(x[i], GRB.LESS_EQUAL, x[k] + eta_3[i,k] * L, name='C45')

#Constraint 51
    for k in R:
        MILP.addConstr(quicksum(s[i][k] for i in R), GRB.LESS_EQUAL, n*91-f[k], name='C51')

#Constraint perishable and radioactive
    for i in R:
        for k in R:
            for j in B:
                MILP.addConstr(ra[i]*per[k], GRB.LESS_EQUAL, 2 - p[i][j] - p[k][j], name='CPR')