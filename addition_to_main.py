
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
        MILP.addConstr(x[k], GRB.LESS_EQUAL, x[i] + eta_1[i,k] * L)

for i in R:
    for k in R:
        MILP.addConstr(x[i], GRB.LESS_EQUAL, x[k] + eta_3[i,k] * L)