def eight_point_algorithm(indexPairs1, indexPairs2):
    """
    indexPairs1 : Nx3 矩阵
       
    indexPairs2 : Nx3 矩阵
       
    F : 输出基础矩阵
    """

    A = np.vstack([
        indexPairs1[:,0]*indexPairs2[:,0], indexPairs1[:,0]*indexPairs2[:,1], indexPairs1[:,0]*indexPairs2[:,2], 
        indexPairs1[:,1]*indexPairs2[:,0], indexPairs1[:,1]*indexPairs2[:,1], indexPairs1[:,1]*indexPairs2[:,2], 
        indexPairs1[:,2]*indexPairs2[:,0], indexPairs1[:,2]*indexPairs2[:,1], indexPairs1[:,2]*indexPairs2[:,2] ]).T

    # compute linear least square solution
    __, __, VT = np.linalg.svd(A)
    # solution can be obtained from the vector corresponds to the minimum singular value
    F = VT[-1].reshape(3,3).T
        
    # constrain F : making rank 2 by zeroing out last singular value
    U, S, VT = np.linalg.svd(F)
    S[-1] = 0
    F = np.dot(np.dot(U, np.diag(S)), VT)
    
    return F / F[2,2]

def ransac(fit_model, validate_model, X, num_samples, max_iter = -1, thresh = 1.0, ratio_of_inliers = 0.99):
    """
    按照实验原理的伪代码编程ransac
    model —— 适应于数据的模型
    max_iter —— 算法的迭代次数
    t —— 用于决定数据是否适应于模型的阀值
    d —— 判定模型是否适用于数据集的数据数目
    输出：
    best_model ——最匹配的模型参数（如果没有找到好的模型则返回null）
    best_consensus_set —— 估计出模型的数据点
    best_error —— 跟数据相关的估计出的模型错误

    iterations = 0
    best_model = null
    best_consensus_set = null
    best_error = 无穷大
    while ( iterations < k )
    maybe_inliers = 从数据集中随机选择n个点
    maybe_model = 适合于maybe_inliers的模型参数
    consensus_set = maybe_inliers

    for ( 每个数据集中不属于maybe_inliers的点 ）
    if ( 如果点适合于maybe_model，且错误小于t ）
    将点添加到consensus_set
    if （ consensus_set中的元素数目大于d ）
    已经找到了好的模型，现在测试该模型到底有多好
    better_model = 适合于consensus_set中所有点的模型参数
    this_error = better_model究竟如何适合这些点的度量
    if ( this_error < best_error )
    我们发现了比以前好的模型，保存该模型直到更好的模型出现
    best_model =  better_model
    best_consensus_set = consensus_set
    best_error =  this_error
    增加迭代次数
    返回 best_model, best_consensus_set, best_error

    """
    best_model = None
    best_mask = []
    best_ratio = -1.0

    if max_iter == -1:
        max_iter = int(np.log10(1 - ratio_of_inliers) / np.log10(1 - np.power(0.8, 8)) * 10)

    for it in range(max_iter):

        all_indices = np.arange(X.shape[0])
        np.random.shuffle(all_indices)
     
        sample_points = X[all_indices[:num_samples],:]
     
        model = fit_model(sample_points)

        if model is None:
            continue
    
        dist = validate_model(model, X)
        mask = np.zeros(len(X)).astype('uint8') 
        mask[np.abs(dist) <= thresh] = 1

        if np.count_nonzero(mask) / len(X) > best_ratio:
            best_ratio = np.count_nonzero(mask) / len(X)
            best_model = model
            best_mask = mask
     
        # done in case we have enough inliers
        if np.count_nonzero(mask) > len(X) * ratio_of_inliers:
            break

    return best_model is not None, best_model, best_mask
