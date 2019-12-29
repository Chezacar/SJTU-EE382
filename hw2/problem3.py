import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import time
from mpl_toolkits.mplot3d import Axes3D
data = pd.read_table("camera_poses.txt",sep=' ',header=None)
data = np.array(data)
print(data[0][1])
(size_x,size_y) = data.shape
print(size_x,size_y)
R_matrix = np.zeros((size_x,3,3))
for i in range(0,size_x,1):
    R_matrix[i,0,:] = data[i,0:3]
    R_matrix[i,1,:] = data[i,3:6]
    R_matrix[i,2,:] = data[i,6:9]
T_vector = np.zeros((3,size_x))
for j in range(0,size_x,1):
    T_vector[:,j] = data[j,9:12]

x_vector = np.zeros((3,size_x))
for k in range(0,size_x,1):
    x_vector[:,k] = np.dot(-R_matrix[k,:,:],T_vector[:,k])
print(x_vector.shape)



fig = plt.figure()
for l in range(size_x):
    plt.ion()
    ax = fig.gca(projection='3d')
    point = x_vector[:,l]
    direction = R_matrix[l]
    ax.quiver(point[0], point[1], point[2], direction[0], direction[1], direction[2],color=['r','g','b'], length=10)
    ax.scatter(x_vector[0], x_vector[1], x_vector[2],c='y') #绘点
    plt.pause(0.1)
    plt.clf()
