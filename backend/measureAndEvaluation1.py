from utils import NUM_OF_DATABASE,IMAGE_DB_PATH,select_filters,PWA
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

def compute_distance(aggregation_feature_path,feature,n=1):
    # 拿到每张图片的类名+图片名
    scenes_list = os.listdir(IMAGE_DB_PATH)
    scene_name_list = []
    for scene in scenes_list:
        scene_dir = os.path.join(IMAGE_DB_PATH, scene)
        pics_list = os.listdir(scene_dir)
        for pic in pics_list:
            scene_name_list.append(scene + '/' + pic)

    sum_matrix = np.load(aggregation_feature_path)

    query_feature = feature
    query_feature = query_feature / np.linalg.norm(query_feature)

    # 计算欧式距离
    variance_distance = (((sum_matrix - query_feature) ** 2).sum(1)) ** 0.5
    # 排序
    idx = np.argsort(variance_distance)
    # print(len(idx))
    # print(idx)
    # 将排序后的距离映射到类名+图片名上
    sorted_name_list = []
    for i in idx:
        sorted_name_list.append(scene_name_list[i])
    return sorted_name_list[:n]

def batch_compute_distance(aggregation_feature_path,path,k=NUM_OF_DATABASE,filters_num=25,agg_method=3):
    """
    批量计算距离
    :param aggregation_feature_path: 聚合特征路径
    :param path: 待检索图像特征路径
    :param k: 返回前k个结果
    :param filters_num: 使用的过滤器数量
    :param agg_method: 特征的聚合方式，默认为3
    :return: 返回排序后的前k个结果的名称
    """
    # 拿到每张图片的类名+图片名
    scenes_list = os.listdir(IMAGE_DB_PATH)
    scene_name_list = []
    for scene in scenes_list:
        scene_dir = os.path.join(IMAGE_DB_PATH,scene)
        pics_list = os.listdir(scene_dir)
        for pic in pics_list:
            scene_name_list.append(scene+'/'+pic)

    # 加载聚合特征文件
    sum_matrix = np.load(aggregation_feature_path)

    # 加载待检测图片特征并对特征处理
    T = np.load(path)
    # 对待检索图像的特征进行聚合
    select_list = select_filters(path)
    query_feature = None
    if agg_method == 3:
        query_feature = PWA(select_list,T,filters_num=filters_num)
        query_feature = query_feature / np.linalg.norm(query_feature)
    elif agg_method == 1:
        query_feature = (T.sum(0)).sum(0)
    elif agg_method == 2:
        query_feature = PWA(select_list,T,filters_num=filters_num,sum_weighted=0)

    # 计算欧式距离
    variance_distance = (((sum_matrix-query_feature)**2).reshape(1, -1).sum(1))**0.5
    # 排序
    idx = np.argsort(variance_distance)
    # print(len(idx))
    # print(idx)
    # 将排序后的距离映射到类名+图片名上
    sorted_name_list = []
    for i in idx:
        sorted_name_list.append(scene_name_list[i])
    return sorted_name_list[:k]

def query_one(pic_path, aggregated_feature_path,model_name='VGG16', k=NUM_OF_DATABASE,filters_num=25,agg_method=3):
    """
    查询一张图片的相似图片结果
    :param pic_path: 一张图片路径
    :param model_name:
    :param aggregated_feature_path: 聚合特征路径
    :param k: 查找前k个结果
    :param filters_num: 使用过滤器的个数
    :param agg_method:
    :return: 返回前k个结果的数组名称
    """
    # 图片名：ImageDatabase/image_test/cabin/xxx.jpg
    # 修改后：ImageDatabase/VGG16/test_feature/cabin/xxx.npy
    pic_list = pic_path.split('/')
    path = 'E:/CSC3170/cbir/ImageDatabase/'+model_name+'/test_feature/'+pic_list[-2]+'/'+pic_list[-1]
    path = path[:-4] + '.npy' # 注意这个地方，如果图片文件的后缀不是.jpg的要考虑[.后缀]的数量。
    top_k_name_list = batch_compute_distance(aggregated_feature_path,path,k,filters_num=filters_num,agg_method=agg_method)
    return top_k_name_list

