import numpy as np
import math
import os
from scipy import io
import matplotlib.pyplot as plt
from toolbox import Find
from toolbox import show
from toolbox import orientation_pro

def load_data(datapath = 'icp_xy.mat'):
    data = io.loadmat(datapath)
    x,y = data['x'],data['y']
    return x,y

def main(datapath):
    x,y = load_data(datapath)
    Transform,distance = Find.match_pro(x,y)
    error = np.sum(distance) / distance.size
    print('Transformation Matrix is {}'.format(Transform))
    print('MSE error is {}'.format(error))
    src = np.ones((4,x.shape[1]))
    src[:3,:] = np.copy(x)
    data_transoform = np.dot(Transform,src)[:3,]
    show.show(x,y,data_transoform)

if __name__ == '__main__':
    datapath = 'icp_xy.mat'
    main(datapath)
    