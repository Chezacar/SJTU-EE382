clear all; %#ok<CLALL>
clc
close all
load('cameraParams.mat');

right_raw = imread('4右.jpg');
middle_raw = imread('4中.jpg');
left_raw = imread('4左.jpg');

right = undistortImage(right_raw,cameraParams);
%right = right_raw;
right_rgb = right;
right = rgb2gray(right);
middle = undistortImage(middle_raw,cameraParams);
%middle = middle_raw;
middle_rgb = middle;
middle = rgb2gray(middle);
left = undistortImage(left_raw,cameraParams);
%left = left_raw;
left_rgb = left;
left = rgb2gray(left);

%[right,middle,left] = undistort(right_raw,middle_raw,left_raw,cameraParams);

points_right = detectMinEigenFeatures(right);
points_middle = detectSURFFeatures(middle);
points_left = detectSURFFeatures(left);

subplot(1,3,1)
imshow(right); hold on;
plot(points_right.selectStrongest(100));

subplot(1,3,2)
imshow(middle); hold on;
plot(points_middle.selectStrongest(100));

subplot(1,3,3)
imshow(left); hold on;
plot(points_left.selectStrongest(100));

% 提取特征点
[features_right, vpts_right] = extractFeatures(right, points_right);
[features_middle, vpts_middle] = extractFeatures(middle, points_middle);
[features_left,vpts_left] = extractFeatures(left,points_left);

% 特征点匹配
indexPairs = matchFeatures(features_middle, features_right,'MaxRatio',0.7,'Unique',true);

matchedPoints_right = vpts_right(indexPairs(:,2));
matchedPoints_middle = vpts_middle(indexPairs(:,1));

figure; showMatchedFeatures(middle,right,matchedPoints_middle,matchedPoints_right);
legend('right','middle');

[E, epipolarInliers] = estimateFundamentalMatrix(matchedPoints_middle, matchedPoints_right,'method','RANSAC','NumTrials',3000,'DistanceThreshold',1e-4);
% 寻找 epipolar inliers
inlierPoints2 = matchedPoints_right(epipolarInliers, :);
inlierPoints1 = matchedPoints_middle(epipolarInliers, :);

% 显示匹配结果
figure
showMatchedFeatures(middle, right, inlierPoints1, inlierPoints2);
legend('middle','right');
title('Epipolar Inliers');

[E, epipolarInliers] = estimateFundamentalMatrix(inlierPoints1, inlierPoints2,'method','RANSAC','NumTrials',3000,'DistanceThreshold',1e-4);
% 相机位姿
[orientation, location] = relativeCameraPose(E, cameraParams, inlierPoints1, inlierPoints2);

[rotationMatrix_middle,translationVector_middle] = cameraPoseToExtrinsics(eye(3),[0 0 0]);

[rotationMatrix_right,translationVector_right] = cameraPoseToExtrinsics(orientation,location);

camMatrix_middle = cameraMatrix(cameraParams,eye(3),[0 0 0]);
camMatrix_right = cameraMatrix(cameraParams,rotationMatrix_right,translationVector_right);

points3D = triangulate(matchedPoints_middle, matchedPoints_right, camMatrix_middle, camMatrix_right);

%%%step8将两张图中的一张与第三张进行特征匹配
%提取特征点,并且特征匹配
indexPairs2= matchFeatures(features_middle, features_left, 'MaxRatio', 0.7, 'Unique', true);
matchedPointsMiddle_ML = vpts_middle(indexPairs2(:,1));
matchedPointsLeft_ML = vpts_left(indexPairs2(:,2));

%找到两次匹配相同的在第一张图上的点
[asd,indexMddle_MR,indexMiddle_ML] = intersect(indexPairs(:,1),indexPairs2(:,1));
ptCloud_left = points3D(indexMddle_MR,:);
pixelPoint_left = matchedPointsLeft_ML(indexMiddle_ML,:).Location;

% %估计相机位置
[Ori_ml, Loc_ml] = estimateWorldCameraPose(pixelPoint_left,ptCloud_left,cameraParams);
[rotationMatrix_left, translationVector_left] = cameraPoseToExtrinsics(Ori_ml, Loc_ml);
Cam3 = cameraMatrix(cameraParams,rotationMatrix_left,translationVector_left);
figure;
showMatchedFeatures(middle, left, matchedPoints_middle(indexMddle_MR,:), pixelPoint_left,'montage','PlotOptions',{'ro','go','y--'});
title('middle and left');

% 重建点云的颜色选择
numPixels = size(middle_rgb, 1) * size(middle_rgb, 2);
allColors = reshape(middle_rgb, [numPixels, 3]);
colorIdx = sub2ind([size(middle_rgb, 1), size(middle_rgb, 2)], round(matchedPoints_middle.Location(:,2)), ...
    round(matchedPoints_middle.Location(:, 1)));
color = allColors(colorIdx, :);

% Create the point cloud
ptCloud = pointCloud(points3D, 'Color', color);

% Visualize the camera locations and orientations
cameraSize = 0.3;
figure
plotCamera('Size', cameraSize, 'Color', 'r', 'Label', '1', 'Opacity', 0);
hold on
grid on
plotCamera('Location', location, 'Orientation', orientation, 'Size', cameraSize, ...
    'Color', 'b', 'Label', '2', 'Opacity', 0);
plotCamera('Location', Loc_ml, 'Orientation', Ori_ml, 'Size', cameraSize, ...
    'Color', 'g', 'Label', '3', 'Opacity', 0);


% Visualize the point cloud
pcshow(ptCloud, 'VerticalAxis', 'y', 'VerticalAxisDir', 'down', ...
    'MarkerSize', 45);

% Rotate and zoom the plot
camorbit(0, -30);
camzoom(1.5);

% Label the axes
xlabel('x-axis');
ylabel('y-axis');
zlabel('z-axis')

title('Up to Scale Reconstruction of the Scene');




%%% bundle adjustment的结果
temps = viewSet;
temps = addView(temps, 1,'Points',vpts_middle,'Orientation',rotationMatrix_middle,'Location',translationVector_middle);
temps = addView(temps, 2,'Points',vpts_right,'Orientation',rotationMatrix_right,'Location',translationVector_right);
temps = addConnection(temps,1,2,'Matches',indexPairs);
temps = addView(temps, 3,'Points',vpts_left,'Orientation',rotationMatrix_left,'Location',translationVector_left);
temps = addConnection(temps,1,3,'Matches',indexPairs2);

tracks = findTracks(temps);
cameraPoses = poses(temps);

% numPixels = size(middle_rgb, 1) * size(middle_rgb, 2);
% allColors = reshape(middle_rgb, [numPixels, 3]);
% colorIdx = sub2ind([size(middle_rgb, 1), size(middle_rgb, 2)], round(matchedPoints_middle.Location(:,2)), ...
%     round(matchedPoints_middle.Location(:, 1)));
% color = allColors(colorIdx, :);
[xyzPoints,errors] = triangulateMultiview(tracks,cameraPoses,cameraParams);

[xyzRefinedPoints,refinedPoses] = bundleAdjustment(xyzPoints,tracks,cameraPoses,cameraParams);
figure
pcshow(xyzRefinedPoints,'VerticalAxis','y','VerticalAxisDir',...
    'down','MarkerSize',45);
hold on
plotCamera(cameraPoses, 'Size', 0.1)
hold off