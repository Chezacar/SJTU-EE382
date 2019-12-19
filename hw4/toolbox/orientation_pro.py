import numpy as np 
import math 


def get_rotation(qu):
	q = np.array(qu, dtype=np.float64, copy=True)
	n = np.dot(q, q)
	q *= math.sqrt(2.0 / n)
	q = np.outer(q, q)
	return np.array([
	    [1.0-q[2, 2]-q[3, 3],     q[1, 2]-q[3, 0],     q[1, 3]+q[2, 0]],
	    [    q[1, 2]+q[3, 0], 1.0-q[1, 1]-q[3, 3],     q[2, 3]-q[1, 0]],
	    [    q[1, 3]-q[2, 0],     q[2, 3]+q[1, 0], 1.0-q[1, 1]-q[2, 2]]])


def get_left(qu):
	if qu.size == 3:
		return np.array([
			[   0, -qu[0], -qu[1], -qu[2]], 
			[qu[0],     0, -qu[2],  qu[1]], 
			[qu[1],  qu[2],     0, -qu[0]], 
			[qu[2], -qu[1],  qu[0],    0]])
	elif qu.size == 4:
		return np.array([
			[qu[0], -qu[1], -qu[2], -qu[3]], 
			[qu[1],  qu[0], -qu[3],  qu[2]], 
			[qu[2],  qu[3],  qu[0], -qu[1]], 
			[qu[3], -qu[2],  qu[1],  qu[0]]])
	else:
		return np.identity(4)

def get_right(qu):
	if qu.size == 3:
		return np.array([
			[   0, -qu[0], -qu[1], -qu[2]], 
			[qu[0],     0,  qu[2], -qu[1]], 
			[qu[1], -qu[2],     0,  qu[0]], 
			[qu[2],  qu[1], -qu[0],    0]])
	elif qu.size == 4:
		return np.array([
			[qu[0], -qu[1], -qu[2], -qu[3]], 
			[qu[1],  qu[0],  qu[3], -qu[2]], 
			[qu[2], -qu[3],  qu[0],  qu[1]], 
			[qu[3],  qu[2], -qu[1],  qu[0]]])
	else:
		return np.identity(4)