def accuracy_of_topK(query_pic,top_k_name,k=1):
    """
    返回前k个结果的准确率
    :param query_pic: 待检索图像的类别：scenexx
    :param top_k_name: 所有检索出来排好序的图像名称
    :param k: 计算每个AP的前k个的scene准确率
    :return: 返回前k个准确率
    """
    num = 0 # 记录类别相同的个数
    for i in range(k):
        # res = str(top_k_name[i])[2:-1]
        res = top_k_name[i].split('/')[0]
        if query_pic == res:
            num += 1
    return num / float(k)

def accuracy_of_topK2(query_pic,top_k_name,k=1):
    """
    给compute_reRanking_AP用的
    :param query_pic: 待检索图像的类别：scenexx
    :param top_k_name: 所有检索出来排好序的图像list
    :param k: 计算每个AP的前k个的scene准确率
    :return: 返回前k个准确率
    """
    num = 0 # 记录类别相同的个数
    for i in range(k):
        res = top_k_name[i].split('/')[0]
        if query_pic == res:
            num += 1
    return num / float(k)

def compute_AP(pic_path,aggregate_feature_path,model_name='VGG16', k=NUM_OF_DATABASE,filters_num=25,agg_method=3):
    """
    计算一张图像检索的AP
    :param pic_path: 一张图片的路径
    :param aggregate_feature_path: 聚合特征的路径
    :param model_name:
    :param k: 检索多少张
    :param filters_num: 过滤器的使用数量
    :param agg_method:
    :return: 返回AP
    """
    top_k_name_list = query_one(pic_path,aggregate_feature_path,model_name,k,filters_num,agg_method=agg_method)
    # print('top_k_name_list:',top_k_name_list)
    query_pic_scene = pic_path.split('/')[-2] # 待检索图片的类别：scenexx
    AP = 0 # average precession
    R = 0 # 表示总相关的图像数量
    for i in range(len(top_k_name_list)):
        # top_k_name[i]: 类名 + 图片名
        # res = str(top_k_name_list[i])[2:-1]
        name = top_k_name_list[i]
        res = name.split('/')[0] # 返回结果图像的类别：scenexx
        i = i + 1
        rel = 0 # rel(k)表示位置k上的图像是否相关,默认为0，不相关
        pk = accuracy_of_topK(query_pic_scene,top_k_name_list,i) # p(k)表示前k个结果的准确率
        if res == query_pic_scene:
            R += 1
            rel = 1
        AP += pk * rel
    return AP / float(R)

def compute_mAP_all(query_pic_dir,aggregate_feature_path,model_name='VGG16', k=NUM_OF_DATABASE,filters_num=25,agg_method=3):
    """
    计算mAP
    :param query_pic_dir: 待检索的图片文件夹 是一个test的文件夹
    :param aggregate_feature_path: 聚合特征的路径
    :param model_name:
    :param k: 检索多少张
    :param filters_num: 过滤器数量
    :param agg_method:
    :return: 返回mAP
    """
    meanAveragePrecision = 0
    Q = 0 # 待检索图像的数量
    scene_list = os.listdir(query_pic_dir)
    for scene in scene_list:
        pics_list = os.listdir(os.path.join(query_pic_dir,scene))
        Q += len(pics_list)
        for pic_dir in pics_list:
            pic_path = query_pic_dir+'/'+scene+'/'+pic_dir
            AP = compute_AP(pic_path,aggregate_feature_path,model_name, k,filters_num,agg_method=agg_method)
            # print(scene +'/'+ pic_dir + ': ' + str(AP))
            meanAveragePrecision += AP
    return meanAveragePrecision / float(Q)

def get_three_dist(query_agg_path, database_agg_path):
    """
    获取三个矩阵形式的距离 distance
    :param query_agg_path: 待检索图像的聚合特征路径，加载后shape:[n,512], n:待检索图像数量
    :param database_agg_path: 数据库图像聚合特征路径，加载后shape:[m,512], m:数据库图像数量
    :return:
        q_g_dist: 每个 query 图像与 每个 database 图像间的距离
        q_q_dist: 每个 query 图像与 每个 query 图像间的距离
        g_g_dist: 每个 database 图像与 每个 database 图像间的距离
    """
    query_feature = np.load(query_agg_path) # [n,512]
    database_feature = np.load(database_agg_path) # [m,512]
    q_g_dist = np.dot(query_feature,np.transpose(database_feature))
    q_q_dist = np.dot(query_feature,np.transpose(query_feature))
    g_g_dist = np.dot(database_feature,np.transpose(database_feature))
    return q_g_dist, q_q_dist, g_g_dist

