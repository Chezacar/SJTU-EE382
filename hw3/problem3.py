import numpy as np
from numpy import linalg as la

def update_q(p, q):
    result = np.ones(4).astype(np.float64)
    result[0] = p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3]
    result[1] = p[0]*q[1] + p[1]*q[0] + p[2]*q[3] - p[3]*q[2]
    result[2] = p[0]*q[2] - p[1]*q[3] + p[2]*q[0] + p[3]*q[1]
    result[3] = p[0]*q[3] + p[1]*q[2] - p[2]*q[1] + p[3]*q[0]
    return result

def q2r(q):
    R = [[1-2*q[2]*q[2]-2*q[3]*q[3],2*q[1]*q[2]+2*q[0]*q[3],2*q[1]*q[3]-2*q[0]*q[2]],
         [2*q[1]*q[2]-2*q[0]*q[3],1-2*q[1]*q[1]-2*q[3]*q[3],2*q[1]*q[3]+2*q[0]*q[2]],
         [2*q[1]*q[3]+2*q[0]*q[2],2*q[2]*q[3]-2*q[0]*q[1],1-2*q[1]*q[1]-2*q[2]*q[2]]]
    return R

def left_q(y):
    temp_y = [[y[0],-y[1],-y[2],-y[3]],[y[1],y[0],-y[3],y[2]],[y[2],y[3],y[0],-y[1]],[y[3],-y[2],y[1],y[0]]]
    return temp_y

def right_q(x):
    temp_x = [[x[0],-x[1],-x[2],-x[3]],[x[1],x[0],x[3],-x[2]],[x[2],-x[3],x[0],x[1]],[x[3],x[2],-x[1],x[0]]]
    return temp_x

def Antiangle(x):
    A = [[0, -x[2], x[1]],
         [x[2], 0, -x[0]],
         [-x[1], x[0], 0]]
    return A

def dtheta(X, Y, R):
    J = np.zeros((3*X.shape[0],3))
    Z = np.zeros(3*X.shape[0])
    for i in range(X.shape[0]):
        J_tmp = np.matmul(R, X[i].T)
        dJ = Antiangle(J_tmp)
        dZ = Y[i] - np.matmul(R, X[i].T)
        J[3*i:3*i+3,:] = dJ
        Z[3*i:3*i+3] = dZ
    J = np.array(J).reshape(-1,3)
    Z = np.array(Z).reshape(-1,1)
    dTheta = np.matmul(np.matmul(la.inv(np.matmul(J.T, J)), J.T), Z)
    return dTheta

def test(X, Y,R=None):
    new_Y = np.matmul(R, X.T)
    difference = la.norm(Y.T- new_Y)
    print('The difference is: {}'.format(difference))
    return difference

def Gauss_Newton_Quaternion(X,Y,iters = 10,num = 5):
    record = np.zeros(2)
    r_record = np.zeros((3,3))
    record[0] = 10000
    rand = np.random.rand(3)
    q = np.array([1,rand[0],rand[1],rand[2]])
    for k in range(iters):
        R = q2r(q)
        delta_theta = dtheta(X,Y,R)
        exp = np.reshape([1, delta_theta[0, 0]/2, delta_theta[1, 0]/2, delta_theta[2, 0]/2],[4,1])
        q = update_q(exp, q)
        diff = test(X,Y,R)
        if record[0] > diff:
            record[0] = diff
            record[1] = k
            r_record = q
        if k - record[1] > num:
            q = r_record
            break
    print(R,record[0],record[1])

def Gauss_Newton_R_matrix(X,Y,iters = 10,num = 5):
    record = np.zeros(2)
    r_record = np.zeros((3,3))
    record[0] = 10000
    R = np.random.rand(3,3)
    u, sigma, v = la.svd(R)
    R = np.matmul(np.matmul(u, np.identity(3)), v.T)
    for k in range(iters):
        dTheta = dtheta(X,Y,R)
        # tmp = t.exp()
        # R = R*tmp
        tmp = Antiangle(dTheta)
        exp = np.identity(3) + tmp
        exp = exp.astype(int)
        R = np.matmul(R,exp)
        u, sigma, v = la.svd(R)
        R = np.matmul(np.matmul(u, np.identity(3)), v.T)
        diff = test(X,Y,R)
        if record[0] > diff:
            record[0] = diff
            record[1] = k
            r_record = R
        if k - record[1] > num:
            R = r_record
            break
    print(R,record[0],record[1])

if __name__ == '__main__':
    x_raw = np.loadtxt('rot_x.txt')
    x_raw = x_raw - np.mean(x_raw,axis=0)
    y_raw = np.loadtxt('rot_y.txt')
    y_raw = y_raw - np.mean(y_raw,axis=0)
    print('基于旋转矩阵')
    Gauss_Newton_R_matrix(x_raw,y_raw,iters = 3000,num = 300)#基于旋转矩阵
    print('四元数')
    Gauss_Newton_Quaternion(x_raw,y_raw,iters = 3000,num = 300)#基于四元数
