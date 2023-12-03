import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from utils import image_border_imgArr
from image_retrieve_utils import re_ranking

from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
from selectFiltersAndAggregation import select_filters1, PWA, useImgPathGet1DFeatureNoSaved
from measureAndEvaluation1 import re_ranking
import VGG16Singleton
from tqdm import tqdm

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

class Service:
    def __init__(self):
        self.status = "stopped"
        self.model = VGG16Singleton.VGG16Singleton.instance()

    def get_feature_from_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) # 获取帧数
        frame_rate = cap.get(cv2.CAP_PROP_FPS) # 获取帧速
        # print("帧速：", frame_rate)
        duration = frame_count / frame_rate
        frame_list = []
        num_per_sec = 2
        step = int(frame_rate/num_per_sec) # 一秒钟只要两张，step=frame_count/2
        # print("帧数 =", int(frame_count), ". We will extract", num_per_sec, "frames per second, or ", int(frame_count/step), "images in total.")
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

            # extract feature
            img = image_border_imgArr(frame, resize=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            features = self.model.predict(x)  # 提取特征
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
        return all_aggregated_feature
    
    def get_feature_from_img(self, img):

        # extract feature
        img = image_border_imgArr(img, resize=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = self.model.predict(x)  # 提取特征
        # print(features.shape) # [1,7,7,512] # 特征的shape（h，w，c）
        features = features[0]  # [7,7,512]
        # print(features.shape)
        
        # 过滤器的排序集合
        sorted_filter_list = select_filters1(features)
        # 对当前的feature[h,w,c]进行聚合
        test_image_feature = aggregate_feature_during_videoRetrieval(features, sorted_filter_list)

        return test_image_feature
    
    def feature_cmp(self, test_image_feature, features_in_data_base, frame_count, duration):
        """
        为Java端调用的视频检索，返回最接近的那一秒
        :param duration: 视频时长
        :return: 返回最接近的一秒
        """
        q_g_dist, q_q_dist, g_g_dist = get_three_dist(test_image_feature, features_in_data_base)
        frame_interval = 15
        frame_number_storage = int(frame_count/frame_interval)+1
        frame_list = [frame_interval*i for i in range(frame_number_storage)]
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
    video_path = "E:/CSC3170/ImageDB/videos/COD.mp4"
    extract_feature_path = "E:/CSC3170/ImageDB/feature/"
    extract_img_path = "E:/CSC3170/ImageDB/images/"
    uniqueName = "COD"
    
    img_path = "E:/CSC3170/cbir/COD_frame_1395.jpg"
    fea_path = "E:/CSC3170/ImageDB/feature/COD.npy"

    
    video_file_name = video_path.split("/")[-1]
    video_name = video_file_name.split(".")[0]
    # 初始化视频文件
    
    # 使用示例
    service = Service()
    
    # func1: video得到特征向量
    res = service.get_feature_from_video(video_path)

    # func2: 从图片提取特征
    img = cv2.imread(img_path)
    test_image_feature = service.get_feature_from_img(img)
    
    features_in_data_base = np.load(fea_path) # the retrieved feature from the video (stored in the database, size=115*512）

    # func3: 特征匹配
    frame_count, duration = 1712, 57
    index, res = service.feature_cmp(test_image_feature, features_in_data_base, frame_count, duration)
    print("Frame = ", index, "The index of most matching frame = ", index/15)
    print("Time in video = ", res)