#该代码为取点工具，摘自csdn博主，老师您可以不用看，就是用来获得点的坐标
import cv2
import numpy as np
img = cv2.imread('/Users/chezacar/Desktop/AmurTiger/python-ECO-HC-master/results/Tiger_26/0.jpg')
#img = cv2.resize(img,(800,600),interpolation = cv2.INTER_CUBIC)
a =[]
b = []
def on_EVENT_LBUTTONDOWN(event, x, y,flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)

cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)
print(a[0],b[0])

img[b[0]:b[1],a[0]:a[1],:] = 0   #注意是 行，列（y轴的，X轴）
cv2.imshow("image", img)
cv2.waitKey(0)
print (a,b)
#print('\033[1;35;0m\a,\b \033[0m')
