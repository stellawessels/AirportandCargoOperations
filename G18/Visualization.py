import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

#13 in onze data is twee van de drie bijzondere aspecten!!

bins_sizes = {0: [300, 155],
1: [300,155]}

bins_used = [0,1]

#which boxes in which bin
Items_in_Bin = {0: [0, 2, 8, 9, 13, 15, 16, 17, 18, 19, 20, 21, 22, 24], 1: [1, 3, 4, 5, 6, 7, 10, 11, 12, 14, 23], 2: [], 3: [], 4: []}

#each item i, [horizontal coordinate x_i, vertical coordinate z_1, horizontal extension, vertical extension]

I_info_solution = {0: [0.0, 36.000000000000014, 59.0, 29.0, 1, 0, 0], 1: [227.0, 5.0, 50.0, 91.0, 0, 0, 0], 2: [65.0, 0.0, 117.0, 35.0, 0, 0, 0], 3: [277.0, 0.0, 23.0, 70.0, 0, 1, 0], 4: [180.0, 0.0, 37.0, 96.0, 1, 0, 0], 5: [0.0, 41.0, 86.0, 56.0, 0, 0, 0], 6: [0.0, 97.0, 35.0, 58.0, 0, 0, 0], 7: [0.0, 0.0, 71.0, 41.0, 0, 0, 0], 8: [83.0, 65.0, 61.0, 90.0, 0, 0, 0], 9: [182.0, 37.000000000000014, 109.0, 28.0, 1, 0, 0], 10: [45.0, 125.0, 98.0, 30.0, 0, 0, 0], 11: [71.0, 0.0, 109.0, 40.0, 0, 0, 0], 12: [86.0, 40.0, 55.0, 76.0, 0, 0, 0], 13: [230.0, 69.0, 70.0, 46.0, 1, 0, 1], 14: [229.0, 96.0, 66.0, 59.0, 0, 0, 0], 15: [231.0, 115.0, 69.0, 39.0, 0, 0, 0], 16: [64.0, 36.0, 117.0, 28.0, 0, 0, 1], 17: [147.0, 64.0, 28.0, 49.0, 0, 0, 0], 18: [182.0, 0.0, 74.0, 25.0, 0, 0, 0], 19: [145.0, 128.0, 86.0, 27.0, 1, 0, 0], 20: [0.0, 0.0, 65.0, 33.0, 0, 0, 0], 21: [0.0, 97.0, 57.0, 57.0, 0, 0, 0], 22: [7.0, 70.0, 58.0, 26.0, 0, 0, 0], 23: [143.0, 96.0, 86.0, 41.0, 0, 0, 0], 24: [175.0, 65.0, 55.0, 31.0, 1, 0, 0]}

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

