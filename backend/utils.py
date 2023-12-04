import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import csv
from sklearn.preprocessing import normalize as sknormalize
import shutil
from PIL import Image
import numpy as np
import cv2

FRAME_INTERVAL = 15
rename_path = './ImageDatabase/InceptionV3'
suffix_pic = '.jpg'
suffix_feature = '.npy'
def rename(path, suffix_pic,suffix_feature):
    old_name_list = os.listdir(path)
    for each_dir in old_name_list:
        scenes_list = os.listdir(rename_path +'/'+ each_dir)
        for file_dir in scenes_list:
            small_old_name_list = os.listdir(rename_path+'/'+each_dir+'/'+file_dir)
            # print(len(old_name_list)) # 4304
            # print(old_name_list)
            for old_name in small_old_name_list:
                index = old_name.split('.')[0][15:]
                # print(index)
                # print(type(index))
                if len(index) == 1:
                    new_index = '0000' + index
                    if old_name.endswith('.jpg'):
                        os.rename(rename_path+'/'+each_dir+'/'+file_dir + '/' + old_name,
                                  rename_path+'/'+each_dir+'/'+file_dir + '/' +'C919TestFlight_' + new_index + suffix_pic)
                    if old_name.endswith('.npy'):
                        os.rename(rename_path + '/' + each_dir + '/' + file_dir + '/' + old_name,
                                  rename_path + '/' + each_dir + '/' + file_dir + '/' + 'C919TestFlight_' + new_index + suffix_feature)
                elif len(index) == 2:
                    new_index = '000' + index
                    if old_name.endswith('.jpg'):
                        os.rename(rename_path + '/' + each_dir + '/' + file_dir + '/' + old_name,
                                  rename_path + '/' + each_dir + '/' + file_dir + '/' + 'C919TestFlight_' + new_index + suffix_pic)
                    if old_name.endswith('.npy'):
                        os.rename(rename_path + '/' + each_dir + '/' + file_dir + '/' + old_name,
                                  rename_path + '/' + each_dir + '/' + file_dir + '/' + 'C919TestFlight_' + new_index + suffix_feature)
                elif len(index) == 3:
                    new_index = '00' + index
                    if old_name.endswith('.jpg'):
                        os.rename(rename_path + '/' + each_dir + '/' + file_dir + '/' + old_name,
                                  rename_path + '/' + each_dir + '/' + file_dir + '/' + 'C919TestFlight_' + new_index + suffix_pic)
                    if old_name.endswith('.npy'):
                        os.rename(rename_path + '/' + each_dir + '/' + file_dir + '/' + old_name,
                                  rename_path + '/' + each_dir + '/' + file_dir + '/' + 'C919TestFlight_' + new_index + suffix_feature)
                elif len(index) == 4:
                    new_index = '0' + index
                    if old_name.endswith('.jpg'):
                        os.rename(rename_path + '/' + each_dir + '/' + file_dir + '/' + old_name,
                                  rename_path + '/' + each_dir + '/' + file_dir + '/' + 'C919TestFlight_' + new_index + suffix_pic)
                    if old_name.endswith('.npy'):
                        os.rename(rename_path + '/' + each_dir + '/' + file_dir + '/' + old_name,
                                  rename_path + '/' + each_dir + '/' + file_dir + '/' + 'C919TestFlight_' + new_index + suffix_feature)
                else:
                    break

# 复制并新建文件夹名
def create_dir():
    train_dir_path = 'ImageDatabase/indoor_images/train'
    test_dir_path = 'ImageDatabase/indoor_images/test'
    train_dir_list = os.listdir(train_dir_path)
    # print(train_dir_list)
    for directory in train_dir_list:
        create_path = test_dir_path + '/' + directory
        if not os.path.exists(create_path):
            os.mkdir(create_path)

def split_train_test():
    dic_split = {}
    with open('ImageDatabase/bird_images/train_test_split.txt') as f:
        reader = csv.reader(f)
        for row in reader:
            data = row[0].split(' ')
            dic_split[data[0]] = data[1]
    # print(dic_split)

    dic_image = {}
    with open('ImageDatabase/bird_images/images.txt') as f:
        reader = csv.reader(f)
        for row in reader:
            data = row[0].split(' ')
            dic_image[data[1]] = data[0]

    train_path = 'ImageDatabase/bird_images/train'
    test_path = 'ImageDatabase/bird_images/test'
    for key in dic_image:
        value = dic_image[key]
        trainOrTest = dic_split[value] # 0/1 1:train
        source_path = train_path + '/' + key
        target_path = test_path + '/' + key
        if trainOrTest == str(1):
            shutil.move(source_path, target_path)

def splitTrainAndTest():
    train_path = 'ImageDatabase/indoor_images/train'
    test_path = 'ImageDatabase/indoor_images/test'
    for eachClass in os.listdir(train_path):
        pics_list = os.listdir(os.path.join(train_path,eachClass))
        eachClass_num = len(pics_list)
        test_num = int(eachClass_num / 10)
        i = 0
        while i < eachClass_num:
            source_path = train_path +'/'+ eachClass +'/'+ pics_list[i]
            target_path = test_path +'/'+ eachClass +'/'+ pics_list[i]
            shutil.move(source_path, target_path)
            i += 10