def get_three_dist1(query_feature, database_agg_path):
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
    query_feature = np.expand_dims(query_feature,axis=0) # [1,512]
    # print(query_feature.shape)
    database_feature = np.load(database_agg_path) # [m,512]
    q_g_dist = np.dot(query_feature,np.transpose(database_feature))
    q_q_dist = np.dot(query_feature,np.transpose(query_feature))
    g_g_dist = np.dot(database_feature,np.transpose(database_feature))
    return q_g_dist, q_q_dist, g_g_dist

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

def compute_reRanking_mAP(test_scene_list, query_agg_path,database_agg_path, train_name_list,
                          k1, k2, lambda_value):
    """
    计算重排序后的mAP值
    :param test_scene_list: 测试集的scene的list
    :param query_agg_path: 测试集的聚合特征路径
    :param database_agg_path: 数据库的聚合特征路径
    :param train_name_list: 数据库的scene+name的list
    :param k1:
    :param k2:
    :param lambda_value:
    :return: 返回重排序后的mAP值
    """
    q_g_dist, q_q_dist, g_g_dist = get_three_dist(query_agg_path, database_agg_path)
    final_dist = re_ranking(q_g_dist, q_q_dist, g_g_dist, k1=k1, k2=k2, lambda_value=lambda_value) # [422,3882] 未排序

    mAP1 = 0
    Q = len(test_scene_list)  # 待检索图像的数量
    for i in range(final_dist.shape[0]):
        each_query_dist = final_dist[i] # [251]
        index = np.argsort(each_query_dist)
        reRank_name_list = []
        for idx in range(len(train_name_list)):
            reRank_name_list.append(train_name_list[index[idx]])
        query_pic_scene = test_scene_list[i]  # 待检索图片的类别：scenexx
        AP = 0  # average precession
        R = 0  # 表示总相关的图像数量
        for j in range(len(reRank_name_list)):
            res = reRank_name_list[j].split('/')[0]  # 返回结果图像的类别：scenexx
            j = j + 1
            rel = 0  # rel(k)表示位置k上的图像是否相关,默认为0，不相关
            pk = accuracy_of_topK2(query_pic_scene, reRank_name_list, j)  # p(k)表示前k个结果的准确率
            if res == query_pic_scene:
                R += 1
                rel = 1
            AP += pk * rel
        AP =  AP / float(R)
        # print(query_pic_scene+'AP: ', AP)
        mAP1 += AP
    return mAP1 / float(Q)

def get_train_name_list(train_path):
    """
    获取数据库中所有图片的类名+图片名
    :param train_path: 数据库的路径
    :return: 返回存放名称的list
    """
    name_list = []
    for scene in os.listdir(train_path):
        for pic_name in os.listdir(os.path.join(train_path,scene)):
            name_list.append(scene + '/' + pic_name)
    return name_list

def get_test_scene_list(test_path):
    """
    获取测试集中各个scene中对应图片数量的scene数量到list中
    :param test_path: 测试集的路径
    :return: 返回测试集scene的list
    """
    list_test = []
    for scene in os.listdir(test_path):
        len_scene = len(os.listdir(os.path.join(test_path,scene)))
        for x in range(len_scene):
            list_test.append(scene)
    return list_test

