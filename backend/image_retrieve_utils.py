import numpy as np

def k_reciprocal_neigh(initial_rank, x, k1):
    forward_k_neigh_index = initial_rank[x,:k1+1] #第i个图片的前20个相似图片的索引号
    # print(len(forward_k_neigh_index))
    backward_k_neigh_index = initial_rank[forward_k_neigh_index,:k1+1]
    # print(len(backward_k_neigh_index))
    fi = np.where(backward_k_neigh_index==x)[0] #返回backward_k_neigh_index中等于i的图片的行索引号
    return forward_k_neigh_index[fi]  #返回与第i张图片 互相为k_reciprocal_neigh的图片索引号

def re_ranking(q_g_dist, q_q_dist, g_g_dist, k1=20, k2=6, lambda_value=0.7):
    original_dist = np.concatenate([np.concatenate([q_q_dist,q_g_dist],axis=1),
                                    np.concatenate([q_g_dist.T,g_g_dist], axis=1)],
                                   axis=0)
    # print(original_dist.shape) # [4304,4304]
    original_dist = 2. - 2 * original_dist  # np.power(original_dist, 2).astype(np.float32) 余弦距离转欧式距离
    original_dist = np.transpose(1. * original_dist / np.max(original_dist, axis=0))  # 归一化
    V = np.zeros_like(original_dist).astype(np.float32)
    # initial_rank = np.argsort(original_dist).astype(np.int32)
    # top K1+1
    initial_rank = np.argpartition(original_dist, range(1, k1 + 1))  # 取前20，返回索引号
    # 二
    query_num = q_g_dist.shape[0]
    all_num = original_dist.shape[0]
    for a in range(all_num):
        # k-reciprocal neighbors
        k_reciprocal_index = k_reciprocal_neigh(initial_rank, a, k1)  # 取出互相是前20的
        k_reciprocal_expansion_index = k_reciprocal_index
        for j in range(len(k_reciprocal_index)):  # 遍历与第i张图片互相是前20的每张图片
            candidate = k_reciprocal_index[j]
            candidate_k_reciprocal_index = k_reciprocal_neigh(initial_rank, candidate, int(np.around(k1 / 2)))
            if len(np.intersect1d(candidate_k_reciprocal_index, k_reciprocal_index)) > 2. / 3 * len(candidate_k_reciprocal_index):
                k_reciprocal_expansion_index = np.append(k_reciprocal_expansion_index, candidate_k_reciprocal_index)
        # 增广k_reciprocal_neigh数据，形成k_reciprocal_expansion_index
        k_reciprocal_expansion_index = np.unique(k_reciprocal_expansion_index)  # 避免重复，并从小到大排序
        weight = np.exp(-original_dist[a, k_reciprocal_expansion_index])  # 第i张图片与其前20+图片的权重
        V[a, k_reciprocal_expansion_index] = 1. * weight / np.sum(weight)  # V记录第i个对其前20+个近邻的权重，其中有0有非0，非0表示没权重的，就似乎非前20+的
    original_dist = original_dist[:query_num, ]  # original_dist裁剪到 只有query x query+g

    if k2 != 1:
        V_qe = np.zeros_like(V, dtype=np.float32)
        for b in range(all_num):  # 遍历所有图片
            V_qe[b, :] = np.mean(V[initial_rank[b, :k2], :], axis=0)  # 第i张图片在initial_rank前k2的序号的权重平均值
            # 第i张图的initial_rank前k2的图片对应全部图的权重平均值
            # 若V_qe中(i,j)=0，则表明i的前k2个相似图都与j不相似
        V = V_qe
        del V_qe
    del initial_rank
    # 三
    invIndex = []
    for c in range(all_num):
        invIndex.append(np.where(V[:, c] != 0)[0])

    jaccard_dist = np.zeros_like(original_dist, dtype=np.float32)

    for d in range(query_num):
        temp_min = np.zeros(shape=[1, all_num], dtype=np.float32)
        indNonZero = np.where(V[d, :] != 0)[0]
        # indImages = []
        indImages = [invIndex[ind] for ind in indNonZero]
        for j in range(len(indNonZero)):
            temp_min[0, indImages[j]] = temp_min[0, indImages[j]] + np.minimum(V[d, indNonZero[j]],V[indImages[j], indNonZero[j]])
        jaccard_dist[d] = 1 - temp_min / (2. - temp_min)

    final_dist = jaccard_dist * (1 - lambda_value) + original_dist * lambda_value
    del original_dist
    del V
    del jaccard_dist
    final_dist = final_dist[:query_num, query_num:]
    # print(final_dist.shape)
    return final_dist # [422,3882] (i,j)表示query的第i张图片与database的第j张图片的final_dist
