import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from cluster_test_utils import re_ranking

##
def get_three_dist(agg_fea_toRetrieval, all_aggregated_feature):
    """
    获取三个矩阵形式的距离 distance
    :param query_feature: 待检索图像聚合特征
    :param database_agg_path: 数据库图像聚合特征路径，加载后shape:[m,512], m:数据库图像数量
    :return:
        q_g_dist: 每个 query 图像与 每个 database 图像间的距离
        q_q_dist: 每个 query 图像与 每个 query 图像间的距离
        g_g_dist: 每个 database 图像与 每个 database 图像间的距离
    """
    # query_feature = np.load(query_agg_path) # [n,512]
    query_feature = np.expand_dims(agg_fea_toRetrieval,axis=0) # [1,512]
    # print(query_feature.shape)
    database_feature = all_aggregated_feature # [m,512]
    q_g_dist = np.dot(query_feature,np.transpose(database_feature))
    q_q_dist = np.dot(query_feature,np.transpose(query_feature))
    g_g_dist = np.dot(database_feature,np.transpose(database_feature))
    return q_g_dist, q_q_dist, g_g_dist

##
def feature_cmp(test_image_feature, features_in_data_base, frame_count, frame_list_path, duration):
    """
    为Java端调用的视频检索，返回最接近的那一秒
    :param duration: 视频时长
    :return: 返回最接近的一秒
    """
    q_g_dist, q_q_dist, g_g_dist = get_three_dist(test_image_feature, features_in_data_base)
    frame_list = np.load(frame_list_path)
    k1 = int(len(frame_list) / 2) if len(frame_list) < 45 else 40
    k2 = int(k1 / 2) if frame_count < 40 else 5
    # k-reciprocal Encoding
    final_dist = re_ranking(q_g_dist, q_q_dist, g_g_dist, k1=k1, k2=k2, lambda_value=0.3)
    final_dist = final_dist[0]

    idx = np.argsort(final_dist)
    ## top n similar list
    sorted_name_list = []
    
    for i in idx:
        sorted_name_list.append(frame_list[i])
    index = sorted_name_list[0]
    percent = index / frame_count
    time = percent * duration
    hour = int(time / 3600)
    minute = int((time % 3600) / 60)
    second = int(time % 60)
    metaRes = str(hour) + ":" + str(minute) + ":" + str(second)
    return index, metaRes

if __name__ == '__main__':
    
    frame_list = "E:/CSC3170/ImageDB/videos/frame_list/COD.npy"  
    fea_path = "E:/CSC3170/ImageDB/feature/COD.npy"  
    data = np.load(fea_path) # the retrieved feature from the video (stored in the database, size=115*512）
    features_in_data_base = data

    # There are 115 feature in the database, select one you want to use as test case
    test_image_feature_index = 2
    test_image_feature = data[test_image_feature_index]
    
    # clustering operation on features_in_data_base
    # YOUR CLUSTERING METHOD: TO BE CONTINUE
    
    
    
    index, res = feature_cmp(test_image_feature, features_in_data_base, 1712, 'E:/CSC3170/ImageDB/videos/frame_list/COD.npy', 57)
    print("The index of most matching frame = ", index/15)
    print("Time in video = ", res)
    
 
    
        