import pickle
import numpy as np
from gurobipy import *

###Get data from files
with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

with open('G18/G3/R.pickle', 'rb') as handle:
    R = pickle.load(handle)

###Create model
MILP = Model('Mixed Integer Linear Problem')

###Create parameters
""" Parameters that should be called, not in a list
R[i][0] #li
R[i][i] #hi
R[i][2] #l+
B[j][1][0] #Lj
B[j][1][1] #Hj
"""

n = len(R) #number of boxes (25)
m = len(B) #number of containers (4)

#Maximum height and length containers
container_heights = []
container_lengths = []
for container in B:
    container_heights.append(B[container][1][1])
    container_lengths.append(B[container][1][0])

H = max(container_heights)
L = max(container_lengths)

#Create lists with 0 or 1 for perishable, radioactive and fragile
per = np.zeros(len(R))
ra = np.zeros(len(R))
f = np.zeros(len(R))

for item in R:
    if R[item][4] == 1:
        per[item] = 1
    if R[item][5] == 1:
        ra[item] = 1
    if R[item][3] == 1:
        f[item] = 1

#Create lists of sides and axes
a = [1,3]
b = [1,3]
#Create list of all vertices
V = [1,2]

###Creating decision variables

##Decision variables geometric contstraints

#Empty decision variables

p = {}
u = {}
x = {}
z = {}
x_prime = {}
z_prime = {}
r = {}
xp = {}
zp = {}

#Create decision variables

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

for j in range(m):
    u[j] = MILP.addVar(vtype=GRB.BINARY, name="u_%d"%j)

# #TRYING: adding if-statement constraints for the conditional variables
#
# for i in range(n):
#     for k in range(n):
#         if MILP.addConstr(x_prime[k] <= x[i], name="Trial constraint x"):
#             xp[i,k] = 1
#         else:
#             xp[i, k] = 0
#
# for i in range(n):
#     for k in range(n):
#         if MILP.addConstr(z_prime[k] <= z[i], name="Trial constraint z"):
#             zp[i,k] = 1
#         else:
#             zp[i, k] = 0

##Decision variables verticle constraints

#Create empty lists for decision variables
g = {}
h = {}
s = {}
eta_1 = {}
eta_3 = {}
beta = {}
v = {}
m_ik = {}

#Define the for-loops for which the decision variables will be used
A = [i for i in R]
BB = [k for k in R]
C = [j for j in B]
D = [(i, k) for i in R for k in R]
E = [(i, j) for i in R for j in B]
F = [(j, k) for j in B for k in R]
G = [(i, k, ver) for i in R for k in R for ver in V]


#Create decision variables

g = MILP.addVars(A,vtype=GRB.BINARY, lb=0, name="g")
h = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="h")
s = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="s")
eta_1 = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="eta_1")
eta_3 = MILP.addVars(D,vtype=GRB.BINARY, lb=0, name="eta_2")
beta = MILP.addVars(G,vtype=GRB.BINARY, lb=0, name="beta")
v = MILP.addVars(D, vtype=GRB.CONTINUOUS, lb =0, name="v") ##Has a special value that still needs to be added
m_ik = MILP.addVars(D, vtype=GRB.BINARY, lb=0, name='m_ik')

###Create objective function


obj = quicksum(u[j] * B[j][1][3] for j in range(m))

MILP.setObjective(obj, GRB.MINIMIZE)
MILP.update()

###Create constraints

##Geometric constraints


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
            if i != k:
                MILP.addConstr(xp[i,k] + xp[k,i] + zp[i,k] + zp[k,i], GRB.GREATER_EQUAL, (p[i,j] + p[k,j]) - 1, name='Constraint 13')

                MILP.addConstr(x_prime[k], GRB.LESS_EQUAL, x[i] + (1-xp[i,k]) * L, name='Constraint 14')

                MILP.addConstr(x[i] + 1, GRB.LESS_EQUAL, x_prime[k] + xp[i,k] * L, name='Constraint 15')

                MILP.addConstr(z_prime[k], GRB.LESS_EQUAL, z[i] + (1 - zp[i, k]) * H, name='Constraint 18')


    MILP.addConstr(r[i,3,1], GRB.LESS_EQUAL, R[i][2], name='Constraint 19')

    MILP.addConstr(r[i, 3, 3], GRB.LESS_EQUAL, 1, name='Constraint 21')



##Vertical constraints


#Constraint 26


for i in R:
    MILP.addConstr(quicksum(quicksum(beta[i,k,ver] for k in R) for ver in V), GRB.GREATER_EQUAL, 2*(1-g[i]), name='C26')

#Constraint 27

for i in R:
    MILP.addConstr(z[i], GRB.LESS_EQUAL, (1-g[i])*H, name='C27')

#Constraint 28

for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(z_prime[k] - z[i], GRB.LESS_EQUAL, v[i,k], name='C28')

#Constraint 29

for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(z[i] - z_prime[k], GRB.LESS_EQUAL, v[i,k], name='C29')

#Constraint 30

for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(v[i,k], GRB.LESS_EQUAL, z_prime[k] - z[i] + 2*H*(1 - m_ik[i,k]), name='C30')

#Constraint 31

for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(v[i,k], GRB.LESS_EQUAL, z[i] - z_prime[k] + 2*H*m_ik[i,k], name='C31')

#Constraint 32


for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(h[i,k], GRB.LESS_EQUAL, v[i,k], name ="C32")

#Constraint 33


for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(v[i,k], GRB.LESS_EQUAL, h[i,k]*H, name="C33")

#Constraint 36


for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(p[i,j]-p[k,j], GRB.LESS_EQUAL, 1 - s[i,k], name="C35")

#Constraint 37


for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(p[k,j]-p[i,j], GRB.LESS_EQUAL, 1 - s[i,k], name="C36")


# Constraint 39 & 41 (edited)

for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(eta_1[i,k], GRB.LESS_EQUAL, 1-beta[i,k,1]) # dit gaat fout denk

for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(eta_3[i,k], GRB.LESS_EQUAL, 1-beta[i,k,2]) # dit gaat fout denk

# Constraints 43 & 45
for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(x[k], GRB.LESS_EQUAL, x[i] + eta_1[i,k] * L, name='C43')

for i in R:
    for k in R:
        if i != k:
            MILP.addConstr(x[i], GRB.LESS_EQUAL, x[k] + eta_3[i,k] * L, name='C45')

#Constraint 51
    for k in R:
        MILP.addConstr(quicksum(s[i,k] for i in R), GRB.LESS_EQUAL, n*91-f[k], name='C51')

#Constraint perishable and radioactive
    for i in R:
        for k in R:
            for j in B:
                if i != k:
                    MILP.addConstr(ra[i]*per[k], GRB.LESS_EQUAL, 2 - p[i,j] - p[k,j], name='CPR')

###Solve the MILP

MILP.update()
MILP.write('P4RMP_LP.lp')

MILP.optimize()

#Write solution file

MILP.write('P4RMPSolution.sol')