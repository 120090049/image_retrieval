import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from utils import image_border_imgArr
from tensorflow.keras.applications.vgg16 import preprocess_input
from featureExtract_VGG16 import extract_VGG16_feature_noSaved
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
from selectFiltersAndAggregation import select_filters1, PWA, useImgPathGet1DFeatureNoSaved
from measureAndEvaluation1 import re_ranking
import VGG16Singleton
from tqdm import tqdm
import time

##
def aggregate_feature_during_videoRetrieval(T, sorted_filters_list):
    """
    对刚提取的特征进行聚合
    :param T: [h,w,c]三维特征
    :return: 返回聚合后的一维特征
    """
    feature = T  # [7,7,512]
    each_aggregated_feature = PWA(sorted_filters_list, feature, filters_num=100)  # [512]
    # 归一化的修改
    each_aggregated_feature = each_aggregated_feature / np.linalg.norm(each_aggregated_feature)
    return each_aggregated_feature

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
def videoRetrievalForRetrieval(model, imgPath, videoFeaturePath, frame_count, frame_list_path, duration):
    """
    为Java端调用的视频检索，返回最接近的那一秒
    :param model: 使用的模型，VGG16
    :param imgPath: 要检索的图片路径
    :param videoFeaturePath: 视频的特征保存路径
    :param duration: 视频时长
    :return: 返回最接近的一秒
    """
    imgFeature2D = useImgPathGet1DFeatureNoSaved(imgPath, model)
    aggre_fea = np.load(videoFeaturePath)
    q_g_dist, q_q_dist, g_g_dist = get_three_dist(imgFeature2D, aggre_fea)
    frame_list = np.load(frame_list_path)
    k1 = int(len(frame_list) / 2) if len(frame_list) < 45 else 40
    k2 = int(k1 / 2) if frame_count < 40 else 5
    final_dist = re_ranking(q_g_dist, q_q_dist, g_g_dist, k1=k1, k2=k2, lambda_value=0.3)
    final_dist = final_dist[0]

    idx = np.argsort(final_dist)
    sorted_name_list = []
    
    ## top n similar list
    
    for i in idx:
        sorted_name_list.append(frame_list[i])
    index = sorted_name_list[0]
    percent = index / frame_count
    time = percent * duration
    hour = int(time / 3600)
    minute = int((time % 3600) / 60)
    second = int(time % 60)
    metaRes = str(hour) + ":" + str(minute) + ":" + str(second)
    return metaRes

##
def uploadedVideoExtractAggregateFeature(model, videoPath, extract_feature_path, extract_img_path=None):
    """
    针对上传的视频与特征提取与保存
    :param model: VGG16
    :param videoPath: 视频的地址
    :param extract_feature_path: 特征保存的地址
    :param if there are extract_img_path, save extracted image (not necessary)
    :return: success
    """
    video_file_name = videoPath.split("/")[-1]
    video_name = video_file_name.split(".")[0]
    
    # 初始化视频文件
    cap = cv2.VideoCapture(videoPath)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) # 获取帧数
    frame_rate = cap.get(cv2.CAP_PROP_FPS) # 获取帧速
    print("帧速：", frame_rate)
    duration = frame_count / frame_rate
    frame_list = []
    num_per_sec = 2
    step = int(frame_rate/num_per_sec) # 一秒钟只要两张，step=frame_count/2
    print("帧数 =", int(frame_count), ". We will extract", num_per_sec, "frames per second, or ", int(frame_count/step), "images in total.")
    current_frame_index = 0

    pbar = tqdm(total=frame_count)
    all_aggregated_feature = []
    while current_frame_index < frame_count:
        # 设置当前帧位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index)
        # 读取帧
        ret, frame = cap.read()
        if not ret:
            break
        frame_list.append(current_frame_index)
        
        # if save image directory is not none, save image
        if extract_img_path is not None:
            filename = extract_img_path + '/' + video_name + f'_frame_{current_frame_index}.jpg'
            cv2.imwrite(filename, frame)

        # extract feature
        img = image_border_imgArr(frame, resize=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)  # 提取特征
        # print(features.shape) # [1,7,7,512] # 特征的shape（h，w，c）
        features = features[0]  # [7,7,512]
        # print(features.shape)
        
        # 过滤器的排序集合
        sorted_filter_list = select_filters1(features)
        # 对当前的feature[h,w,c]进行聚合
        aggregate_gea_temp = aggregate_feature_during_videoRetrieval(features, sorted_filter_list)
        if len(all_aggregated_feature) == 0:
            all_aggregated_feature = aggregate_gea_temp
        else:
            all_aggregated_feature = np.vstack((all_aggregated_feature, aggregate_gea_temp))
        
        # 更新帧索引
        current_frame_index += step
        pbar.update(step)
    
    # 释放视频对象
    cap.release()
    
    # 保存frame_list
    frame_list_path = os.path.dirname(videoPath) + '/frame_list/' + video_name + ".npy"
    # 检查目标文件夹是否存在，如果不存在则创建
    dir_name = os.path.dirname(frame_list_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # 现在可以安全地保存文件
    np.save(frame_list_path, frame_list)
    extract_feature_path = extract_feature_path + video_name + ".npy"
    np.save(extract_feature_path, all_aggregated_feature)
    return ["success", frame_count, frame_list_path, duration]

##
def getTime(list, frame_count, howLong):
    res = []
    for index in list:
        percent = index / frame_count
        time = percent * howLong
        hour = int(time / 3600)
        minute = int((time % 3600) / 60)
        second = int(time % 60)
        metaRes = str(hour) + ":" + str(minute) + ":" + str(second)
        res.append(metaRes)
    return res

if __name__ == '__main__':
    model = VGG16Singleton.VGG16Singleton.instance()
    video_path = "E:/CSC3170/ImageDB/videos/COD.mp4"
    extract_feature_path = "E:/CSC3170/ImageDB/feature/"
    extract_img_path = "E:/CSC3170/ImageDB/images/"
    uniqueName = "COD"
    
    img_path = "E:/CSC3170/cbir/COD_frame_1395.jpg"
    fea_path = "E:/CSC3170/ImageDB/feature/COD.npy"

    if 0:
        res = uploadedVideoExtractAggregateFeature(model, video_path, extract_feature_path, extract_img_path)
        print(res)

    else:
        res = ['success', 1712.0, 'E:/CSC3170/ImageDB/videos/frame_list/COD.npy', 57.06666666666667]
        
        start_time = time.time()  # 开始时间
        
        res = videoRetrievalForRetrieval(model, img_path, fea_path, res[1], res[2], res[3])
        print(res)
        
        end_time = time.time()  # 结束时间
        elapsed_time = end_time - start_time  # 运行时间
        print(f"运行时间：{elapsed_time} 秒")
    
    # fea_path = "E:/CSC3170/ImageDB/feature/COD.npy"
    # data = np.load(fea_path)
    # print(data.shape)
        