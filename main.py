import numpy as np
import math
import os
from scipy import io
import matplotlib.pyplot as plt
from toolbox import *

def load_data(datapath = 'hw4/icp_xy.mat'):
    data = io.loadmat('datapath')
    x,y = data['x'].T,data['y'].T
    return x,y

def main(datapath):
    x,y = load_data
    Transform,distance = match_pro(x,y)
    error = np.sum(dist) / dist.size
    print('Transformation Matrix is {}'.format(T))
    print('MSE error is {}'.format(error))
    src = np.ones((4,x.shape[0]))
    src[:3,:] = np.copy(x)
    data_transoform = np.dot(T,src)[:3,]
    show(x,y,data_transoform)

if __name__ == '__main__':
    datapath = 'hw4/icp_xy.mat'
    main(datapath)
    