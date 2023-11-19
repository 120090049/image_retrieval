import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.applications.vgg16 import VGG16

class VGG16Singleton(object):
    def __init__(self):
        print("VGG16单例对象创建")
    @classmethod
    def instance(cls):
        if not hasattr(VGG16Singleton, "_instance"):
            VGG16Singleton._instance = VGG16(weights=None, include_top=False)  # 加载VGG16模型
            # 下面这一行是加载权重，可以不要。因为上一句 weights='imagenet' 会自动从网上下载权重文件。
            path = "weight/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5"
            VGG16Singleton._instance.load_weights(path)
        return VGG16Singleton._instance

if __name__ == '__main__':
    single_1 = VGG16Singleton.instance()
    single_2 = VGG16Singleton.instance()

    print(single_1 is single_2)  # True
    print(single_1)
    print(single_2)