import pandas as pd
import numpy as np
import pickle

###Get data from files
with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

with open('G18/G3/R.pickle', 'rb') as handle:
    R = pickle.load(handle)

with open("P4RMPSolution.sol") as f:
    content = f.read()
# with open('G18/G3/R.pickle', 'rb') as handle:
#     R = pickle.load(handle)

lines = content.split('\n')

length_R = 24
keylist = np.arange(0,length_R +1,1)
answers = {}
for i in keylist:
    answers.setdefault(i, [])
for line, value in enumerate(lines):
    for i in range(length_R+1):
        newvalue = value.split()
        if len(newvalue) != 0:
            if newvalue[0] == 'x_'+ str(i):
                answers[i].append(float(newvalue[1]))
            if newvalue[0] == 'z_'+ str(i):
                answers[i].append(float(newvalue[1]))
            if newvalue[0] == 'x_prime_' + str(i):
                answers[i].append(float(newvalue[1]) - float(answers[i][0]))
            if newvalue[0] == 'z_prime_' + str(i):
                answers[i].append(float(newvalue[1]) - float(answers[i][1]))



for i in range(length_R+1):
    answers[i].append(R[i][3])
    answers[i].append(R[i][4])
    answers[i].append(R[i][5])
