import os
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.preprocessing import normalize as sknormalize
from networkFeatureExtract.featureExtract_VGG16 import extract_VGG16_feature_noSaved, VGG16, preprocess_input, image
from utils import image_border

def useImgPathGet1DFeatureNoSaved(imgPath, model):
    """
    给你一张图片的路径，提取该图片并且聚合成1D的特征，不保存，但会特征
    :param imgPath: 图片路径
    :param model: 使用的提取模型
    :return: 返回1D特征
    """
    img = image_border(imgPath, resize=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)  # 提取特征
    # print(features.shape) # [1,7,7,512] # 特征的shape（h，w，c）
    features = features[0]  # [7,7,512]
    ordered_filter_list = select_filters1(features)
    # 使用排序好的过滤器进行特征聚合 [512]
    feature = PWA(ordered_filter_list, features, a=2, b=2, filters_num=100, sum_weighted=1)
    return feature / np.linalg.norm(feature)  # 单位化

def select_filters(feature_path):
    """
    选择每一个图像feature_map的方差大的filters
    :param feature_path: ======特征的路径========
    :return: 方差从大到小的序号
    """
    feature_map = np.load(feature_path) #[7,7,512]
    # print(feature_map.shape)
    average = (feature_map.sum(0)).sum(0) / (feature_map.shape[0] * feature_map.shape[1]) # [512]
    # print(average.shape)
    variance = feature_map - average # [7,7,512]
    # print(variance.shape)
    variance = (variance*variance)**0.5
    variance = (variance.sum(0)).sum(0) # [512]
    # print(variance.shape)
    dic_variance = dict(zip(range(variance.shape[0]),variance))
    dic_variance_sorted = sorted(dic_variance.items(),key=lambda d:d[1],reverse=True)
    select_number = []
    for tuple1 in dic_variance_sorted:
        select_number.append(tuple1[0])
    # print(len(select_number)) #512
    return select_number

def select_filters1(T):
    """
    选择每一个图像feature_map的方差大的filters
    :param T: ======提取的特征=======
    :return: 方差从大到小的序号
    """
    feature_map = T #[7,7,512]
    # print(feature_map.shape)
    average = (feature_map.sum(0)).sum(0) / (feature_map.shape[0] * feature_map.shape[1]) # [512]
    # print(average.shape)
    variance = feature_map - average # [7,7,512]
    # print(variance.shape)
    variance = (variance*variance)**0.5
    variance = (variance.sum(0)).sum(0) # [512]
    # print(variance.shape)
    dic_variance = dict(zip(range(variance.shape[0]),variance))
    dic_variance_sorted = sorted(dic_variance.items(),key=lambda d:d[1],reverse=True)
    select_number = []
    for tuple1 in dic_variance_sorted:
        select_number.append(tuple1[0])
    # print(len(select_number)) #512
    return select_number

def L2_normalize(x,copy=False):
    if type(x) == np.ndarray and len(x.shape) == 1:
        return np.squeeze(sknormalize(x.reshape(1,-1),copy=copy))
    else:
        return sknormalize(x,copy=copy)