def image_DB_num(src):
    """
    计算数据库中图片的总数量
    :param src: 数据库路径
                - src               总目录
                    - scene01       场景类别目录
                        - pic01     场景图像目录
                        ...
                    - scene02
                    ...
    :return: 数据库中图片的数量
    """
    class_list = os.listdir(src)
    i = 0
    suffix = {'jpg': 1, 'jpeg': 1, 'png': 1}
    for scene in class_list:
        scene_path = os.path.join(src,scene)
        scene_list = os.listdir(scene_path)
        for img_path in scene_list:
            suffix_str = str(img_path.split('.')[-1].lower())
            if suffix.get(suffix_str) == 1:
                i += 1
            else:
                continue
    return i

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

def image_border(src, resize=(224,224)):
    """
    给不是正方形的图片四周加白条，然后将图片resize成224*224的
    :param src: 图片路径
    :param resize: resize后的大小，默认是224×224，是VGG16的标准输入尺寸
    :return: 返回加完白条并resize后的image
    """
    img_ori = Image.open(src)
    w = img_ori.size[0]
    h = img_ori.size[1]

    max_value = w if w > h else h
    img_new = Image.new('RGB', (max_value,max_value), (255,255,255))
    width = int(abs(w-h)/2)
    x_start = 0
    y_start = 0
    if h != max_value:
        x_start = width
    if w != max_value:
        y_start = width
    img_new.paste(img_ori,(y_start,x_start))
    img_new1 = img_new.resize(size=resize)
    return img_new1

def image_border_imgArr(imgArr, resize=(224,224)):
    """
    给不是正方形的图片四周加白条，然后将图片resize成224*224的
    :param imgArr: 图片matrix
    :param resize: resize后的大小，默认是224×224，是VGG16的标准输入尺寸
    :return: 返回加完白条并resize后的image
    """
    img_ori = cv2.cvtColor(imgArr, cv2.COLOR_BGR2GRAY)
    w = len(img_ori[0])
    h = len(img_ori)
    max_value = w if w > h else h
    up = int((max_value - h) / 2)
    down = max_value - h - up
    left = int((max_value - w) / 2)
    right = max_value - w - left
    after = np.pad(img_ori, ((up,down),(left,right)),'constant',constant_values=(255,255))
    after = cv2.resize(after,resize)
    return cv2.cvtColor(after, cv2.COLOR_GRAY2BGR)

def get_scene_name_list(path):
    """
    获取“scenexx/picNamexx”这样的名称列表
    :param path: 存储类别和图片名称的总目录
    :return: 返回一个有名字的列表
    """
    scene_name_list = []
    for scene in os.listdir(path):
        for pic in os.listdir(os.path.join(path,scene)):
            scene_name_list.append(scene+'/'+pic)
    return scene_name_list

def get_imgDB_name_list(path, save_path):
    name_list = os.listdir(path)
    np.save(save_path, name_list)

def get_test_img_count(test_path):
    """
    返回测试文件夹中有几张图片
    :param test_path: 测试图片文件夹路径
    :return: 返回数量
    """
    count = 0
    scene_list = os.listdir(test_path)
    for scene in scene_list:
        count += len(os.listdir(os.path.join(test_path,scene)))
    return count

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

def extract_batch_feature(model_type, pic_path, feature_save_path, resizeShape):
    """
    批量特征提取：[h,w,c]，一张图片的特征保存到一个.npy文件中
    :param model_type: 特征提取模型对象
    :param pic_path: 存储图像数据集的文件夹路径，一般这个路径里面有多个分类文件夹，每个分类中包含多张图片
    :param feature_save_path: 提取出来的特征放在哪个文件夹下
    :param resizeShape: resize成多大的尺寸
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
                img = image_border(img_path,resize=resizeShape)
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)
                features = model_type.predict(x) # 提取特征
                # print(features.shape) # [1,7,7,512] # 特征的shape（h，w，c）
                features = features[0]  # [7,7,512]
                np.save(feature_save_path+'/'+name+'/'+str(pic[:-4])+".npy",features) # 保存特征
    print("特征批量提取完毕！")

IMAGE_DB_PATH = 'E:/CSC3170/cbir/ImageDatabase/image_DB' # 存储图片集的路径
NUM_OF_DATABASE = image_DB_num(IMAGE_DB_PATH) # 实时统计图片集的数量（注意：该图片集智能存储jpeg，jpg，png的图片）
SCENE_NAME_LIST = get_scene_name_list(IMAGE_DB_PATH) # 获取分类名的list，验证检索准确度时使用
if __name__ == '__main__':
    # 获取图片数据库图片的名称列表
    imgDB_path = IMAGE_DB_PATH
    # imgDB_path = "E:/ImageDB/images/" # 图片库文件夹路径
    imgDB_name_list_save_path = "E:/ImageDB/imageDBNamelist.npy" # 图片库所有图片名组成的name_list保存的路径
    get_imgDB_name_list(imgDB_path, imgDB_name_list_save_path)