import matplotlib.pyplot as plt

import pickle


with open('G18/G3/B.pickle', 'rb') as handle:
    B = pickle.load(handle)

b1 = (91, 50, 1, 0, 0, 0)

fig = plt.figure()
axs = {
    "axs1": fig.add_axes([0.1, 0.6, 0.6, 0.2], xticklabels = []),
    "axs2": fig.add_axes([0.1, 0.1, 0.6, 0.2], xticklabels = []),
    "axs3": fig.add_axes([0.6, 0.1, 0.6, 0.2], xticklabels = []),
    "axs4": fig.add_axes([0.6, 0.6, 0.6, 0.2], xticklabels = [])
}
plt.show()