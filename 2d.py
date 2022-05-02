import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import time
import numpy as np

#file to plot
file = "s-obraz.dev"

#list of values from dev-file
MD = []
X = []
Y = []
Z = []

#parse file to get x,y,z values
with open(file,"r") as f:
	i = 0
	for line in f:
		if i >= 12:
			j = 0
			for v in line.strip().split(' '):
				if v != '':
					if j == 0: MD.append(v)
					if j == 1: X.append(v)
					if j == 2: Y.append(v)
					if j == 3: Z.append(v)
					j += 1
		i += 1

S = []
for i in range(0,len(X)):
	print(str(X[i]) + "\t" + str(Y[i]) + "\t" + str(Z[i]))
	S.append(1)

MD = np.array(MD,dtype=float)
X = np.array(X,dtype=float)
Y = np.array(Y,dtype=float)
Z = np.array(Z,dtype=float)


fig = plt.figure()
plt.subplot(311)
plt.title('X(MD)')
plt.xlabel('Depth')
plt.ylabel('X')
plt.plot(MD,X)
plt.subplot(312)
plt.title('Y(MD)')
plt.xlabel('Depth')
plt.ylabel('Y')
plt.plot(MD,Y)
plt.subplot(313)
plt.title('Z(MD)')
plt.xlabel('Depth')
plt.ylabel('Z')
plt.plot(MD,Z)
plt.subplots_adjust(wspace=0.5, hspace=1.5)
plt.show()