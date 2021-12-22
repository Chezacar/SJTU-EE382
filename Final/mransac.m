function [best_model, best_mask] = mransac(fit_model, validate_model, X, num_samples, max_iter, thresh, ratio_of_inliers)

%     fit_model : callable
%         function that fits the model, with th signature fun(x)->model.
%         The argument x passed to this function is an ndarray of shape (num_samples, m),
%         where num_samples is the number of sampling points per iteration in the RANSAC method,
%         and m is the dimension of the features of each point. This function should explain the
%         meaning of these features itself. It must return the model parameters in only one 
%         object (no matter what type).     
%     validate_model : callable
%         function that computes the errors of the model on all points, with th signature fun(model, x)->error.
%         The argument x passed to this function is an ndarray of shape (n, m), where n is 
%         the number of the whole samples set, and m is the dimension of the features of 
%         each point. This function should explain the meaning of these features itself. 
%         It must return the errors as an ndarray of shape (n, ). 
%     X : ndarray NxM, dtype = float
%         contains a set of observed data points, where N is the number of the whole samples set, 
%         and M is the dimension of the features of each point. This function does not care about 
%         the meaning of M. You should explain it yourself in function 'fit_model' and function 
%         'validate_model'. N must larger than or equal to 8. 
%     num_samples : int
%         the number of sampling points per iteration.
%     max_iter : int
%         maximum number of iterations to perform.
%     thresh : float
%         threshold to distinguish inliers and outliers.
%     ratio_of_inliers : float
%         when the ratio of inliers exceeds this value, the iteration will stop.
%     Return
%     ------
%     retval : boolen
%         whether we find the best model parameters
%     best_model : 
%         model parameters which best fit the data (or None if no good model is found)
%     best_mask : ndarray (N,), dtype = int
%         output array of N elements, every element of which is set to 0 for outliers and to 1 for the other points. 



%max_iter = -1, thresh = 1.0, ratio_of_inliers = 0.99 
% if len(X) < 8:
%         raise ValueError("Number of points must larger than or equal to 8.")
% end
best_model = None;
best_mask = [];
best_ratio = -1.0;

if (max_iter == -1)
    max_iter = int(np.log10(1 - ratio_of_inliers) / np.log10(1 - np.power(0.8, 8)) * 10);
end

%进行RANSAC迭代
for iter = 1:max_iter
    all_indices = 1:size(X,1);
    all_indices = randperm(size(all_indices,1));
    sample_points = X(all_indices(1:num_samples),:);
    model = fit_model(sample_points);
    dist = validate_model(model,X);
    mask = uint8(zeros(size(X,1)));
    
    %计算点云中模型误差
    for j = 1 : size(x,1)
        if abs(dist)<=thresh
            mask(j) = 1;
        end
    end
    
    A = (mask ~= 0);
    n = sum(A(:));
    temp = n / size(X,1);
    if temp > best_ratio
        best_ratio = temp;
        best_model = model;
        best_mask = mask;
    end
    if temp > ratio_of_inliers
        break
    end
end
end

