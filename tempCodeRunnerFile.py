from  mpl_toolkits.mplot3d import*
import numpy as np
import matplotlib.pyplot as plt
import os


X = []
Y = []
Z = []

if not os.getcwd() == './Res':
    os.chdir('./Res')

with open('ploted.txt') as f:
    for line in f:
        x1, y1, z1= line.split()
        X.append(int(x1))
        Y.append(int(y1))
        Z.append(int(z1))
r=40
cube=np.zeros((r,r,r))

for i in range(len(X)):
    X[i]=X[i]+int(r/2)
    Y[i]=Y[i]+int(r/2)
    Z[i]=Z[i]+int(r/2)
    cube[X[i]][Y[i]][Z[i]]=1
    

fig = plt.figure()
ax = fig.add_subplot(projection='3d')   
ax.grid(False)
plt.axis('off')
ax.voxels(cube,facecolors='grey', edgecolor="black")
plt.show()

