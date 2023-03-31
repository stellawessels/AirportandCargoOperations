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

#Binsizes

bins_sizes = {}
keylistbin = np.arange(0,len(B), 1)
for i in keylistbin:
    bins_sizes.setdefault(i, [])
for i in range(len(B)):
    bins_sizes[i].append(B[i][1][0])
    bins_sizes[i].append(B[i][1][1])
length_R = len(R) -1
keylist = np.arange(0,length_R +1,1)
I_info_solution = {}
for i in keylist:
    I_info_solution.setdefault(i, [])
Items_in_Bin = {}
keylist_bins = np.arange(0, len(B), 1)
for i in keylist_bins:
    Items_in_Bin.setdefault(i, [])

for line, value in enumerate(lines):
    for i in range(length_R+1):
        newvalue = value.split()
        if len(newvalue) != 0:
            if newvalue[0] == 'x_'+ str(i):
                I_info_solution[i].append(float(newvalue[1]))
            if newvalue[0] == 'z_'+ str(i):
                I_info_solution[i].append(float(newvalue[1]))
            if newvalue[0] == 'x_prime_' + str(i):
                I_info_solution[i].append(float(newvalue[1]) - float(I_info_solution[i][0]))
            if newvalue[0] == 'z_prime_' + str(i):
                I_info_solution[i].append(float(newvalue[1]) - float(I_info_solution[i][1]))



for i in range(length_R+1):
    I_info_solution[i].append(R[i][3])
    I_info_solution[i].append(R[i][4])
    I_info_solution[i].append(R[i][5])

for line, value in enumerate(lines):
    for i in range(length_R+1):
        for j in range(len(B)):
            newvalue = value.split()
            if len(newvalue) != 0:
                if newvalue[0] == 'p_('+ str(i) +',' + str(j) + ')':
                    if newvalue[1] == str(1):
                        Items_in_Bin[j].append(i)

bins_used = []

for key in range(len(Items_in_Bin)):
    if len(Items_in_Bin[key]) != 0:
        bins_used.append(key)
