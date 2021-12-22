## 代码说明

### MATLAB代码

代码使用MATLAB编写，在MATLABR2019b版本中多次测试过可以一键直接运行。运行后会依次弹出六个窗口，分别是

1、提取的SURF特征

2、初步匹配结果

3、RANSAC后匹配结果（重叠）

4、RANSAC后匹配结果（平行）

5、3D重建后结果

6、Bundle Adjustment优化后结果

### Python代码

python代码是根据算法内容仅使用numpy实现的RANSAC函数和8-Points函数，由于我对python比较熟练所以使用python进行编写。但是最后没找到综合进MATLAB主程序的好办法，但算法流程应当是正确的，遂附在整个报告文件中供参考

## 文件说明

4左中右三张图片是测试用图片，标定棋盘是标定用的棋盘，

cameraParams.mat是相机标定结果

拍摄照片的设备是iPhone 7Plus，使用的是主摄广角镜头，f/1.8大光圈

1200万像素未压缩 分辨率4032 × 3024