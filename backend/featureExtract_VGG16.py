import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
import sys
sys.path.append('E:/CSC3170/cbir')
from measureAndEvaluation1 import query_one
from tensorflow.keras.preprocessing import image
import time
import numpy as np
from utils import image_border, IMAGE_DB_PATH

def extract_batch_feature(model_type, pic_path, feature_save_path):
    """
    批量特征提取：[h,w,c]，一张图片的特征保存到一个.npy文件中
    :param model_type: 特征提取模型对象
    :param pic_path: 存储图像数据集的文件夹路径，一般这个路径里面有多个分类文件夹，每个分类中包含多张图片
    :param feature_save_path: 提取出来的特征放在哪个文件夹下
    :return: void 无返回值
    """
    if not os.path.exists(feature_save_path): # 判断用于存储特征的路径是否存在，不存在先创建
        os.mkdir(feature_save_path)
    file_list = os.listdir(pic_path)
    # 只能处理jpg，jpeg和png后缀的图片
    suffix = {'jpg':1, 'jpeg':1, 'png':1}
    for name in file_list:  # 遍历所有“类别”的文件名
        # 对于每一个类别的文件夹进行判断有无，无就创建
        if not os.path.exists(feature_save_path + '/' + name):
            os.mkdir(feature_save_path + '/' + name)
        for pic in os.listdir(os.path.join(pic_path, name)): # 遍历每张图片
            suffix_str = str(pic.split('.')[-1].lower())
            if suffix.get(suffix_str) == 1:
                img_path = pic_path + "/" + name + '/' + pic
                img = image_border(img_path,resize=(224,224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)
                features = model_type.predict(x) # 提取特征
                # print(features.shape) # [1,7,7,512] # 特征的shape（h，w，c）
                features = features[0]  # [7,7,512]
                np.save(feature_save_path+'/'+name+'/'+str(pic[:-4])+".npy",features) # 保存特征
    print("特征批量提取完毕！")

def extract_VGG16_feature_noSaved(pic_path, MODEL=None):
    """
    图像检索使用：提取一张图片的特征[h,w,c]
    :param pic_path: 存储图像数据集的文件夹路径，一般这个路径里面有多个分类文件夹，每个分类中包含多张图片
    :param MODEL: 全局独一份Mode，默认为空
    :return: 返回提取特征的三维数据 [h,w,c]
    """
    if MODEL is None:
        # 以下开始进行特征提取
        MODEL = VGG16(weights=None, include_top=False)  # 加载VGG16模型
        # 下面这一行是加载权重，可以不要。因为上一句 weights='imagenet' 会自动从网上下载权重文件。
        MODEL.load_weights('../weight/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5')
    # model1 = VGG16Singleton()
    img = image_border(pic_path, resize=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = MODEL.predict(x)  # 提取特征
    # print(features.shape) # [1,7,7,512] # 特征的shape（h，w，c）
    features = features[0]  # [7,7,512]
    # print(features.shape)
    return features

def print_diff_filters_num_avg_time(filter_list, modelName, testCount):
    for filter_num in filter_list:
        aggregate_feature_path = "../ImageDatabase/"+modelName+"/train_aggregate_feature/"+"aggregate_feature_"+str(filter_num)+".npy"
        test_feature_path = "../ImageDatabase/image_test"
        start = time.time()
        for scene in os.listdir(test_feature_path):
            for pic in os.listdir(os.path.join(test_feature_path,scene)):
                pic_path = test_feature_path+"/"+scene+"/"+pic
                query_one(pic_path,aggregate_feature_path,modelName,filters_num=filter_num)
        end = time.time()
        print(str(filter_num)+" "+str((end-start)/float(testCount)))

FILTERS_NUM = 100 # 过滤器数量
if __name__ == '__main__':
    '''一、提取数据库和测试集中所有图片的特征并保存'''
    # 以下开始进行特征提取
    model = VGG16(weights=None, include_top=False)  # 加载VGG16模型
    # 下面这一行是加载权重，可以不要。因为上一句 weights='imagenet' 会自动从网上下载权重文件。
    model.load_weights('../weight/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5')
    # 提取数据库的每张图片的特征的code
    feature_save_path1 = '../ImageDatabase/VGG16/train_feature'
    extract_batch_feature(model, IMAGE_DB_PATH, feature_save_path1) # IMAGE_DB_PATH = 'E:/CSC3170/cbir/ImageDatabase/image_DB'
    print("训练数据库特征提取完毕")

    # 提取test测试集的每张图片的特征的code
    pic_path2 = '../ImageDatabase/image_test'
    feature_save_path2 = '../ImageDatabase/VGG16/test_feature'
    extract_batch_feature(model, pic_path2, feature_save_path2)
    print("测试数据库特征提取完毕")
    

    '''二、使用不同数量的过滤器检测测试集中图像检索的平均时间'''
    # filters_num_list = [20,25,50,75,100,150,160,170,180,190,200,210,220,230,240,250,300,400,512]
    # model_name = "VGG16"
    # test_count = 48 # 目前48张
    # print_diff_filters_num_avg_time(filters_num_list, model_name, test_count)
