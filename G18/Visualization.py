import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

#13 in onze data is twee van de drie bijzondere aspecten!!

bins_sizes = {0: [200,150],
1: [200,150],
2: [180,120]}

bins_used = [0,1,2]

#which boxes in which bin
Items_in_Bin = {0: [1, 3, 5, 9, 10, 11, 14],
1: [6, 8, 13, 15, 16, 17, 18, 19],
2: [0, 2, 4, 7, 12]}

#each item i, [horizontal coordinate x_i, vertical coordinate z_1, horizontal extension, vertical extension]

I_info_solution = {0: [120.0, 0.0, 50, 25,0,0,0],
1: [153.00000000000006, 0.0, 45, 51,1,0,1],
2: [33.00000000000006, 27.0, 36, 29,1,0,0],
3: [33.99999999999997, 25.0, 35, 47,0,0,1],
4: [15.999999999999972, 0.0, 55, 27,0,0,0],
5: [70.99999999999997, 59.0, 40, 25,1,0,0],
6: [98.00000000000006, 0.0, 55, 23,0,0,0],
7: [70.99999999999997, 59.0, 31, 47,0,0,0],
8: [101.00000000000006, 23.0, 52, 24,0,0,0],
9: [33.99999999999997, 0.0, 37, 25,0,0,0],
10: [33.99999999999997, 72.0, 28, 41,0,0,0],
11: [6.999999999999972, 0.0, 27, 50,0,0,0],
12: [70.99999999999997, 0.0, 42, 59,0,0,0],
13: [69.00000000000006, 38.0, 29, 31,0,0,0],
14: [70.99999999999997, 0.0, 40, 59,0,0,0],
15: [27.000000000000057, 38.0, 42, 59,0,0,0],
16: [53.00000000000006, 0.0, 45, 38,0,0,0],
17: [0.0, 0.0, 34, 38,0,0,0],
18: [34.00000000000003, 97.0, 35, 43,1,0,0],
19: [170.0, 0.0, 30, 46,0,1,0]}

#define Matplotlib figure and axis
fig, axs = plt.subplots(nrows=1, ncols=len(bins_used), figsize=(10, 5))
cr = 0
# create simple line plot and add rectangle to plot
for i, bin_num in enumerate(bins_used):
    axs[i].set_ylim([0, bins_sizes[bin_num][1]])
    axs[i].set_xlim([0, bins_sizes[bin_num][0]])

    for y, valuey in enumerate(bins_used):
        if valuey != bin_num:
            continue
        for x, valuex in enumerate(Items_in_Bin[valuey]):
            facecolor = ''
            if I_info_solution[valuex][4] == 1:
                facecolor = 'blue'
            elif I_info_solution[valuex][5] == 1:
                facecolor = 'green'
            elif I_info_solution[valuex][6] == 1:
                facecolor = 'red'
            else:
                facecolor = 'gray'
                #facecolor = colorsrandom[cr]
                #cr+=1
            axs[i].add_patch(
                Rectangle((I_info_solution[valuex][0], I_info_solution[valuex][1]), I_info_solution[valuex][2],
                          I_info_solution[valuex][3],edgecolor = 'black', facecolor=facecolor, fill=True, lw=1))

plt.show()

