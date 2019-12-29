import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image as im
from numpy import linalg as la
raw_pic = im.open('target.jpg')
raw_pic_array = np.array(raw_pic)
#print(raw_pic_array.shape)
pic = cv2.resize(raw_pic_array,(800,600),interpolation = cv2.INTER_CUBIC)

#选取四个点的坐标分别为(76，112),(624,191),(68,567),(642,466)

#下面先用其次法来解决这个问题
#构造A矩阵
x1 = [76,122]
x2 = [624,191]
x3 = [68,567]
x4 = [642,466]
t1 = [50,50]
t2 = [750,50]
t3 = [50,550]
t4 = [750,550]
A = np.array([[x1[0],x1[1],1,0,0,0,-x1[0] * t1[0],-x1[1] * t1[0],-t1[0]],
     [0,0,0,x1[0],x1[1],1,-x1[0] * t1[1],-x1[1] * t1[1],-t1[1]],
     [x2[0],x2[1],1,0,0,0,-x2[0] * t2[0],-x2[1] * t2[0],-t2[0]],
     [0,0,0,x2[0],x2[1],1,-x2[0] * t2[1],-x2[1] * t2[1],-t2[1]],
     [x3[0],x3[1],1,0,0,0,-x3[0] * t3[0],-x3[1] * t3[0],-t3[0]],
     [0,0,0,x3[0],x3[1],1,-x3[0] * t3[1],-x3[1] * t3[1],-t3[1]],
     [x4[0],x4[1],1,0,0,0,-x4[0] * t4[0],-x4[1] * t4[0],-t4[0]],
     [0,0,0,x4[0],x4[1],1,-x4[0] * t4[1],-x4[1] * t4[1],-t4[1]]])
print(A)
U,sigma,Vt = la.svd(A)
print(sigma)

#sigma_min = np.min(sigma)
#min_index = np.where(sigma == sigma_min)[0]
#print(sigma_min,min_index)
vector_h = Vt.T[:,-1]
#print(vector_h)
H1 = vector_h.reshape(3,3)
#lambad = 1 / H1[2,2]
H1 = H1 / H1[2,2]
result1 = cv2.warpPerspective(pic, H1, (pic.shape[1],pic.shape[0]))
result1 = im.fromarray(result1)
result1.save('result1.jpg')

# 下面是非齐次解法
A2 = [[x1[0],x1[1],1,0,0,0,-x1[0] * t1[0],-x1[1] * t1[0]],
      [0,0,0,x1[0],x1[1],1,-x1[0] * t1[1],-x1[1] * t1[1]],
      [x2[0],x2[1],1,0,0,0,-x2[0] * t2[0],-x2[1] * t2[0]],
      [0,0,0,x2[0],x2[1],1,-x2[0] * t2[1],-x2[1] * t2[1]],
      [x3[0],x3[1],1,0,0,0,-x3[0] * t3[0],-x3[1] * t3[0]],
      [0,0,0,x3[0],x3[1],1,-x3[0] * t3[1],-x3[1] * t3[1]],
      [x4[0],x4[1],1,0,0,0,-x4[0] * t4[0],-x4[1] * t4[0]],
      [0,0,0,x4[0],x4[1],1,-x4[0] * t4[1],-x4[1] * t4[1]]]
A2 = np.array(A2)
B2 = np.array([t1,t2,t3,t4])
B2 = B2.reshape(8,1)
H2_vector = np.dot(la.inv(A2),B2) 
H2 = np.reshape(np.append(H2_vector,1),(3,3))
result2 = cv2.warpPerspective(pic, H2, (pic.shape[1],pic.shape[0]))
result2 = im.fromarray(result2)
result2.save('result2.jpg')
