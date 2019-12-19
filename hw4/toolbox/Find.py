import numpy as np 
from orientation_pro import *
from sklearn.neighbors import NearestNeighbors

def match_pro(x,y,iters,threshold):
    src = np.ones(x.shape[0],4)
    dsc = np.ones（y.shape[0],4)
    src[:3,:] = np.copy(x.T)
    src[:3,:] = np.copy(y.T)
    prev_error = 0
    for i in range(iters):
        dist,indices = NearestNeighbors(n_neighbors=1).fit(y).kneighbors(x, return_distance=True)
        dist = dist.ravel()
        indices = indices.ravel()
        T = get_transform(x,dsc[:3,indices].T)
        src = np.dot(T,src)
        error = np.sum(dist)/dist.size
        if abs(prev_erroc-error) < threshold:
            break
        prev_error = error
    T_final = get_transform(x,)
    return T_final,dist

def get_transform(src,dsc):
    src_mean = np.mean(src,axis = 0)
    dst_mean = np.mean(dsc,axis = 0)
    src_0 = src - src_mean
    dst_0 = dsc - dst_mean
    R_matrix = get_rotation(src_0,dst_0)
    t = src_0 - np.dot(R_matrix,src_mean)
    Transform = np.identity(4)
    T[:3,:3] = R
    T[:3,3] = t    
    return T