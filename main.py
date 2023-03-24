import pickle
import numpy as np
from gurobipy import *

with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

with open('G18/G3/R.pickle', 'rb') as handle:
    R = pickle.load(handle)

print(B)
print(R)


n = len(R)  #25
m = len(B)  #4

a = [1,3]
b = [1,3]

container_heights = []
container_lengths = []
for container in B:
    container_heights.append(B[container][1][1])
    container_lengths.append(B[container][1][0])

H = max(container_heights)
L = max(container_lengths)

""" Parameters
B[j][1][0] #Lj
B[j][1][1] #Hj
B[j][1][3] # Cost
"""

# R[i][0] = length
# R[i][1] = height
# R[i][2] = lplus

MILP = Model('Mixed Integer Linear Problem')

p = {}
u = {}
x = {}
z = {}
x_prime = {}
z_prime = {}
r = {}
xp = {}
zp = {}

for i in range(n):
    x[i] = MILP.addVar(vtype=GRB.CONTINUOUS, name="x_%d"%i)
    z[i] = MILP.addVar(vtype=GRB.CONTINUOUS, name="z_%d"%i)
    x_prime[i] = MILP.addVar(vtype=GRB.CONTINUOUS, name="x_prime_%d"%i)
    z_prime[i] = MILP.addVar(vtype=GRB.CONTINUOUS, name="z_prime_%d"%i)
    for j in range(m):
        p[i,j] = MILP.addVar(vtype=GRB.BINARY, name="p_(%d,%d)"%(i,j))
    for aa, value_a in enumerate(a):
        for bb, value_b in enumerate(b):
            r[i, value_a, value_b] = MILP.addVar(vtype=GRB.BINARY, name="r_(%d,%d,%d)"%(i, value_a, value_b))

    for k in range(n):
        xp[i,k] = MILP.addVar(vtype=GRB.BINARY, name="xp_(%d,%d)"%(i,k))
        zp[i,k] = MILP.addVar(vtype=GRB.BINARY, name="zp_(%d,%d)"%(i,k))

for i in range(n):
    for k in range(n):
        if MILP.addConstr(x_prime[k] <= x[i], name="Trial constraint x"):
            xp[i,k] = 1
        else:
            xp[i, k] = 0

for i in range(n):
    for k in range(n):
        if MILP.addConstr(z_prime[k] <= z[i], name="Trial constraint z"):
            zp[i,k] = 1
        else:
            zp[i, k] = 0


for j in range(m):
    u[j] = MILP.addVar(vtype=GRB.BINARY, name="u_%d"%j)

obj = quicksum(u[j] * B[j][1][3] for j in range(m))

MILP.setObjective(obj, GRB.MINIMIZE)
MILP.update()

for j in range(m):
    MILP.addConstr(quicksum(p[i,j] for i in range(n)), GRB.LESS_EQUAL, n * u[j])

for i in range(n):
    MILP.addConstr(quicksum(p[i,j] for j in range(m)), GRB.EQUAL, 1, name='Constraint 4')

    MILP.addConstr(x_prime[i], GRB.LESS_EQUAL, quicksum(B[j][1][0] * p[i,j] for j in range(m)), name='Constraint 5')

    MILP.addConstr(z_prime[i], GRB.LESS_EQUAL, quicksum(B[j][1][1] * p[i, j] for j in range(m)), name='Constraint 7')

    MILP.addConstr(x_prime[i] - x[i], GRB.EQUAL, r[i,1,1] * R[i][0] + r[i,1,3] * R[i][1], name='Constraint 8')
    MILP.addConstr(z_prime[i] - z[i], GRB.EQUAL, r[i,3,1] * R[i][0] + r[i,3,3] * R[i][1], name='Constraint 10')

    for bb, value_b in enumerate(b):
        MILP.addConstr(quicksum(r[i,value_a,value_b] for aa, value_a in enumerate(a)), GRB.EQUAL, 1, name='Constraint 11')

    for aa, value_a in enumerate(a):
        MILP.addConstr(quicksum(r[i,value_a,value_b] for bb, value_b in enumerate(b)), GRB.EQUAL, 1, name='Constraint 12')

    for j in range(m):
        for k in range(n):
            MILP.addConstr(xp[i,k] + xp[k,i] + zp[i,k] + zp[k,i], GRB.GREATER_EQUAL, (p[i,j] + p[k,j]) - 1, name='Constraint 13')

            MILP.addConstr(x_prime[k], GRB.LESS_EQUAL, x[i] + (1-xp[i,k]) * L, name='Constraint 14')

            MILP.addConstr(x[i] + 1, GRB.LESS_EQUAL, x_prime[k] + xp[i,k] * L, name='Constraint 15')

            MILP.addConstr(z_prime[k], GRB.LESS_EQUAL, z[i] + (1 - zp[i, k]) * H, name='Constraint 18')


    MILP.addConstr(r[i,3,1], GRB.LESS_EQUAL, R[i][2], name='Constraint 19')

    MILP.addConstr(r[i, 3, 3], GRB.LESS_EQUAL, 1, name='Constraint 21')


MILP.update()
MILP.write('P4RMP_LP.lp')

MILP.optimize()

MILP.write('P4RMPSolution.sol')