def PWA(select_list,X,a=2,b=2,filters_num=25,sum_weighted=1):
    """
    将每张图片的feature_map乘以权重并聚合到一起
    :param select_list: filters排序后的序号列表
    :param X: 每张图片的feature_map
    :param a: 2
    :param b: 2
    :param filters_num: 要使用几个filters
    :param sum_weighted: 1:表示加权求和，0或其他值:表示求平均值
    :return: 拼接好后的特征向量
    """
    select_num_map = select_list[0:filters_num]
    # print("select_num_map前25个:", select_num_map)
    X = np.array(X)
    if X.shape[0] == 1:
        X = X[0]
    channels = X.shape[2]
    aggregated_feature = []
    for i in select_num_map:
        x = X[:,:,i] #[7,7]
        # print(x.shape)
        # norm
        sum1 = (x ** a).sum() ** (1. / a)
        if sum1 != 0:
            weight = (x / sum1) ** (1. / b)
        else:
            weight = x
        weight = np.expand_dims(weight,axis=2).repeat(channels,axis=2) #[7,7,512]
        # print("weight:",weight.shape)
        aggregated_feature_part = weight * X  # [7,7,512]
        # print("aggregated_feature_part:",aggregated_feature_part.shape)
        aggregated_feature_part = aggregated_feature_part.sum(axis=(0, 1))  # [512]
        # print("aggregated_feature_part:",aggregated_feature_part.shape)
        aggregated_feature_part_normal = aggregated_feature_part
        # norm
        aggregated_feature_normal = L2_normalize(np.array(aggregated_feature_part_normal), copy=False)
        aggregated_feature_normal = aggregated_feature_normal.reshape((1, -1))
        # print(aggregated_feature_normal.shape)
        # print(len(aggregated_feature_normal))
        # 并列堆叠
        if len(aggregated_feature) == 0:
            aggregated_feature = aggregated_feature_normal
        else:
            aggregated_feature = np.vstack((aggregated_feature,aggregated_feature_normal))

    # print(aggregated_feature.shape) #[25, 512]
    N = aggregated_feature.shape[0]
    c = X.shape[2]
    aggregated_feature_normal = np.zeros([c])
    if sum_weighted == 1:
        for i in range(N):
            agg_feature = aggregated_feature[i]
            agg_feature = np.log(N/(0.9+i)) * agg_feature
            aggregated_feature_normal += agg_feature
        aggregated_feature_normal = aggregated_feature_normal / N
    else:
        aggregated_feature_normal = aggregated_feature.sum(0) / N
    return aggregated_feature_normal # [512]

def get_all_aggregated_feature(feature_database_dir,aggregated_save_dir,filters_num=25):
    """
    将数据库所有图像特征聚合后堆叠在一起用于度量距离
    :param feature_database_dir: 数据库特征的文件夹
    :param aggregated_save_dir: 聚合特征保存路径
    :param filters_num: 想要用多个个过滤器
    :return: void 保存所有图像聚合后的特征表示 [n, 512]
    """
    scene_list = os.listdir(feature_database_dir)
    all_aggregated_feature = []
    for each_scene in scene_list:
        each_scene_dir = os.path.join(feature_database_dir,each_scene)
        each_feature_list = os.listdir(each_scene_dir)
        for each_feature in each_feature_list:
            each_feature_dir = os.path.join(each_scene_dir,each_feature)
            filters_sort_list = select_filters(each_feature_dir) # 排序后的通道序号
            feature = np.load(each_feature_dir) # [7,7,512]
            each_aggregated_feature = PWA(filters_sort_list, feature,filters_num=filters_num) # [512]
            # 归一化的修改
            each_aggregated_feature = each_aggregated_feature / np.linalg.norm(each_aggregated_feature)
            if len(all_aggregated_feature)==0:
                all_aggregated_feature = each_aggregated_feature
            else:
                all_aggregated_feature = np.vstack((all_aggregated_feature,each_aggregated_feature))
    # print(all_aggregated_feature.shape)
    if not os.path.exists(aggregated_save_dir):
        os.mkdir(aggregated_save_dir)
    np.save(aggregated_save_dir+"/aggregate_feature_"+str(filters_num)+".npy", all_aggregated_feature)
    print("filters_num:,",filters_num,", save success!")

def get_all_aggregated_feature_forJava(image_database_dir,aggregated_save_dir,model,filters_num=100):
    """
    将数据库所有图像特征聚合后堆叠在一起用于度量距离
    :param image_database_dir: 数据库图片的文件夹
    :param aggregated_save_dir: 聚合特征保存路径
    :param model: 模型对象
    :param filters_num: 想要用多个个过滤器
    :return: void 保存所有图像聚合后的特征表示 [n, 512]
    """
    pic_list = os.listdir(image_database_dir)
    all_aggregated_feature = []
    for each_pic in pic_list:
        each_pic_dir = image_database_dir+each_pic
        each_pic_feature = extract_VGG16_feature_noSaved(each_pic_dir, model)
        filters_sort_list = select_filters1(each_pic_feature) # 排序后的通道序号
        each_aggregated_feature = PWA(filters_sort_list, each_pic_feature,filters_num=filters_num) # [512]
        # 归一化的修改
        each_aggregated_feature = each_aggregated_feature / np.linalg.norm(each_aggregated_feature)
        if len(all_aggregated_feature)==0:
            all_aggregated_feature = each_aggregated_feature
        else:
            all_aggregated_feature = np.vstack((all_aggregated_feature,each_aggregated_feature))
    # print(all_aggregated_feature.shape)
    if not os.path.exists(aggregated_save_dir):
        os.mkdir(aggregated_save_dir)
    np.save(aggregated_save_dir+"aggregate_feature_"+str(filters_num)+".npy", all_aggregated_feature)
    print("filters_num:,",filters_num,", save success!")

