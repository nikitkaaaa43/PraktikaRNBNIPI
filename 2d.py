import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import time
import numpy as np

# file to plot
file = "s-obraz.dev"
# depth of visulizing
DEPTH = 50

# list of values from dev-file
MD = []
X = []
Y = []
Z = []

# parse file to get x,y,z values
with open(file, "r") as f:
    i = 0
    for line in f:
        if i >= 12:
            j = 0
            md = 0
            x = 0
            y = 0
            z = 0
            for v in line.strip().split(' '):
                if v != '':
                    if j == 0: MD.append(v)
                    if j == 1: X.append(v)
                    if j == 2: Y.append(v)
                    if j == 3: Z.append(v)
                    j += 1
        i += 1

for i in range(0, len(X)):
    print(str(X[i]) + "\t" + str(Y[i]) + "\t" + str(Z[i]))

MD = np.array(MD, dtype=float)
X = np.array(X, dtype=float)
Y = np.array(Y, dtype=float)
Z = np.array(Z, dtype=float)

plot_md = []
for md in MD:
    if float(md) < DEPTH:
        plot_md.append(md)
plot_x = X[:len(plot_md)]
plot_y = Y[:len(plot_md)]
plot_z = Z[:len(plot_md)]

fig = plt.figure()
plt.subplot(311)
plt.title('X(MD)')
plt.xlabel('Depth')
plt.ylabel('X')
plt.plot(plot_md, plot_x)
plt.subplot(312)
plt.title('Y(MD)')
plt.xlabel('Depth')
plt.ylabel('Y')
plt.plot(plot_md, plot_y)
plt.subplot(313)
plt.title('Z(MD)')
plt.xlabel('Depth')
plt.ylabel('Z')
plt.plot(plot_md, plot_z)
plt.subplots_adjust(wspace=0.5, hspace=1.5)
plt.show()