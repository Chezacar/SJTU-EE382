function [right,middle,left] = undistort(right_raw,middle_raw,left_raw,cameraParams)

right = undistortImage(right_raw,cameraParams);
right = rgb2gray(right);
middle = undistortImage(middle_raw,cameraParams);
middle = rgb2gray(middle);
left = undistortImage(left_raw,cameraParams);
left = rgb2gray(left);
end