'''def batch_compute_distance(aggregation_feature_path,path, k=100):
    """
    批量计算距离
    :param aggregation_feature_path: 聚合特征的路径
    :param path: 待检索的特征路径
    :param k: 返回前k个结果
    :return: 返回排序后的前k个检索结果
    """
    # 为了拿到各张图片的名称，用于后面检索排序知道排在第 k 位的图片叫什么
    train_feature = IMAGE_DB_PATH
    features_list = os.listdir(train_feature)
    file_name_list = [] # 图片名称组成的列表
    # print(features_list)
    for scene in features_list:
        for feature_dir in os.listdir(os.path.join(train_feature,scene)):
            file_name_list.append(scene+'/'+feature_dir) # 将 “类别名 + 图片名” 存入 list 中

    sum_matrix = np.load(aggregation_feature_path)
    T = np.load(path)
    select_list = select_filters(path)
    query_P_avg = PWA(select_list,T) # [512]
    # print(query_P_avg.shape) # [512]

    # 计算欧式距离相似度
    # variance_matrix = tf.sqrt(tf.reduce_sum(tf.pow((sum_matrix - query_P_avg), 2), axis=1))
    variance_matrix = np.sqrt(((sum_matrix - query_P_avg)**2).sum(1))

    # # 计算余弦距离相似度 也可以使用余弦距离计算，计算得到的mAP差不多
    # sum_matrix_norm = tf.sqrt(tf.reduce_sum((sum_matrix * sum_matrix),axis=1))
    # # print(sum_matrix_norm.shape) # [n]
    # query_P_avg_norm = tf.sqrt(tf.reduce_sum(query_P_avg * query_P_avg))
    # # print(query_P_avg_norm.shape) # 数值(标量)
    # variance_matrix=tf.constant(1.)-tf.reduce_sum((sum_matrix*query_P_avg),axis=1)/(sum_matrix_norm*query_P_avg_norm)

    # 排序（升序排序）
    # idx = tf.argsort(variance_matrix)
    idx = np.argsort(variance_matrix, axis=1)
    # 将排序后的距离映射到图片名称上
    # sorted_name = tf.gather(tf.convert_to_tensor(file_name_list), idx)
    sorted_name = []
    for i in idx:
        sorted_name.append(file_name_list[i])
    return sorted_name[:k]

def query_one(pic_path,aggregation_feature_path, k=100):
    """
    查询一张图片的相似图片结果
    :param pic_path: 待检索图像的相对路径
    :param aggregation_feature_path: 聚合特征的路径
    :param k: 查找前k个结果
    :return: 返回前k个结果
    """
    # ImageDatabase/image_test/cabin/xxx.jpg
    # ImageDatabase/VGG16/test_feature/cabin/xxx.jpg
    pic_list = pic_path.split('/')
    path = 'ImageDatabase/' + CLASS_OF_MODEL + '/test_feature/' + pic_list[-2] +'/'+pic_list[-1]
    path = path[:-4]+'.npy'
    top_k_name_list = batch_compute_distance(aggregation_feature_path,path, k)
    # for i in range(3882):
    #     name = str(top_k_name_list[i])
    #     # print(name)
    #     if(name[2:9] == 'scene01'):
    #         print(top_k_name_list[i], '    ' + str(i))
    return top_k_name_list'''

if __name__ == '__main__':
    # 以下开始进行特征提取
    MODEL = VGG16(weights=None, include_top=False)  # 加载VGG16模型
    # 下面这一行是加载权重，可以不要。因为上一句 weights='imagenet' 会自动从网上下载权重文件。
    MODEL.load_weights('weight/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5')
    originalPth = "E:/CSC3170/ImageDB/images/"
    destinationPath = "E:/CSC3170/ImageDB/feature/"
    get_all_aggregated_feature_forJava(originalPth, destinationPath, MODEL, filters_num=100)
