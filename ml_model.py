"""
封装了用到的机器学习模型 和 相关的操作
1. 每个机器学习返回的是训练好的模型
2. 注意参数的shape
"""
# encoding:utf-8
import numpy as np
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

# KNN算法
def neighborKNN(trainVec,trainScore):
    knn = KNeighborsClassifier()
    knn.fit(trainVec,trainScore)
    return knn
# Logistics回归
def linearLogistic(trainVec,trainScore):
    model = linear_model.LogisticRegression(penalty = 'l1') # 采用多分类的Logistics模型
    model.fit(trainVec,trainScore)
    return model
# 随机森林
def randomForest(trainVec,trainScore):
    model = RandomForestClassifier(max_depth=None) # 取消最大深度，防止过拟合
    model.fit(trainVec, trainScore)
    return model
# 多分类支持向量机
def SVM(trainVec,trainScore):
    model = SVC()
    model.fit(trainVec, trainScore)
    return model
# 采取多项式朴素贝叶斯
def naiveBayes(trainVec,trainScore):
    model = MultinomialNB()
    model.fit(trainVec,trainScore)
    return model

def saveModel(model,modelname):
    """
    存储训练好的模型
    :param model: 训练好的机器学习模型
    :param modelname: 模型存储路径
    :return: None
    """
    try:
        with open(modelname,'wb',encoding='utf-8') as f:
            f.dump(model,modelname)
    except Exception as error:
        print('模型存储失败，因为：',error)

def readModel(modelname):
    """
    读取存储的模型
    :param modelname: 模型的路径
    :return: 读取成功，返回模型；否则，返回None
    """
    try:
        model = None
        with open(modelname,'rb',encoding='utf-8') as f:
            model = f.load(f)
    except Exception as error:
        print('模型读取失败，因为：',error)
    else:
        return model