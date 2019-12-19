import numpy as np 
from .orientation_pro import *
from sklearn.neighbors import NearestNeighbors

def match_pro(x,y,iters = 100,threshold = 1e-10):
    #print(x.shape[0],y.shape[0])
    src = np.ones((4,x.shape[1]))
    dsc = np.ones((4,y.shape[1]))
    src[:3,:] = np.copy(x)
    dsc[:3,:] = np.copy(y)
    prev_error = 0
    for i in range(iters):
        dist,indices = NearestNeighbors(n_neighbors=1).fit(dsc[:3,:].T).kneighbors(src[:3,:].T, return_distance=True)
        dist = dist.ravel()
        indices = indices.ravel()
        T = get_transform(src[:3,:].T,dsc[:3,indices].T)
        src = np.dot(T,src)
        error = np.sum(dist)/dist.size
        if abs(prev_error - error) < threshold:
            break
        prev_error = error
    T_final = get_transform(x.T,src[:3,:].T)
    return T_final,dist

def get_transform(src,dsc):
    src_mean = np.mean(src,axis = 0)
    dsc_mean = np.mean(dsc,axis = 0)
    src_0 = src - src_mean
    dsc_0 = dsc - dsc_mean
    temp = np.sum([np.dot(get_left(j).T, get_right(i)) for i, j in zip(src_0,dsc_0)], axis=0)
    values,vectors = np.linalg.eig(temp)
    qu = vectors[:,np.argmax(values)]
    R_matrix = get_rotation(qu)
    t = dsc_mean.T - np.dot(R_matrix,src_mean.T)
    Transform = np.identity(4)
    Transform[:3,:3] = R_matrix
    Transform[:3,3] = t    
    return Transform