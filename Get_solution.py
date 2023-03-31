import pandas as pd
import numpy as np
with open("P4RMPSolution.sol") as f:
    content = f.read()
# with open('G18/G3/R.pickle', 'rb') as handle:
#     R = pickle.load(handle)

R = 24
lines = content.split('\n')


keylist = np.arange(0,R+1,1)
answers = {}
for i in keylist:
    answers[i] = None
for line, value in enumerate(lines):
    for i in range(R+1):
        newvalue = value.split()
        if len(newvalue) != 0:
            if newvalue[0] == 'x_'+ str(i):
                answers[i].append(newvalue[1])
            if newvalue[0] == 'z_'+ str(i):
                answers[i].append(newvalue[1])
print(answers)