def draw_pics(name_list, query_path):
    """
    检索一张图片并将检索结果绘制出来
    :param name_list: 排序好的的名称列表
    :param query_path: 待检索图像路径
    :return: void 无返回值
    """
    img_list = []
    for img in name_list:
        img_list.append('ImageDatabase/image_DB/' + img)
    # 待检索图像
    plt.subplot(3, 5, 3)
    plt.imshow(cv2.cvtColor(cv2.imread(query_path), cv2.COLOR_BGR2RGB))
    plt.title((query_path.split('/')[-1]).split('_')[-1])
    plt.xticks(())
    plt.yticks(())

    # 检索结果图像
    for i in range(10):
        plt.subplot(3, 5, i + 6)
        plt.imshow(cv2.cvtColor(cv2.imread(img_list[i]), cv2.COLOR_BGR2RGB))
        plt.title((img_list[i].split('/')[-1]).split('_')[-1])
        plt.xticks(())
        plt.yticks(())
        ax = plt.gca()
        if img_list[i].split('/')[-2] == query_path.split('/')[-2]:
            ax.spines['bottom'].set_linewidth('2.0') # 设置线宽
            ax.spines['bottom'].set_linestyle("-") # 设置样式
            ax.spines['bottom'].set_color('#00ff00') # 设置颜色
            ax.spines['top'].set_linewidth('2.0')  # 设置线宽
            ax.spines['top'].set_linestyle("-")  # 设置样式
            ax.spines['top'].set_color('#00ff00')  # 设置颜色
            ax.spines['left'].set_linewidth('2.0')  # 设置线宽
            ax.spines['left'].set_linestyle("-")  # 设置样式
            ax.spines['left'].set_color('#00ff00')  # 设置颜色
            ax.spines['right'].set_linewidth('2.0')  # 设置线宽
            ax.spines['right'].set_linestyle("-")  # 设置样式
            ax.spines['right'].set_color('#00ff00')  # 设置颜色
        else:
            ax.spines['bottom'].set_linewidth('2.0')  # 设置线宽
            ax.spines['bottom'].set_linestyle("-")  # 设置样式
            ax.spines['bottom'].set_color('red')  # 设置颜色
            ax.spines['top'].set_linewidth('2.0')  # 设置线宽
            ax.spines['top'].set_linestyle("-")  # 设置样式
            ax.spines['top'].set_color('red')  # 设置颜色
            ax.spines['left'].set_linewidth('2.0')  # 设置线宽
            ax.spines['left'].set_linestyle("-")  # 设置样式
            ax.spines['left'].set_color('red')  # 设置颜色
            ax.spines['right'].set_linewidth('2.0')  # 设置线宽
            ax.spines['right'].set_linestyle("-")  # 设置样式
            ax.spines['right'].set_color('red')  # 设置颜色
    # plt.savefig('ImageDatabase/queryResult/beforeReRank/'+query_path.split('/')[-1],dpi=300)
    plt.show()

if __name__ == '__main__':
    model_name1 = 'VGG16'  # RestNet50 / VGG16

    # query one
    # aggregate_feature_path1 = 'ImageDatabase/VGG16/test_aggregate_feature/aggregate_feature_100.npy'
    # for scene1 in os.listdir('ImageDatabase/image_test'):
    #     for pic1 in os.listdir(os.path.join('ImageDatabase/image_test',scene1)):
    #         pic_path1 = 'ImageDatabase/image_test/'+scene1+'/'+pic1
    #         top_k_name_list1 = query_one(pic_path1,aggregate_feature_path1,filters_num=100)
    #         draw_pics(top_k_name_list1,pic_path1)

    # 计算所有test图像检索结果的mAP
    # query_pic_dir_all1 = 'ImageDatabase/image_test'
    # aggregate_feature_path1 = 'ImageDatabase/'+model_name1+'/train_aggregate_feature/aggregate_feature_100.npy'
    # mAP = compute_mAP_all(query_pic_dir_all1,aggregate_feature_path1,model_name=model_name1, k=NUM_OF_DATABASE,filters_num=100)
    # print('filters_num :',100,'mAP: ',mAP) # 别人的方法：0.7677 ====> 我的方法：VGG:76.92% filters=100
                                                                            # ResNet:75.63

    # 重排序 re-rank
    test_scene_list1 = get_test_scene_list('ImageDatabase/image_test')
    query_agg_path1 = 'ImageDatabase/'+model_name1+'/test_aggregate_feature/aggregate_feature_100.npy'
    database_agg_path1 = 'ImageDatabase/'+model_name1+'/train_aggregate_feature/aggregate_feature_100.npy'
    train_name_list1 = get_train_name_list('ImageDatabase/image_DB')
    mAP = compute_reRanking_mAP(test_scene_list1,query_agg_path1,database_agg_path1,train_name_list1,
                                k1=40, k2=5, lambda_value=0.3)
    print('re-rank mAP: ',mAP) # 别人的方法：0.8242 ====> 我的方法：VGG:81.34% filters=100
                                                                # ResNet:80.67%
