import numpy as np
from numpy import linalg as la
x_raw = np.loadtxt('rot_x.txt')
x_raw = x_raw - np.mean(x_raw,axis=0)
y_raw = np.loadtxt('rot_y.txt')
y_raw = y_raw - np.mean(y_raw,axis=0)

def q_process(x):
    size = x.shape[0]
    temp = np.zeros((size,1))
    X = np.hstack((temp,x))
    return X

def left_q(y):
    temp_y = [[y[0],-y[1],-y[2],-y[3]],[y[1],y[0],-y[3],y[2]],[y[2],y[3],y[0],-y[1]],[y[3],-y[2],y[1],y[0]]]
    return temp_y

def right_q(x):
    temp_x = [[x[0],-x[1],-x[2],-x[3]],[x[1],x[0],x[3],-x[2]],[x[2],-x[3],x[0],x[1]],[x[3],x[2],-x[1],x[0]]]
    return temp_x

def get_A(x,y):
    A = np.zeros((4,4))
    size_x = x.shape[0]
    for i in range(size_x):
        temp_y = left_q(y[i])
        temp_x = right_q(x[i])
        A += np.matmul(temp_y,temp_x)
    return A

#SLAM十四讲qR转换公式
def q2r(q):
    R = [[1-2*q[2]*q[2]-2*q[3]*q[3],2*q[1]*q[2]+2*q[0]*q[3],2*q[1]*q[3]-2*q[0]*q[2]],
         [2*q[1]*q[2]-2*q[0]*q[3],1-2*q[1]*q[1]-2*q[3]*q[3],2*q[1]*q[3]+2*q[0]*q[2]],
         [2*q[1]*q[3]+2*q[0]*q[2],2*q[2]*q[3]-2*q[0]*q[1],1-2*q[1]*q[1]-2*q[2]*q[2]]]
    return R
x_q = q_process(x_raw)
y_q = q_process(y_raw)
A = get_A(x_q,y_q)
#A = -1 * A
print(A)
A_vals,A_vecs = la.eig(A)
index = np.argmax(A_vals)
q = A_vecs[:,index]
R = q2r(q)
print(q,R)