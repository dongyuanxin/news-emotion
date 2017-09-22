__author__ == 'asruaDong'

import numpy as np
import random

class GenerateSample(object):
    def __init__(self,trainset ,topk = 10,loop = 4):
        self._trainset = trainset
        self.__size = len(self._trainset) # 样本数量
        self.topk = topk # 最邻近的k个元素
        self.loop = loop # 循环几次

    @classmethod
    def _cosSimilar(cls,arr_x,arr_y):
        res = GenerateSample(np.array([arr_x,arr_y])).cosSimilar(np.array(arr_x),np.array(arr_y))
        print(res)

    #  计算余弦相似度
    def cosSimilar(self,arr_x,arr_y):
        if len(arr_y) != len(arr_x):
            return None
        top_result = np.sum(arr_x * arr_y)
        bottom_result = np.sqrt(np.sum(arr_x**2)*np.sum(arr_y**2))
        return top_result/bottom_result

    # 返回距离index位置的向量的余弦距离
    def disArray(self,index = None):
        if (not index) or (index<0 or index>self.__size):
            index = np.random.randint(0,self.__size) # 如果没有index，随机分布生成
        # new：index是0，而距离又是[-1,1]。所以为了排序方便，直接取绝对值
        dis_arr = [self.cosSimilar(onevector , self._trainset[index]) for onevector in self._trainset] # 每个元素均计算
        return np.array(dis_arr),index

    # 参数是处理好的disArray
    def neighborArray(self,disarr):
        neighbor_index = np.argsort(disarr)[self.__size-self.topk:self.__size-1]
        return self._trainset[neighbor_index],neighbor_index

    # 开始生成
    def generate(self):
        dis_arr , base_index = self.disArray() # base_index 基础vector
        neighbor_arr, neighor_index = self.neighborArray(dis_arr)
        near_index = random.choice(neighor_index)
        near_vector = self._trainset[near_index] # 选出的最近vector
        # base_index && near_index 是我们选中的两个点
        for i in range(self.loop):
            alpha = np.random.rand() # 均匀分布生成系数
            if i % 2:
                alpha *= (-1) # 增加/减少扰动
            near_vector = near_vector + alpha*(near_vector-self._trainset[base_index])
        self.__baseindex = base_index
        self.__nearindex = near_index
        self.__neighborindex = neighor_index
        return near_vector

    def show(self,x_num = 1,y_num = 1):
        try:
            assert len(self._trainset[0]==2) # 这里只对2个基数的vector做展示
            import matplotlib as mpl
            import matplotlib.pyplot as plt
        except Exception as error:
            print('请安装对应版本的matplotlib')
            return
        else:
            mpl.rcParams['font.sans-serif'] = ['FangSong']
            mpl.rcParams['axes.unicode_minus'] = False
            plt.figure()
            for i in range(x_num):
                for j in range(y_num):
                    plt.subplot(x_num,y_num,y_num*i+j+1)
                    plt.scatter(self._trainset[:,0],self._trainset[:,1],color = 'blue',s = 1.5)
                    vector = self.generate()
                    plt.scatter(self._trainset[self.__baseindex,0],self._trainset[self.__baseindex,1],color="green",s = 10)
                    plt.scatter(self._trainset[self.__neighborindex, 0], self._trainset[self.__neighborindex, 1], color="yellow", s=10)
                    plt.scatter(vector[0],vector[1],color="red",s = 10)
            plt.show()

    def test(self,x_num = 5,y_num = 5):
        TOP = 100
        BOTTOM = 1
        SIZE = 100
        arr = np.array([[np.random.randint(BOTTOM, TOP), np.random.randint(BOTTOM, TOP)] for i in range(SIZE)])
        myclass = GenerateSample(arr)
        myclass.show(x_num,y_num)

if __name__=='__main__':
    pass